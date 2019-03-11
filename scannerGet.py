# encoding:utf-8
__author__ = 'shiliang'
__date__ = '2019/3/11 20:56'

from thrift.transport import TSocket,TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase

def connectHBase():
    '''
    连接远程HBase
    :return: 连接HBase的客户端实例
    '''
    # thrift默认端口是9090
    socket = TSocket.TSocket('10.0.86.245',9090) # 10.0.86.245是master结点ip
    socket.setTimeout(5000)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Hbase.Client(protocol)
    socket.open()
    return client

def ListTables(client):
    '''
    列出所有表
    '''
    print(client.getTableNames())

def scannerGetSelect(client, tableName, columns, startRow, stopRow=None, rowsCnt=2000):
    '''
    依次扫描HBase指定表的每行数据(根据起始行，扫描到表的最后一行或指定行的前一行)
    :param client: 连接HBase的客户端实例
    :param tableName: 表名
    :param columns: 一个包含(一个或多个列簇下对应列名的)列表
    :param startRow: 起始扫描行
    :param stopRow:  停止扫描行(默认为空)
    :param rowsCnt:  需要扫描的行数
    :return MutilRowsDict: 返回一个包含多行数据的字典，以每行行键定位是哪一行
    '''
    # 如果stopRow为空，则使用scannerOpen方法扫描到表最后一行
    if stopRow is None:
        scannerId = client.scannerOpen(tableName, startRow, columns)
    # 如果stopRow不为空，则使用scannerOpenWithStop方法扫描到表的stopRow行
    else:
        scannerId = client.scannerOpenWithStop(tableName, startRow, stopRow, columns)
    results = client.scannerGetList(scannerId, rowsCnt)
    # 如果查询结果不为空，则传入行键值或列值参数正确
    if results:
        MutilRowsDict = {}
        for result in results:
            RowDict = {}          # 一个包含一行所有列簇:列值字典的字典
            colFamilyDict = {}    # 一个包含当前列簇下所有的列值的字典
            preColFamily = None      # 记录前一次循环的列簇值，为空表示遍历该列簇的第一个列值起
            cnt = 0                  # 循环计数器
            for key, TCell_value in result.columns.items():
                cnt += 1
                # 获取该行行键
                rowKey = result.row
                # 由于key值是'列簇:列名'形式,所以需要通过split函数以':'把列名分割出来
                colFamily_colName = key.split(':') # 一个含有1.列簇2.列名的列表
                colFamily = colFamily_colName[0]  # 列簇
                colName = colFamily_colName[1]    # 列名
                # 如果本次列簇为空或和上次循环的列簇相同，则每个列值归属为colFamilyDict字典中并更新上一次列簇的记录
                if (preColFamily is None) or preColFamily == colFamily:
                    colFamilyDict[colName] = TCell_value.value
                    preColFamily = colFamily  # 记录上一次列簇名
                # 如果本次列簇和上次循环的列簇不相同，则把含有列值的colFamilyDict归属为RowDict字典中并清空colFamilyDict字典和preColFamily记录
                else:
                    RowDict[preColFamily] = colFamilyDict
                    colFamilyDict = {}
                    colFamilyDict[colName] = TCell_value.value
                    preColFamily = None
                # 若是最后一次迭代，则把含有列值的colFamilyDict归属为RowDict字典中
                if cnt == len(result.columns.items()):
                    RowDict[colFamily] = colFamilyDict
            # 把当前含有多个列值信息的行的字典和改行行键存储在MutilRowsDict中
            MutilRowsDict[rowKey] = RowDict
        return MutilRowsDict
    # 如果查询结果为空，则传入行键值或列值参数错误，返回空列表
    else:
        return []

if __name__ == '__main__':
    tableName = '2018AAAI'  # 数据库表名
    # 连接HBase数据库，返回客户端实例
    client = connectHBase()
    MutilRowsDict = scannerGetSelect(client, tableName, ['paper:title', 'creator'], '20180291')
    print(MutilRowsDict)
    # 列出所有表名
    ListTables(client)