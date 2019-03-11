# -*- coding: utf-8 -*-
__author__ = 'shiliang'
__date__ = '2019/3/1 23:48'

import math

from thrift.transport import TSocket,TTransport
from thrift.protocol import TBinaryProtocol
from hbase.ttypes import ColumnDescriptor
from hbase import Hbase
from hbase.ttypes import Mutation
from tqdm import tqdm
import xlrd


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

def createTable(client, tableName, *colFamilys):
    '''
    创建新表
    :param client: 连接HBase的客户端实例
    :param tableName: 表名
    :param *colFamilys: 任意个数的列簇名
    '''
    colFamilyList = []
    # 根据可变参数定义列族
    for colFamily in colFamilys:
        col = ColumnDescriptor(name=str(colFamily))
        colFamilyList.append(col)
    # 创建表
    client.createTable(tableName,colFamilyList)
    print('建表成功！')

def deleteTable(client, tableName):
    '''
    删除表
    '''
    if client.isTableEnabled(tableName):
        client.disableTable(tableName)  # 删除表前需要先设置该表不可用
    client.deleteTable(tableName)
    print('删除表{}成功！'.format(tableName))

def deleteTable(client, tableName):
    '''
    删除表
    :param client: 连接HBase的客户端实例
    :param tableName: 表名
    :return:
    '''
    if client.isTableEnabled(tableName):
        client.disableTable(tableName)
    client.deleteTable(tableName)
    print('删除表'+tableName+'成功.')

def deleteAllRow(client, tableName, rowKey):
    '''
    删除指定表某一行数据
    :param client: 连接HBase的客户端实例
    :param tableName: 表名
    :param rowKey: 行键
    '''
    if getRow(client, tableName, rowKey):
        client.deleteAllRow(tableName, rowKey)
        print('删除{0}表{1}行成功！'.format(tableName, rowKey))
    else:
        print('错误提示：未找到{0}表{1}行数据！'.format(tableName, rowKey))

def insertRow(client, tableName, rowName, colFamily, columnName, value):
    '''
    在指定表指定行指定列簇插入/更新列值
    '''
    mutations = [Mutation(column='{0}:{1}'.format(colFamily, columnName), value=str(value).encode('utf-8').decode('utf-8'))]
    client.mutateRow(tableName, rowName, mutations)
    # print('在{0}表{1}列簇{2}列插入{3}数据成功.'.format(tableName, colFamily, columnName, value))


def getRow(client, tableName, rowName, colFamily=None, columns=None):
    '''
    功能：获取HBase指定表的某一行数据。
    :param client 连接HBase的客户端实例
    :param tableName 表名
    :param rowName 行键名
    :param colFamily 列簇名
    :param columns 一个包含指定列名的列表
    :return RowDict 一个包含列名和列值的字典(若直接返回指定列值，则返回的是字符串)
    '''
    # 1.如果列簇和列名两个都为空，则直接取出当前行所有值，并转换成字典形式作为返回值
    RowDict = {}
    if colFamily is None and columns is None:
        results = client.getRow(tableName, rowName)
        for result in results:
            for key, TCell_value in result.columns.items():
                # 由于key值是'列簇:列名'形式,所以需要通过split函数以':'把列名分割出来
                each_col = key.split(':')[1]
                RowDict[each_col] = TCell_value.value # 取出TCell元组中的value值
        return RowDict
    # 2.如果仅是列名为空，则直接取出当前列簇所有值，并转换成字典形式作为返回值
    elif columns is None:
        results = client.getRowWithColumns(tableName, rowName, [colFamily])
        for result in results:
            for key, TCell_value in result.columns.items():
                # 由于key值是'列簇:列名'形式,所以需要通过split函数以':'把列名分割出来
                each_col = key.split(':')[1]
                RowDict[each_col] = TCell_value.value  # 取出TCell元组中的value值
        return RowDict
    # 3.如果列簇和列名都不为空，则直接取出当前列的值
    elif colFamily is not None and columns is not None:
        results = client.getRow(tableName, rowName)
        for result in results:
            value = result.columns.get('{0}:{1}'.format(colFamily, columns)).value
        return value
    else:
        raise Exception('关键参数缺失，请重新检查参数！')

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
            RowDict = {}
            for key, TCell_value in result.columns.items():
                # 获取该行行键
                rowKey = result.row
                # 由于key值是'列簇:列名'形式,所以需要通过split函数以':'把列名分割出来
                each_col = key.split(':')[1]
                RowDict[each_col] = TCell_value.value  # 取出TCell元组中的value值
                # 把当前含有多个列值信息的行的字典和改行行键存储在MutilRowsDict中
                MutilRowsDict[rowKey] = RowDict
        return MutilRowsDict
    # 如果查询结果为空，则传入行键值或列值参数错误，返回空列表
    else:
        return []

