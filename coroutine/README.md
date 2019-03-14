# Python异步IO之协程（一）:从yield from到async的使用
> 引言：协程(coroutine)是Python中一直较为难理解的知识，但其在多任务协作中体现的效率又极为的突出。众所周知，Python中执行多任务还可以通过`多进程`或`一个进程中的多线程`来执行，但两者之中均存在一些缺点。因此，我们引出了协程。
## 目录
 1. [《Python异步IO之协程(一):从yield from到async的使用》](https://blog.csdn.net/SL_World/article/details/86597738)
 2. [《Python异步IO之协程(二):使用asyncio的不同方法实现协程》](https://blog.csdn.net/SL_World/article/details/86691747)

## *为什么需要协程？*
首先，我们需要知道同步和异步是什么东东，不知道的看[详解](https://www.cnblogs.com/Anker/p/5965654.html)。
简单来说：

**【同步】：就是发出一个“调用”时，在没有得到结果之前，该“调用”就不返回，“调用者”需要一直等待该“调用”结束，才能进行下一步工作。**

**【异步】：“调用”在发出之后，就直接返回了，也就没有返回结果。“被调用者”完成任务后，通过状态来通知“调用者”继续回来处理该“调用”。**

下面我们先来看一个用普通同步代码实现多个IO任务的案例。
```js
# 普通同步代码实现多个IO任务
import time
def taskIO_1():
    print('开始运行IO任务1...')
    time.sleep(2)  # 假设该任务耗时2s
    print('IO任务1已完成，耗时2s')
def taskIO_2():
    print('开始运行IO任务2...')
    time.sleep(3)  # 假设该任务耗时3s
    print('IO任务2已完成，耗时3s')

start = time.time()
taskIO_1()
taskIO_2()
print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
```
执行结果：
```js
开始运行IO任务1...
IO任务1已完成，耗时2s
开始运行IO任务2...
IO任务2已完成，耗时3s
所有IO任务总耗时5.00604秒
```
上面，我们顺序实现了两个同步IO任务`taskIO_1()`和`taskIO_2()`，则最后总耗时就是**5秒**。我们都知道，在计算机中CPU的运算速率要远远大于IO速率，而当CPU运算完毕后，如果再要闲置很长时间去等待IO任务完成才能进行下一个任务的计算，这样的任务执行效率很低。

所以我们需要有一种异步的方式来处理类似上述任务，会极大增加效率(当然就是协程啦～)。而我们最初很容易想到的，**是能否在上述IO任务执行前中断当前IO任务**(对应于上述代码`time.sleep(2)`)，**进行下一个任务，当该IO任务完成后再唤醒该任务。**

而在Python中**生成器**中的关键字`yield`可以实现**中断功能**。所以起初，协程是基于生成器的变形进行实现的，之后虽然编码形式有变化，但基本原理还是一样的。[戳我查看生成器及迭代器和可迭代对象的讲解和区别](https://blog.csdn.net/SL_World/article/details/86507872)。

## 一、使用yield from和@asyncio.coroutine实现协程
在Python3.4中，协程都是通过使用yield from和`asyncio模块`中的@asyncio.coroutine来实现的。`asyncio`专门被用来实现异步IO操作。
#### （1）什么是yield from?和yield有什么区别?
【1】我们都知道，`yield`在生成器中有中断的功能，可以传出值，也可以从函数外部接收值，而`yield from`的实现就是简化了`yield`操作。
让我们先来看一个案例：

```js
def generator_1(titles):
    yield titles
def generator_2(titles):
    yield from titles

titles = ['Python','Java','C++']
for title in generator_1(titles):
    print('生成器1:',title)
for title in generator_2(titles):
    print('生成器2:',title)
```
执行结果如下：
```js
生成器1: ['Python', 'Java', 'C++']
生成器2: Python
生成器2: Java
生成器2: C++
```
在这个例子中`yield titles`返回了`titles`完整列表，而`yield from titles`实际等价于：

```js
for title in titles:　# 等价于yield from titles
    yield title　　
```
【2】而`yield from`功能还不止于此，它还有一个主要的功能是省去了很多异常的处理，不再需要我们手动编写，其**内部已经实现大部分异常处理**。

【举个例子】：下面通过生成器来实现一个**整数加和**的程序，通过`send()`函数向生成器中传入要加和的数字，然后最后以返回`None`结束，`total`保存最后加和的总数。

```js
def generator_1():
    total = 0
    while True:
        x = yield 
        print('加',x)
        if not x:
            break
        total += x
    return total
def generator_2(): # 委托生成器
    while True:
        total = yield from generator_1() # 子生成器
        print('加和总数是:',total)
def main(): # 调用方
    g1 = generator_1()
    g1.send(None)
    g1.send(2)
    g1.send(3)
    g1.send(None)
    # g2 = generator_2()
    # g2.send(None)
    # g2.send(2)
    # g2.send(3)
    # g2.send(None)
    
main()
```
执行结果如下。可见对于生成器`g1`，在最后传入`None`后，程序退出，报`StopIteration`异常并返回了最后`total`值是５。

```js
加 2
加 3
加 None
------------------------------------------
StopIteration       
<ipython-input-37-cf298490352b> in main()
---> 19     g1.send(None)
StopIteration: 5
```
如果把`g1.send()`那５行注释掉，解注下面的`g2.send()`代码，则结果如下。可见`yield from`**封装了处理常见异常的代码**。对于`g2`即便传入`None`也不报异常，其中`total = yield from generator_1()`返回给`total`的值是`generator_1()`最终的`return total`

```js
加 2
加 3
加 None
加和总数是: 5
```
【3】借用上述例子，这里有几个概念需要理一下：

 - **【子生成器】**：yield from后的generator_1()生成器函数是**子生成器**
 - **【委托生成器】**：generator_2()是程序中的**委托生成器**，它负责委托**子生成器**完成具体任务。
 -  **【调用方】**：main()是程序中的**调用方**，负责调用委托生成器。 

**`yield from`在其中还有一个关键的作用是：建立调用方和子生成器的通道**，

 - 在上述代码中`main()`每一次在调用`send(value)`时，`value`不是传递给了**委托生成器**generator_2()，而是借助`yield from`传递给了**子生成器**generator_1()中的`yield`
 - 同理，**子生成器**中的数据也是通过`yield`直接发送到**调用方**main()中。
 
*之后我们的代码都依据`调用方-子生成器-委托生成器`的**规范形式**书写。*
#### （2）如何结合@asyncio.coroutine实现协程
那`yield from`通常用在什么地方呢？在协程中，**只要是和IO任务类似的、耗费时间的任务都需要使用`yield from`来进行中断，达到异步功能！**
我们在上面那个同步IO任务的代码中修改成协程的用法如下：
```js
# 使用同步方式编写异步功能
import time
import asyncio
@asyncio.coroutine # 标志协程的装饰器
def taskIO_1():
    print('开始运行IO任务1...')
    yield from asyncio.sleep(2)  # 假设该任务耗时2s
    print('IO任务1已完成，耗时2s')
    return taskIO_1.__name__
@asyncio.coroutine # 标志协程的装饰器
def taskIO_2():
    print('开始运行IO任务2...')
    yield from asyncio.sleep(3)  # 假设该任务耗时3s
    print('IO任务2已完成，耗时3s')
    return taskIO_2.__name__
@asyncio.coroutine # 标志协程的装饰器
def main(): # 调用方
    tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
    done,pending = yield from asyncio.wait(tasks) # 子生成器
    for r in done: # done和pending都是一个任务，所以返回结果需要逐个调用result()
        print('协程无序返回值：'+r.result())

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
    try:
        loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
    finally:
        loop.close() # 结束事件循环
    print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
```
执行结果如下：

```js
开始运行IO任务1...
开始运行IO任务2...
IO任务1已完成，耗时2s
IO任务2已完成，耗时3s
协程无序返回值：taskIO_2
协程无序返回值：taskIO_1
所有IO任务总耗时3.00209秒
```
【使用方法】： `@asyncio.coroutine`**装饰器**是协程函数的标志，我们需要在每一个任务函数前加这个装饰器，并在函数中使用`yield from`。在同步IO任务的代码中使用的`time.sleep(2)`来假设任务执行了2秒。但在协程中`yield  from`后面必须是**子生成器函数**，**而`time.sleep()`并不是生成器**，所以这里需要使用内置模块提供的生成器函数`asyncio.sleep()`。

【功能】：通过使用协程，极大增加了多任务执行效率，最后消耗的时间是任务队列中耗时最多的时间。上述例子中的总耗时3秒就是`taskIO_2()`的耗时时间。

【执行过程】：

 1. 上面代码先通过`get_event_loop()`**获取**了一个**标准事件循环**loop(因为是一个，所以协程是单线程)
 2. 然后，我们通过`run_until_complete(main())`来运行协程(此处把调用方协程main()作为参数，调用方负责调用其他委托生成器)，`run_until_complete`的特点就像该函数的名字，直到循环事件的所有事件都处理完才能完整结束。
 3. 进入调用方协程，我们把多个任务[`taskIO_1()`和`taskIO_2()`]放到一个`task`列表中，可理解为打包任务。
 4. 现在，我们使用`asyncio.wait(tasks)`来获取一个**awaitable objects即可等待对象的集合**(此处的aws是协程的列表)，**并发运行传入的aws**，同时通过`yield from`返回一个包含`(done, pending)`的元组，**done表示已完成的任务列表，pending表示未完成的任务列表**；如果使用`asyncio.as_completed(tasks)`则会按完成顺序生成协程的**迭代器**(常用于for循环中)，因此当你用它迭代时，会尽快得到每个可用的结果。【此外，当**轮询**到某个事件时(如taskIO_1())，直到**遇到**该**任务中的`yield from`中断**，开始**处理下一个事件**(如taskIO_2()))，当`yield from`后面的子生成器**完成任务**时，该事件才再次**被唤醒**】
 5. 因为`done`里面有我们需要的返回结果，但它目前还是个任务列表，所以要取出返回的结果值，我们遍历它并逐个调用`result()`取出结果即可。(注：对于`asyncio.wait()`和`asyncio.as_completed()`返回的结果均是先完成的任务结果排在前面，所以此时打印出的结果不一定和原始顺序相同，但使用`gather()`的话可以得到原始顺序的结果集，[两者更详细的案例说明见此](https://blog.csdn.net/SL_World/article/details/86691747))
 6. 最后我们通过`loop.close()`关闭事件循环。


综上所述：协程的完整实现是靠**①事件循环＋②协程**。
## 二、使用async和await实现协程
在Python 3.4中，我们发现很容易将**协程和生成器混淆**(虽然协程底层就是用生成器实现的)，所以在后期加入了其他标识来区别协程和生成器。

在**Python 3.5**开始引入了新的语法`async`和`await`，以简化并更好地**标识异步IO**。

要使用新的语法，只需要做两步简单的替换：

 - 把`@asyncio.coroutine`替换为`async`；
 -  把`yield from`替换为`await`。

更改上面的代码如下，可得到同样的结果：

```js
import time
import asyncio
async def taskIO_1():
    print('开始运行IO任务1...')
    await asyncio.sleep(2)  # 假设该任务耗时2s
    print('IO任务1已完成，耗时2s')
    return taskIO_1.__name__
async def taskIO_2():
    print('开始运行IO任务2...')
    await asyncio.sleep(3)  # 假设该任务耗时3s
    print('IO任务2已完成，耗时3s')
    return taskIO_2.__name__
async def main(): # 调用方
    tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
    done,pending = await asyncio.wait(tasks) # 子生成器
    for r in done: # done和pending都是一个任务，所以返回结果需要逐个调用result()
        print('协程无序返回值：'+r.result())

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
    try:
        loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
    finally:
        loop.close() # 结束事件循环
    print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
```

## 三、总结
最后我们将整个过程串一遍。
【引出问题】：
 1. 同步编程的并发性不高
 2. **多进程**编程效率受CPU核数限制，当任务数量远大于CPU核数时，执行效率会降低。
 3. **多线程**编程需要线程之间的通信，而且需要**锁机制**来防止**共享变量**被不同线程乱改，而且由于Python中的**GIL(全局解释器锁)**，所以实际上也无法做到真正的并行。
 

 【产生需求】：
 1. 可不可以采用**同步**的方式来**编写异步**功能代码？
 2.  能不能只用一个**单线程**就能做到不同任务间的切换？这样就没有了线程切换的时间消耗，也不用使用锁机制来削弱多任务并发效率！
 3. 对于IO密集型任务，可否有更高的处理方式来节省CPU等待时间？

【结果】：所以**协程**应运而生。当然，实现协程还有其他方式和函数，以上仅展示了一种较为常见的实现方式。此外，**多进程和多线程是内核级别**的程序，而**协程是函数级别**的程序，是可以通过程序员进行调用的。以下是协程特性的总结：

|协程| 属性 |
|--|--|
| 所需线程 | **单线程**<br>(因为仅定义一个loop，所有event均在一个loop中) |
| 编程方式 | 同步 |
| 实现效果 | **异步** |
| 是否需要锁机制 | 否 |
| 程序级别 | 函数级 |
| 实现机制 | **事件循环＋协程** |
| 总耗时 | 最耗时事件的时间 |
| 应用场景 | IO密集型任务等 |

【额外加餐】：使用`tqdm`库实现**进度条**
这是一个免费的库：`tqdm`是一个用来生成进度条的优秀的库。这个协程就像`asyncio.wait`一样工作，不过会显示一个代表完成度的进度条。详情见：[python进度可视化](https://ptorch.com/news/170.html)

```js
async def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        await f
```
## 四、结束语
感谢大家能耐心读到这里，写了这么多文字，再来个真实的案例实战一下效果更佳哦~！
以下是一个[协程在爬虫的应用实战案例](https://blog.csdn.net/SL_World/article/details/86633611)，其中对比了分布式多进程爬虫，最后将异步爬虫和多进程爬虫融合，效果更好。


# Python异步IO之协程（二）:使用asyncio的不同方法实现协程

> 引言：在[上一章](https://blog.csdn.net/SL_World/article/details/86597738)中我们介绍了从yield from的来源到async的使用，并在最后以`asyncio.wait()`方法实现协程，下面我们通过不同控制结构来实现协程，让我们一起来看看他们的不同作用吧～

 
在多个协程中的**线性控制流**很容易**通过**内置的**关键词`await`来管理**。使用`asyncio`模块中的方法可以实现更多复杂的结构，它可以**并发地**完成多个协程。
## 一、asyncio.wait()
你可以将一个操作分成多个部分并分开执行，而`wait(tasks)`可以被用于**中断**任务集合(tasks)中的某个**被事件循环轮询**到的**任务**，直到该协程的其他后台操作完成才**被唤醒**。

```js
import time
import asyncio
async def taskIO_1():
    print('开始运行IO任务1...')
    await asyncio.sleep(2)  # 假设该任务耗时2s
    print('IO任务1已完成，耗时2s')
    return taskIO_1.__name__
async def taskIO_2():
    print('开始运行IO任务2...')
    await asyncio.sleep(3)  # 假设该任务耗时3s
    print('IO任务2已完成，耗时3s')
    return taskIO_2.__name__
async def main(): # 调用方
    tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
    done,pending = await asyncio.wait(tasks) # 子生成器
    for r in done: # done和pending都是一个任务，所以返回结果需要逐个调用result()
        print('协程无序返回值：'+r.result())

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
    try:
        loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
    finally:
        loop.close() # 结束事件循环
    print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
```
执行结果如下：
```js
开始运行IO任务1...
开始运行IO任务2...
IO任务1已完成，耗时2s
IO任务2已完成，耗时3s
协程无序返回值：taskIO_2
协程无序返回值：taskIO_1
所有IO任务总耗时3.00209秒
```

【解释】：wait()[官方文档](https://docs.python.org/zh-cn/3/library/asyncio-task.html)用法如下：
```js
done, pending = await asyncio.wait(aws)
```
此处并发运行传入的`aws`(awaitable objects)，同时通过`await`返回一个包含(done, pending)的元组，**done**表示**已完成**的任务列表，**pending**表示**未完成**的任务列表。

**注：**

①只有当给`wait()`传入`timeout`参数时才有可能产生`pending`列表。

②通过`wait()`返回的**结果集**是**按照**事件循环中的任务**完成顺序**排列的，所以其往往**和原始任务顺序不同**。
## 二、asyncio.gather()
如果你只关心协程并发运行后的结果集合，可以使用`gather()`，它不仅通过`await`返回仅一个结果集，而且这个结果集的**结果顺序**是传入任务的**原始顺序**。
```js
import time
import asyncio
async def taskIO_1():
    print('开始运行IO任务1...')
    await asyncio.sleep(3)  # 假设该任务耗时3s
    print('IO任务1已完成，耗时3s')
    return taskIO_1.__name__
async def taskIO_2():
    print('开始运行IO任务2...')
    await asyncio.sleep(2)  # 假设该任务耗时2s
    print('IO任务2已完成，耗时2s')
    return taskIO_2.__name__
async def main(): # 调用方
    resualts = await asyncio.gather(taskIO_1(), taskIO_2()) # 子生成器
    print(resualts)

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
    try:
        loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
    finally:
        loop.close() # 结束事件循环
    print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
```
执行结果如下：
```js
开始运行IO任务2...
开始运行IO任务1...
IO任务2已完成，耗时2s
IO任务1已完成，耗时3s
['taskIO_1', 'taskIO_2']
所有IO任务总耗时3.00184秒
```
【解释】：`gather()`通过`await`直接**返回**一个结果集**列表**，我们可以清晰的从执行结果看出来，虽然任务2是先完成的，但最后返回的**结果集的顺序是按照初始传入的任务顺序排的**。
## 三、asyncio.as_completed()
`as_completed(tasks)`是一个生成器，它管理着一个**协程列表**(此处是传入的tasks)的运行。当任务集合中的某个任务率先执行完毕时，会率先通过`await`关键字返回该任务结果。可见其返回结果的顺序和`wait()`一样，均是按照**完成任务顺序**排列的。
```js
import time
import asyncio
async def taskIO_1():
    print('开始运行IO任务1...')
    await asyncio.sleep(3)  # 假设该任务耗时3s
    print('IO任务1已完成，耗时3s')
    return taskIO_1.__name__
async def taskIO_2():
    print('开始运行IO任务2...')
    await asyncio.sleep(2)  # 假设该任务耗时2s
    print('IO任务2已完成，耗时2s')
    return taskIO_2.__name__
async def main(): # 调用方
    tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
    for completed_task in asyncio.as_completed(tasks):
        resualt = await completed_task # 子生成器
        print('协程无序返回值：'+resualt)

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
    try:
        loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
    finally:
        loop.close() # 结束事件循环
    print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
```

执行结果如下：
```js
开始运行IO任务2...
开始运行IO任务1...
IO任务2已完成，耗时2s
协程无序返回值：taskIO_2
IO任务1已完成，耗时3s
协程无序返回值：taskIO_1
所有IO任务总耗时3.00300秒
```
【解释】：从上面的程序可以看出，使用`as_completed(tasks)`和`wait(tasks)`**相同之处**是返回结果的顺序是**协程的完成顺序**，这与gather()恰好相反。而**不同之处**是`as_completed(tasks)`可以**实时返回**当前完成的结果，而`wait(tasks)`需要等待所有协程结束后返回的`done`去获得结果。
## 四、总结
以下`aws`指：`awaitable objects`。即**可等待对象集合**，如一个协程是一个可等待对象，一个装有多个协程的**列表**是一个`aws`。

| asyncio |  主要传参 |　返回值顺序  | `await`返回值类型 | 函数返回值类型 |

|--|--|--|--|--|

| wait() | aws | 协程完成顺序 | (done,pending)<br>装有两个任务列表元组 | coroutine |

| as_completed() | aws  | 协程完成顺序 | 原始返回值 | 迭代器 |

|  gather() | *aws | 传参任务顺序 | 返回值列表 | awaitable |




【我的博客对应地址】：https://blog.csdn.net/SL_World/article/details/86597738


