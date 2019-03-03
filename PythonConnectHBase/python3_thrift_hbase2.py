# -*- coding: utf-8 -*-
__author__ = 'shiliang'
__date__ = '2019/3/1 23:48'

import math

from thrift.transport import TSocket,TTransport
from thrift.protocol import TBinaryProtocol
from hbase.ttypes import ColumnDescriptor
from hbase import Hbase
from hbase.ttypes import Mutation


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
    mutations = [Mutation(column='{0}:{1}'.format(colFamily, columnName), value=str(value))]
    client.mutateRow(tableName, rowName, mutations)
    print('在{0}表{1}列簇{2}列插入{3}数据成功.'.format(tableName, colFamily, columnName, value))


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

if __name__ == '__main__':
    # 连接HBase数据库，返回客户端实例
    client = connectHBase()
    # 创建表
    # createTable(client, 'firstTable', 'c1', 'c2', 'c3')
    # 插入或更新列值
    # insertRow(client, 'firstTable', '0001', 'c1', 'name', 'sparks')
    # 获取HBase指定表的某一行数据
    dataDict = getRow(client, 'firstTable', '0001')
    print(dataDict)
    # 删除指定表某行数据
    # deleteAllRow(client, '2018AAAI_Papers', '20181106')
    # 列出所有表名
    ListTables(client)