def bigInt2str(bigNum):
    '''
    大整数转换为字符串
    :param bigNum: 大整数
    :return string: 转换后的字符串
    '''
    string = ''
    for i in range(len(str(bigNum)),0,-1):
        a = int(math.pow(10, (i-1)))
        b = bigNum//a%10
        string += str(b)
    return string

def xlsx2HBase(client, xlsx_Path, tableName, colFamily1, colFamily2, year):
    '''
    xlsx数据上传到HBase中
    :param client: 连接HBase的客户端实例
    :param xlsx_Path: xlsx文件所在地址
    :param tableName: 表名
    :param colFamily1: 列簇1
    :param colFamily2: 列簇2
    :param year: 年份
    '''
    # 1.打开所在工作簿
    data = xlrd.open_workbook(xlsx_Path)
    # 2.获取工作簿中的sheet
    sheet = data.sheets()[0]
    # 3.获取当前sheet的行数(含表头)
    nRows = sheet.nrows
    # 从第1行遍历到第nRows-1行,tqdm()使用进度条
    for RowNum in tqdm(range(1,nRows)):
        rowName = year+'{:0>4d}'.format(RowNum) # 根据年份和行值拼接成字符串形成rowKey
        for ColNum in range(2,5):               # 从第2列遍历到第4列
            value = sheet.cell(RowNum, ColNum).value   # 单元格信息
            if value != '0':
                header = sheet.cell(0, ColNum).value       # 每列的表头信息
                insertRow(client, tableName, rowName, colFamily1, header, value)
                # print('第'+rowName+'行'+header+'列插入数据成功.')
        for ColNum in range(5,47):  # 从第5列遍历到第46列
            value = sheet.cell(RowNum, ColNum).value   # 单元格信息
            if value != '0':
                header = sheet.cell(0, ColNum).value  # 每列的表头信息
                insertRow(client, tableName, rowName, colFamily2, header, value)
                # print('第'+rowName+'行'+header+'列插入数据成功.')

if __name__ == '__main__':
    tableName = '2018AAAI' # 数据库表名
    # tableName = '2018AAAI_Papers' # 数据库表名
    # tableName = 'trash' # 数据库表名
    colFamily1 = 'paper_info'     # 第一个列簇
    colFamily2 = 'creator_info'   # 第二个列簇
    xlsx_Path = 'C:\\Users\\Administrator\\Desktop\\whole_data.xlsx'
    year = '2018'

    # 连接HBase数据库，返回客户端实例
    client = connectHBase()
    # ListTables(client)
    # xlsx数据上传到HBase中
    # xlsx2HBase(client, xlsx_Path, tableName, colFamily1, colFamily2, year)
    # 创建表
    # createTable(client, tableName, colFamily1, colFamily2)
    # 插入或更新列值
    # insertRow(client, tableName, '20180936', 'creator_info', 'affiliation2', 'Ecole Polytechnique Fédérale de Lausanne (EPFL)')
    # 获取HBase指定表的某一行数据
    # dataDict = getRow(client, 'firstTable', '0001')
    # print(dataDict)
    # 删除指定表某行数据
    # deleteAllRow(client, '2018AAAI_Papers', '20181106')
    # 删除整表
    # deleteTable(client, tableName)
    # 依次扫描HBase指定表的每行数据(根据起始行，扫描到表的最后一行或指定行的前一行)
    # MutilRowsDict = scannerGetSelect(client, tableName, ['creator_info:affiliation2'], '20180936')
    # print(MutilRowsDict)
    # 列出所有表名
    ListTables(client)
