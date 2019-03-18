# encoding:utf-8
__author__ = 'shiliang'
__date__ = '2019/3/13 23:23'


import matplotlib.pyplot as plt
from wordcloud import WordCloud # 词云库
import jieba  # 中文分词库

# 1.读取本地中文文本文件
text = open('C:\\Users\\Administrator\\Desktop\\xiaowangzi.txt',encoding='gbk').read()
# 2.使用jieba进行中文分词;cut_all参数表示分词模式,True为全局模式,False为精确模式,默认为False
cut_text = jieba.cut(text, cut_all=False)
result = '/'.join(cut_text) # 因为cut方法返回的是一个生成器,所以要么使用for循环遍历，要么使用join()
# 3.创建WordCloud实例,设置词云图宽高(最终以矩形显示)、背景颜色(默认黑色)和最大显示字数
wc = WordCloud(font_path='C:\\Users\\Administrator\\Desktop\\yahei.ttc', width=600, height=400, background_color="white", max_words=4000)
# 4.根据分词后的中文文本，统计词频，生成词云图
wc.generate(result)
# 5.使用matplotlib绘图
plt.imshow(wc)
plt.axis("off") # 取消坐标系
plt.show()      # 在IDE中显示图片
# 6.将生成的词云图保存在本地
wc.to_file('C:\\Users\\Administrator\\Desktop\\wordcloud.png')
