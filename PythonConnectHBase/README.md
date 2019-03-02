# Learning_Python
## 前提条件

 1. 已安装Python-3.6。
 2. 已经有搭建好的完全分布式集群，并已经**成功启动Hadoop，Zookeeper和HBase**。笔者当前搭建好的集群是`Hadoop-3.0.3`，`Zookeeper-3.4.13`和`HBase-2.1.0`。

 
| Hostname  | IP | 
|--|--|
| master  | 10.0.86.245 |
| ceph1 | 10.0.86.246 |
| ceph2  | 10.0.86.221 |
| ceph3  | 10.0.86.253 |

## 一、下载Thrift安装包到远程集群的`master`结点中
Thrift-0.11.0链接：https://github.com/SparksFly8/Tools

**Ubuntu安装Thrift依赖：**
```js
apt-get install automake bison flex g++ git libboost1.55 libevent-dev libssl-dev libtool make pkg-config
```
**CentOS-7.5安装Thrift依赖：**
```js
yum install automake bison flex g++ git libboost1.55 libevent-dev libssl-dev libtool make pkg-config
```
解压并编译thrift，我是解压到`/usr/local/`中。
```js
tar -zxvf thrift-0.11.0.tar.gz
cd thrift-0.11.0
./configure --with-cpp --with-boost --with-python --without-csharp --with-java --without-erlang --without-perl --with-php --without-php_extension --without-ruby --without-haskell  --without-go
make
make install
```
在master结点中Hbase安装目录下的`/usr/local/hbase/bin`目录启动thrift服务
```js
[root@master bin]# ./hbase-daemon.sh start thrift
```
启动成功master状态如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190302002158486.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
## 二、本地Python连接远程集群中的HBase
①分别下载两个安装包：`thrift`和`hbase-thrift`。
②在`..\site-packages\hbase`下替换两个文件，[Hbase.py](https://github.com/SparksFly8/Tools/blob/master/Hbase.py)和[ttypes.py](https://github.com/SparksFly8/Tools/blob/master/ttypes.py)。
```js
F:\Env\virtual3.6\Lib\site-packages\hbase  # 我自己本地放置包的路径
```
③运行如下示例代码：连接HBase：

```js
from thrift.transport import TSocket,TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase

# thrift默认端口是9090
socket = TSocket.TSocket('10.0.86.245',9090) # 10.0.86.245是master结点ip
socket.setTimeout(5000)

transport = TTransport.TBufferedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)
socket.open()

print(client.getTableNames())  # 获取当前所有的表名
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190302003544396.png)
运行结果对比HBase中数据表正确：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190302095412154.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
## 三、本地Python操作远程HBase常用方法
说明：以下案例均建立在上述成功连接HBase的基础上运行。
> **1.建表**

【函数】：`createTable(tableName, columnFamilies)`
【参数】：tableName-表名； columnFamilies-列簇(列表)
【案例】：

```js
from hbase.ttypes import ColumnDescriptor
# 定义列族
col1 = ColumnDescriptor(name='c1')
col2 = ColumnDescriptor(name='c2')
# 创建表
client.createTable('table',[col1, col2])
print(client.getTableNames())  # 获取当前所有的表名,返回一个包含所有表名的列表
```
等价于HBase Shell命令：
```js
$ create 'table','c1','c2'
```

执行结果：

```js
['table']
```
> **2.删除表**

【函数】：`deleteTable(tableName)`
【参数】：tableName-表名
【案例】：

```js
client.disableTable('table') # 删除表前需要先设置该表不可用
client.deleteTable('table')
print(client.getTableNames())  # 获取当前所有的表名,返回一个包含所有表名的列表
```
等价于HBase Shell命令：
```js
$ disable 'table'
$ drop 'table'
```
执行结果：

```js
[]
```
> **3.向某行某列插入/更新数据**

【函数】：`mutateRow(tableName, row, mutations)`
【参数】：tableName-表名；row-行键；mutations-变化(列表)；
【案例】：

```js
def insertRow(client, tableName, rowName, colFamily, columnName, value):
    mutations = [Mutation(column='{0}:{1}'.format(colFamily, columnName), value=str(value))]
    client.mutateRow(tableName, rowName, mutations)
    print('在{0}表{1}列簇{2}列插入{3}数据成功.'.format(tableName, colFamily, columnName, value))

insertRow(client, 'table', '0001', 'c1', 'hobby2', 'watch movies')
print(client.get('table','0001','c1')[0].value) 
```
等价于HBase Shell命令：
```js
$ put 'table','0001','c1:hobby2','watch movies'
```
执行结果：

```js
在table表c1列簇hobby2列插入watch movies数据成功.
```
> **4.读取指定列簇指定列数据**

【函数1】：`get(tableName, row, column)`
【函数2】：`getVer(tableName, row, column, numVersions)`

【参数】：tableName-表名；row-行键；numVersions-版本号；
column-指定列簇的列名(或仅填列簇名也ok)；
【案例】：

```js
# 若该行下指定列簇有多个列，则返回的是个包含多个列值的列表，可用索引来指明是哪一列
print(client.get('table','0001','c1')[index].value)
print(client.getVer('table','0001','c1',1))[index].value) 
# 获取固定列簇固定列的值，即仅包含一个值的列表，需用索引0来获取。
print(client.get('table','0001','c1:hobby2')[0].value)
print(client.getVer('table','0001','c1:hobby2',1))[0].value) 
```
等价于HBase Shell命令：
```js
$ get 'table','0001','c1'
$ get 'table','0001','c1:hobby2'
```
执行结果：

```js
watch movies
```
> **5.遍历指定行所有数据**

【函数1】：`getRow(tableName, row)`
【函数2】：`getRowWithColumns(tableName, row, columns)`

【参数】：tableName-表名；row-行键；column-一个指定列簇指定列名的列表(若仅填列簇名就返回该列簇下所有列值)；
【案例】：

```js
results = client.getRow('table','0001')
for result in results:
    print(result.columns.get('c1:hobby2').value)
    
