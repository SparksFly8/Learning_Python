# 中英文词云图

>引言: "**词云**"，又称文字云，是由**词汇**组成**类似云的彩色图形**。可对网络文本中出现**频率较高**的“**关键词**”予以**视觉上的突出**，形成"关键词云层"或"**关键词渲染**"，从而**过滤掉大量的文本信息**，使浏览者只要一眼扫过文本即可领略文本主旨。                                        
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;——摘自百度百科

![在这里插入图片描述](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1552824473304&di=f17a2bb6816ca4cba4ffccffae7d211c&imgtype=0&src=http://5b0988e595225.cdn.sohucs.com/q_70,c_zoom,w_640/images/20180808/54c5b98f04494d57a7ad7e6fe592dbe7.jpeg)
## 本文运行环境与所需包：

 - Python-3.6.6
 - wordcloud(词云库，可直接对英文句子进行分词)
 - jieba(中文分词库)
 - numpy、matplotlib(绘图库)

## 一、简易词云图：
#### ①7行代码英文文本速成词云图
因为`wordcloud`库内置了对**英文文本的分词功能**，所以对于获取的英文文本直接带入`generate()`函数中即可。

这里，我将要处理的英文文本放在了`content.txt`中
```js
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
```
生成**英文词云图**：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190317181702156.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
#### ②9行代码中文文本速成词云图

因为`wordcloud`库**无法对中文文本进行分词**，所以对于获取的中文文本，需要通过**中文分词器**(`jieba`)分词后才能带入`generate()`函数中进行**词频统计**并**生成词云图**。

这里，我将要处理的中文文本(《小王子》前15页，共1w字)放在了`xiaowangzi.txt`中
```js
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
```
**【解释】：**

 1）因为是中文文本，使用open()读取数据时往往不是`Unicode`码，所以编码方案需使用`gbk`，若使用`utf-8`可能会报编码错误；反之，英文文本建议用`utf-8`编码。
 
 2）此处WordCloud中的`font_path`参数是字体文件路径，因为WordCloud中**没有内置相关中文字体**，所以需要我们自己**手动添加**。(此处我用的是**微软雅黑**，中英文字体**获取方式见文章底部**)
 
 3）本例使用`jieba.cut()`方法进行**中文分词**，方法接受三个输入参数:

 1. **需要分词的字符串**；(必填)
 2. **cut_all**参数用来控制是否采用全模式；(选填，默认为**精确模式**，即False)
 3. HMM 参数用来控制是否使用HMM 模型；(选填，默认为False)

生成**中文词云图**如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190317200713793.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
#### 【补充】：

**jieba.cut()用法示例**：

1.因为该方法返回一个**生成器**，所以无法直接打印，可以通过**for循环遍历**或**join()方法**展示：

```js
>>> seg_list = jieba.cut('我来到北京清华大学')
>>> print(seg_list)
<generator object Tokenizer.cut at 0x7f085f445888>
```
for循环遍历:
```js
>>> seg_list = jieba.cut('我来到北京清华大学')
>>> for word in seg_list:
>>>   print(word)
我
来到
北京
清华
清华大学
华大
大学
```
全模式(`cut_all=True`)：
```js
>>> seg_list = jieba.cut('我来到北京清华大学', cut_all=True)
>>> print('全模式: ' + '/'.join(seg_list))  
全模式: 我/来到/北京/清华/清华大学/华大/大学
```
精确模式(`cut_all=False`)：
```js
>>> seg_list = jieba.cut('我来到北京清华大学', cut_all=False)
>>> print('精确模式: ' + '/'.join(seg_list)) 
精确模式: 我/来到/北京/清华大学
```

## 二、自定义优化词云图：
【引出问题1】：在前面两个示例中，我们通过几行代码就实现了一个基本的词云图。但细心的读者可能会发现**小王子**案例中的词云图出现了醒目的`“他们、什么、没有、可是、这样和一个”`类似**没有实际意义**的词语。

【解决方法】：可以使用**中英文停用词(StopWord)**，在**统计词频**的时候**忽略**这些词或标点符号。**英文停用词**在`wordcloud`中就有`STOPWORDS`可以直接使用，而中文停用词需要自己手动添加([中文停用词见笔者整理在GitHub中](https://github.com/SparksFly8/Tools/blob/master/%E4%B8%AD%E6%96%87%E5%81%9C%E7%94%A8%E8%AF%8D%E6%95%B4%E7%90%86%28%E5%90%AB%E6%A0%87%E7%82%B9%E7%AC%A6%E5%8F%B7%E5%92%8C%E6%95%B0%E5%AD%97%29.txt))。

【具体用法】：

**①英文文本-部分代码如下**
```js
from wordcloud import STOPWORDS
//...
stopwords = set(STOPWORDS)  // 用一个集合set存储英文停用词
stopwords.add("said")       // 可在原有停用词基础上自定义增加所需的词语
// 带入到WordCloud实例中的stopwords参数即可。
wc = WordCloud(width=600, height=400, background_color='white',
               max_font_size=45,stopwords=stopwords, max_words=4000)
//...
```
**①中文文本-部分代码如下**
```js
//...
zn_StopWordPath = r'C:\Users\Administrator\Desktop\zn_STOPWORDS.txt'
stopWordList = []
with open(zn_StopWordPath, 'r', encoding='utf-8') as f:
    text = f.read()
    stopWordList = text.split(';\n')
stopwords = set(stopWordList)
stopwords.add('是')
// 带入到WordCloud实例中的stopwords参数即可。
wc = WordCloud(width=600, height=400, background_color='white',
               max_font_size=45,stopwords=stopwords, max_words=4000)
//...
```

【引出问题2】：只生成单一矩形图和固定颜色很单调，可否自定义根据图片背景等其他属性来设置自己的词云图？

【解决方法】：首先在`WordCloud`初始化函数中提供了**25**个参数供用户设置：

```js
def __init__(self, font_path=None, width=400, height=200, margin=2,
                 ranks_only=None, prefer_horizontal=.9, mask=None, scale=1,
                 color_func=None, max_words=200, min_font_size=4,
                 stopwords=None, random_state=None, background_color='black',
                 max_font_size=None, font_step=1, mode="RGB",
                 relative_scaling='auto', regexp=None, collocations=True,
                 colormap=None, normalize_plurals=True, contour_width=0,
                 contour_color='black', repeat=False):
```
这里我们可以使用`Image`和`numpy`来存储图片，使用`mask`参数来引入我们的背景图片，使用`max_words`参数来设置词云图中词数的个数，使用`random_state`参数来设置词在图中的随机形态个数，部分代码如下：

```js
from PIL import Image
import numpy as np
//...
image = np.array(Image.open('C:\\Users\\Administrator\\Desktop\\girl.png'))
wc = WordCloud(mask=image, background_color='white',max_font_size=45,
               stopwords=stopwords, random_state=42,max_words=3000)
//...
```
女孩的图片`girl.png`如下(建议使用**白底**或具有显著鲜明区分的背景图)：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190317232000961.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)

生成的**英文词云图**如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190317232206834.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)

生成的**中文词云图**如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190318114132220.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)

