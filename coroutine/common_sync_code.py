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
