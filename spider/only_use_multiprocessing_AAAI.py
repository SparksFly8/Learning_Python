import multiprocessing
from multiprocessing import Pool
import time
import requests
from lxml import etree

urls = [
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16488',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16583',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16380',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16911',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16581',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16674',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16112',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/17343',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16659',
    'https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewPaper/16449',
]
'''
提交请求获取AAAI网页,并解析HTML获取title
'''
def get_title(url, cnt):
    response = requests.get(url)  # 提交请求
    html = response.content  # 获取网页内容
    title = etree.HTML(html).xpath('//*[@id="title"]/text()')  # 由xpath解析HTML
    print('第%d个title:%s' % (cnt, ''.join(title)))


'''
调用方
'''
def main():
    print('当前环境CPU核数是：%d核' % multiprocessing.cpu_count())
    p = Pool(4)  # 进程池
    i = 0
    for url in urls:
        i += 1
        p.apply_async(get_title, args=(url, i))
    p.close()
    p.join()  # 运行完所有子进程才能顺序运行后续程序


if __name__ == '__main__':
    start = time.time()
    main()  # 调用方
    print('总耗时：%.5f秒' % float(time.time() - start))
