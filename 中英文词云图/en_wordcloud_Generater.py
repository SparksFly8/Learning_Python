# encoding:utf-8
__author__ = 'shiliang'
__date__ = '2019/3/13 23:23'


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  # 词云库
from PIL import Image
import matplotlib.pyplot as plt  # 数学绘图库
import numpy as np


def en_wordcloudGenerater(filePath, imagePath, imageSavePath, isImageColor):
    '''
    英文词云图生成器
    :param filePath: 本地文本文件路径
    :param imagePath: 本地图片(最好是白底)路径
    :param imageSavePath: 词云图保存路径
    :param isImageColor: 是否使用背景图片颜色作为词的颜色(bool值)
    '''
    # 使用上下文管理器with读取本地文本文件
    with open(filePath, 'r', encoding='utf-8') as f:
        # 1、读入txt文本数据
        text = f.read()
        # 2、设置停用词(可通过add方法添加所需英文词汇或标点符号)
        stopwords = set(STOPWORDS)
        stopwords.add('said')
        # 3.1、获取本地背景图片
        image = np.array(Image.open(imagePath))
        if isImageColor:
            # 3.2、获取背景图片颜色
            image_colors = ImageColorGenerator(image)
        # 4、创建WordCloud实例并自定义设置参数(如背景色,背景图片和停用词等)
        wc = WordCloud(mask=image, background_color='white', max_font_size=45,
                       stopwords=stopwords, random_state=42, max_words=3000)
        # 5、根据设置的参数，统计词频并生成词云图
        wc.generate(text)
        # 6.将生成的词云图保存在本地
        plt.figure('词云图')  # 指定所绘图名称
        if isImageColor:
            plt.imshow(wc.recolor(color_func=image_colors))  # 以图片的形式显示词云,并依据背景色重置词的颜色
        else:
            plt.imshow(wc)
        plt.axis('off')      # 关闭图像坐标系
        plt.show()           # 在IDE中显示图片
        wc.to_file(imageSavePath)  # 按照背景图的宽高度保存词云图


if __name__ == '__main__':
    # 本地文本文件路径
    filePath = 'C:\\Users\\Administrator\\Desktop\\content.txt'
    # 本地图片(最好是白底)路径
    imagePath = 'C:\\Users\\Administrator\\Desktop\\girl.png'
    # 词云图保存路径
    imageSavePath = 'C:\\Users\\Administrator\\Desktop\\wordcloud.png'
    en_wordcloudGenerater(filePath, imagePath, imageSavePath, False)