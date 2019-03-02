# Python使用SMTP协议实现邮件发送(含明文/SSL加密/TLS加密)
> SMTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件。
Python对SMTP支持有`smtplib`和`email`两个模块

 1. `email`负责**构造邮件** 
 2. `smtplib`负责**发送邮件**
## Tips
欲看完整代码请见[我的GitHub](https://github.com/SparksFly8/Learning_Python/tree/master/SMTP).
## 一、基本环境设置
以下笔者测试使用163邮箱给foxmail邮箱发邮件，所以需要手动对发送方邮箱配置SMTP协议，其余邮箱操作同理。
首先，登录到163邮箱，然后在设置菜单中点击如下选项。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019011217254360.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)

然后，手动开启SMTP服务，此时可能需要设置客户端授权码，即为**登录第三方邮件客户端的专用口令**，和该邮箱登录密码不同，对于163邮箱可以自己设置授权码，但如果是QQ或者foxmail邮箱会有系统自动分配给用户授权码。
![１１１](https://img-blog.csdnimg.cn/20190112172626215.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
因为发送方是163邮箱，所以此时用到的SMTP服务器是`smtp.163.com`，在163邮箱设置可看到如下图所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190112173305473.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)

对于其他邮箱相应的SMTP服务器是`smtp.xxx.com`，比如以下是**常用邮箱SMTP端口及登录说明**(亲测可用)：


| 邮箱 | SMTP服务器 |登录口令 | 支持加密方式 | 对应端口号 |
|--|--|--|--|--|--|
| 163  | smtp.163.com |个人设置授权码 | 明文\SSL加密 | 25\465 | 
| 126  | smtp.126.com | 个人设置授权码 | 明文\SSL加密 | 25\465 |
| QQ  | smtp.qq.com | 系统分配授权码 | 明文\SSL加密\TLS加密 | 25\465\587 |
| Gmail  |smtp.gmail.com | 邮箱登录密码 | TLS加密 | 587 |



## 二、实现文本邮件发送
我们以下先来实现一下简单的文本邮件的发送代码。**其中`plain`表示纯文本内容。**
```js
msg = MIMEText('I Love You','plain','utf-8')
```

```js
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
# SMTP服务器以及相关配置信息
smtp_sever = 'smtp.163.com'
from_addr = 'xxx@163.com'
password = 'xxxx'  # 授权码
to_addr = 'xxx@foxmail.com'

# 1.创建邮件(写好邮件内容、发送人、收件人和标题等)
msg = MIMEText('I Love You','plain','utf-8')
msg['From'] = formataddr(('若水',from_addr)) # 发件人昵称和邮箱
msg['To'] = formataddr(('小伙伴',to_addr))　# 收件人昵称和邮箱
msg['Subject'] = '2019你好'　              # 邮件标题
# 2.登录账号
sever = smtplib.SMTP(smtp_sever,25)　# 明文传输端口号是25
sever.login(from_addr,password)
# 3.发送邮件
sever.sendmail(from_addr,to_addr,msg.as_string())
sever.quit()
```
**【注意事项】：**

**1）上面代码中发送方是163邮箱，所以密码不是邮箱的登录密码，而是手动开启SMTP协议后设置或分配的`授权码`！**，但如果是Gmail则使用的密码是**登录密码**。