results = client.getRowWithColumns('table','0001',['c1'])) 
for result in results:
    print(result.columns.get('c1:hobby2').value)
    
results = client.getRowWithColumns('table','0001',['c1:hobby2'])
for result in results:
    print(result.columns.get('c1:hobby2').value)
```
等价于HBase Shell命令：
```js
$ get 'table','0001'
$ get 'table','0001','c1'
$ get 'table','0001','c1:hobby2'
```
执行结果：

```js
watch movies
```
【额外补充】：以下是我根据`getRow`和`getRowWithColumns`两个函数，经过数据清洗成常用字典形式，并**过滤冒号**，返回仅含有列名对应列值的字典。其中对于以下三种情况分别进行了处理：
①获取HBase指定表**指定行**的所有数据，以**字典**形式作为返回值。
②获取HBase指定表指定行**指定列簇**的所有数据，以**字典**形式作为返回值。
③获取HBase指定表指定行**指定列簇指定列**的数据，以**字符串**形式作为返回值。

```js
'''
    功能：获取HBase指定表的某一行数据。  
    @param client 连接HBase的客户端实例
    @param tableName 表名
    @param rowName 行键名
    @param colFamily 列簇名
    @param columns 一个包含指定列名的列表
    @return RowDict 一个包含列名和列值的字典(若直接返回指定列值，则返回的是字符串)
'''
def getRow(client, tableName, rowName, colFamily=None, columns=None):
    # 1.如果列簇和列名两个都为空，则直接取出当前行所有值，并转换成字典形式作为返回值
    if colFamily is None and columns is None:
        results = client.getRow(tableName, rowName)
        RowDict = {}
        for result in results:
            for key, TCell_value in result.columns.items():
                # 由于key值是'列簇:列名'形式,所以需要通过split函数以':'把列名分割出来
                each_col = key.split(':')[1]
                RowDict[each_col] = TCell_value.value # 取出TCell元组中的value值
        return RowDict
    # 2.如果仅是列名为空，则直接取出当前列簇所有值，并转换成字典形式作为返回值
    elif columns is None:
        results = client.getRowWithColumns(tableName, rowName, [colFamily])
        RowDict = {}
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

print(getRow(client, 'table', '0001'))
print(getRow(client, 'table', '0001', 'c1'))
print(getRow(client, 'table', '0001', 'c1', 'hobby2'))
```
执行结果：

```js
# 第一个结果
{'age': '25', 'hobby1': 'reading', 'hobby2': 'watch movies', 'name': 'Tom', 'age': '30', 'hobby11': 'reading books'}
# 第二个结果
{'age': '25', 'hobby1': 'reading', 'hobby2': 'watch movies', 'name': 'Tom'}
# 第三个结果
watch movies
```


【参考文献】：
[\[1\] 使用 Python 和 Thrift 连接 HBase.](http://shzhangji.com/cnblogs/2018/04/22/connect-hbase-with-python-and-thrift/)
[\[2\] 用Python3.6操作HBase之HBase-Thrift.](https://blog.csdn.net/luanpeng825485697/article/details/81048468)