如果想要使用背景图的颜色来填充词语的颜色，则**部分代码**如下：

```js
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import wordcloud, ImageColorGenerator # 图片颜色生成器
//...
image = np.array(Image.open('C:\\Users\\Administrator\\Desktop\\girl.png'))
image_colors = ImageColorGenerator(image)  # 取色
wc = WordCloud(mask=image, background_color='white',max_font_size=45,
               stopwords=stopwords, random_state=42,max_words=3000)
plt.figure("词云图")
plt.imshow(wc.recolor(color_func=image_colors)) # 重置wc实例中的词的颜色
//...
```
生成**英文词云图**如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190317233359460.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)

## 三、完整代码&&总体步骤：
####  3.1 英文词云图生成器完整代码+注释：
```js
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
            plt.imshow(wc.recolor(color_func=image_colors))
        else: # 以图片的形式显示词云,并依据背景色重置词的颜色
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
```
####  3.2 中文词云图生成器完整代码+注释：

```js
import matplotlib.pyplot as plt  # 数学绘图库
import jieba  # 分词库
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  # 词云库
from PIL import Image
import numpy as np

def zn_wordcloudGenerater(filePath, fontPath, imagePath, imageSavePath, zn_STOPWORDS, isImageColor):
    '''
    中文词云图生成器
    :param filePath: 本地文本文件路径
    :param fontPath: 字体文件路径
    :param imagePath: 本地图片(最好是白底)路径
    :param imageSavePath: 词云图保存路径
    :param zn_STOPWORDS: 中文停用词(List类型)
    :param isImageColor: 是否使用背景图片颜色作为词的颜色(bool值)
    '''
    # 使用上下文管理器with读取本地文本文件
    with open(filePath, 'r', encoding='gbk') as f:
        # 1、读入txt文本数据
        text = f.read()
        # 2.使用jieba进行中文分词;cut_all参数表示分词模式,True为全局模式,False为精确模式,默认为False
        cut_text = jieba.cut(text, cut_all=False)
        result = '/'.join(cut_text)
        # 3、设置中文停用词(可通过add方法添加所需中文词汇或标点符号)
        stopwords = set(zn_STOPWORDS)
        stopwords.add('是')
        # 4.1、获取本地背景图片
        image = np.array(Image.open(imagePath))
        if isImageColor:
            # 4.2、获取背景图片颜色
            image_colors = ImageColorGenerator(image)
        # 5、创建WordCloud实例并自定义设置参数(如背景色,背景图片和停用词等)
        wc = WordCloud(font_path=fontPath, background_color='white', max_words=3000,
                       mask=image, stopwords=stopwords, random_state=42, max_font_size=45)
        # 6、根据设置的参数，统计词频并生成词云图
        wc.generate(result)
        # 7、将生成的词云图保存在本地
        plt.figure('词云图')  # 指定所绘图名称
        if isImageColor:
            plt.imshow(wc.recolor(color_func=image_colors))  # 以图片的形式显示词云,并依据背景色重置词的颜色
        else:
            plt.imshow(wc)
        plt.axis('off')      # 关闭图像坐标系
        plt.show()           # 在IDE中显示图片
        wc.to_file(imageSavePath)  # 按照背景图的宽高度保存词云图

def txt2set(zn_StopWordPath):
    '''
    读取本地中文停用词文本并转换为列表
    :param zn_StopWordPath: 中文停用词文本路径
    :return stopWordList: 一个装有中文停用词的列表
    '''
    with open(zn_StopWordPath, 'r', encoding='utf-8') as f:
        text = f.read()
        stopWordList = text.split(';\n')
        return stopWordList

if __name__ == '__main__':    
    # 本地中文文本文件路径
    zn_filePath = 'C:\\Users\\Administrator\\Desktop\\xiaowangzi.txt'
    # 本地中文字体路径
    zn_fontPath = 'C:\\Users\\Administrator\\Desktop\\yahei.ttc'
    # 本地图片(最好是白底)路径
    imagePath = 'C:\\Users\\Administrator\\Desktop\\girl.png'
    # 词云图保存路径
    imageSavePath = 'C:\\Users\\Administrator\\Desktop\\wordcloud.png'
    # 中文停用词文本路径
    zn_StopWordPath = 'C:\\Users\\Administrator\\Desktop\\zn_STOPWORDS.txt'
    # 中文词云图生成器
    zn_StopWordsList = txt2set(zn_StopWordPath)
    zn_wordcloudGenerater(zn_filePath, zn_fontPath, imagePath, imageSavePath, zn_StopWordsList, False)
```

####  3.3 词云图生成总体步骤：

 1. **获取数据**——读取本地文本文件。
 2. **创建词云实例**，并设置好**自定义参数**。
 3. 基于实例和文本数据，**统计词频**并**生成词云图**。
 4. **展现**已生成的**词云图**并**存储**在**本地**。

#### 中英文字体文件获取：
文件后缀为``.ttf``或``.ttc``等。

①本地Windows系统路径：`C:\Windows\Fonts`。

②在线字体库下载：[点击此处](http://font.chinaz.com/zhongwenziti_2.html)。