2）如果没有加入如下代码，则会被识别为**垃圾邮件**，故出现错误代码是`554`的`smtplib.SMTPDataError`错误。[点击查看邮件退信代码说明](http://help.163.com/09/1224/17/5RAJ4LMH00753VB8.html)
```js
msg['From'] = formataddr(('若水',from_addr))
msg['To'] = formataddr(('小伙伴',to_addr))
msg['Subject'] = '2019你好'
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190112175041822.png)
**3）如果是群发邮件，则需要发送到多个邮箱，则`sever.sendmail`中的`to_addr`可以是存储多个邮箱的列表。**
4）`msg['To']`接收的是**字符串**而不是list，如果有多个邮件地址，用`,`分隔即可
5）以上代码最好在本机的IDE(如Pytharm)中运行，笔者同样在Pycharm运行成功的邮件发送代码，在Jupyter中运行却屡屡报`SMTPDataError`错，如有大佬知道原因还请不吝赐教。

若一切顺利，则可在QQ邮箱上看到该邮件(往往在垃圾箱中)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190113125624419.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
## 三、发送HTML邮件
只需要把上面发送纯文本代码中的`MIMEText`中的`plain`换成`html`即可，然后再把html文本粘贴在前面，代码如下:
```js
msg = MIMEText('<html><body>'
               '<h1>2019请关注我的博客</h1>'
               '<p>我的博客地址是：'
               '<a href="https://blog.csdn.net/sl_world">sl_world</a>...'
               '</p></body></html>','html','utf-8')
```
运行成功可以在收件箱看到如下图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190113125448986.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
## 四、发送带附件的邮件
如果我们想要发送带附件的邮件，先来分析一下带附件邮件的组成，很容易得到

 - **邮件内容＝邮件正文＋邮件附件**

所以此处我们可以使用`MIMEMultipart`创建实例，然后通过把`邮件正文`和`邮件附件`分别添加(attach)到里面即可，因为`MIMEBase`可以表示任何对象，所以此处使用它存储邮件附件。此处我使用的附件路径是`/home/sparkfly/Desktop/测试文档.doc`
 - **MIMEMultipart**
    - **MIMEText－邮件正文**
    - **MIMEBase－邮件附件**

代码如下：
```js
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formataddr
import smtplib
# SMTP服务器以及相关配置信息
smtp_sever = 'smtp.163.com'
from_addr = 'xxx@163.com'
password = 'xxx'　　# 授权码
to_addr = 'xxx@foxmail.com'
# 创建MIMEMultipart实例，通过attach方法把MIMEText和MIMEBase添加进去
msg = MIMEMultipart()
msg['From'] = formataddr(('若水',from_addr))
msg['To'] = formataddr(('小伙伴',to_addr))
msg['Subject'] = 'Welcome to 2019'
# 添加邮件正文MIMEText
msg.attach(MIMEText('附件如下','plain','utf-8'))
# 添加附件就是加上一个MIMEBase，从本地读取一个word文档
with open('/home/sparkfly/Desktop/测试文档.doc','rb') as f:
    # 设置附件的MIME和文件名，这里是docx类型
    mimebase = MIMEBase('我的测试文档','docx')
    # 加上必要的头信息
    mimebase.add_header('Content-Disposition', 'attachment', filename='myDocument.docx')
    mimebase.add_header('Content-ID', '<0>')
    mimebase.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来
    mimebase.set_payload(f.read())
    # 用Base64编码
    encoders.encode_base64(mimebase)
    # 添加到MIMEMultipart中
    msg.attach(mimebase)

server = smtplib.SMTP(smtp_sever,25)
server.set_debuglevel(1)　 # 查看实时登录日志信息
server.login(from_addr,password)
server.sendmail(from_addr,to_addr,msg.as_string())
server.quit()
```
其中`server.set_debuglevel(1)`可以查看实时登录日志信息，方便debug。
运行结果如下，OK!
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190113154555823.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
## 五、将图片嵌入到邮件正文
#### 【方法一】:
首先还是和上一步一样，把图片当做附件添加到`MIMEMultipart`实例中，然后在`MIMEText`中把`plain`改成`html`，使用`<img>`html单标签和属性`src="cid:Image"`把附件中的图片引入到邮件正文中，若有多个图片，给它们依次编号，然后引用不同的`cid:x`即可。此处代码仅在上一步中修改**读取本地图片的文件路径等相关信息**和如下代码即可。

```js
msg.attach(MIMEText('<html><body><h1>2019请关注我的博客</h1>'
                    '<p><img src="cid:Image"></p>'
                    '</body></html>','html','utf-8'))
```
并且修改`Content-ID`参数对应为`Image`
```js
mimebase.add_header('Content-ID', 'Image')
```
#### 【方法二】:
在方法一的基础上，直接使用`MIMEImage`对象处理图片文件，替换`MIMEBase`对象，仅三行代码ok。
修改部分代码如下：

```js
from email.mime.image import MIMEImage
...
with open('/home/sparkfly/Desktop/image.png','rb') as f:
    mimeImage = MIMEImage(f.read())
    mimeImage.add_header('Content-ID', 'Image')
    msg.attach(mimeImage)
...
```
成功后收到邮件如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190113164741119.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
## 六、额外补充
#### １．同时支持纯文本和HTML格式邮件查看
对于查看不了HTML格式邮件的情况，我们可以同时编写一份纯文本`plain`格式的内容，然后给收件人可选去读取。
还是以上面的的代码为例子，此处在加入邮件正文`MIMEText`的时候，加入两次，一次是`html`格式的，一次是`plain`纯文本格式的。之后在`MIMEMultipart`中加入`alternative`参数表示二选一。修改部分代码如下：
```js
msg = MIMEMultipart('alternative')
msg.attach(MIMEText('2019请关注我的博客', 'plain', 'utf-8'))
msg.attach(MIMEText('<html><body><h1>2019请关注我的博客</h1>'
                    '<p><img src="cid:0"></p>'
                    '</body></html>','html','utf-8'))
```
成功后收到邮件如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190113164653985.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
点击`纯文本`显示如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190113164841406.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)
#### ２．常用邮箱SMTP加密方式
使用上述SMTP协议发送邮件实则发送的是明文邮件，如果想要加密，有如下几种方式。
**1）明文传输:**　端口号是`25`。
```js
server = smtplib.SMTP(smtp_sever,25)
```
**2）SSL加密:** 端口号是`465`，通信过程加密，邮件数据安全。
```js
server = smtplib.SMTP_SSL(smtp_sever,465)
```
**3）TLS加密:** 端口号是`587`，通信过程加密，邮件数据安全，使用正常的smtp端口。对于TLS加密方式需要先建立**SSL连接**，然后再发送邮件。**此处使用`starttls()`来建立安全连接**
```js
server = smtplib.SMTP(smtp_sever,587)
server.starttls()
```
不同邮箱支持不同的加密协议，常用邮箱支持的**加密方式**和对应**端口号**如下：


|邮箱| SMTP服务器 |端口号 |支持加密方式 |
|--|--|--|--|--|
|163  | smtp.163.com |25/465 |明文/SSL加密|
|126  | smtp.126.com |25/465 |明文/SSL加密|
|QQ  | smtp.qq.com |25/465/587 |明文/SSL加密/TLS加密|
|Gmail  |smtp.gmail.com |587 |TLS加密|


#### ３．登录gmail常见问题
笔者以上都用的是`163`邮箱作为发送方，如果使用`gmail`作为发送方，除了SMTP服务器要改成`smtp.gmail.com`外，还需要把端口改成`587`，密码直接使用gmail的登录密码即可。但依然**可能会登录失败**。原因是目前**gmail对安全性较低的应用的访问权限进行控制**，我们需要手动设置。[点击进行Gmail安全性较低的应用的访问权限设置](https://myaccount.google.com/lesssecureapps?utm_source=google-account&utm_medium=web)，点击界面如下，设置启用即可。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190113182026504.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NMX1dvcmxk,size_16,color_FFFFFF,t_70)

【我的博客对应地址】：https://blog.csdn.net/SL_World/article/details/86368760
