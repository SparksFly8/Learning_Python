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
