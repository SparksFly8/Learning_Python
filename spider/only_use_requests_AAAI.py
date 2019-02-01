import time
from lxml import etree
import requests

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
    response = requests.get(url)  # 提交请求,获取响应内容
    html = response.content  # 获取网页内容(content返回的是bytes型数据,text()获取的是Unicode型数据)
    title = etree.HTML(html).xpath('//*[@id="title"]/text()')  # 由xpath解析HTML
    print('第%d个title:%s' % (cnt, ''.join(title)))

if __name__ == '__main__':
    start1 = time.time()
    i = 0
    for url in urls:
        i = i + 1
        start = time.time()
        get_title(url, i)
        print('第%d个title爬取耗时:%.5f秒' % (i, float(time.time() - start)))
    print('爬取总耗时:%.5f秒' % float(time.time() - start1))