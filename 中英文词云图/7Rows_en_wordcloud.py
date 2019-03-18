# encoding:utf-8
__author__ = 'shiliang'
__date__ = '2019/3/13 23:23'


from wordcloud import WordCloud  # 词云库
import matplotlib.pyplot as plt

# 1.读取本地英文文本文件
text = open('C:\\Users\\Administrator\\Desktop\\content.txt',encoding='utf-8').read()
# 2.创建WordCloud实例,设置词云图宽高(最终以矩形显示)、背景颜色(默认黑色)和最大显示字数
wc = WordCloud(width=600, height=400, background_color="white", max_words=4000)
# 3.根据读取的英文文本，先分词再生成词云图
wc.generate(text)
# 4.使用matplotlib绘图
plt.imshow(wc)
plt.axis("off") # 取消坐标系
plt.show()      # 在IDE中显示图片
# 5.将生成的词云图保存在本地
wc.to_file('C:\\Users\\Administrator\\Desktop\\wordcloud.png')