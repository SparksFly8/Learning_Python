from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
# SMTP服务器以及相关配置信息
smtp_sever = 'smtp.163.com'
from_addr = 'xxx@163.com'
password = 'xxx' # 授权码
to_addr = 'xxx@foxmail.com'
# 创建MIMEMultipart实例，通过attach方法把MIMEText和MIMEBase添加进去
msg = MIMEMultipart()
msg['From'] = formataddr(('若水',from_addr))
msg['To'] = formataddr(('小伙伴',to_addr))
msg['Subject'] = 'Welcome to 2019'
# 向邮件正文嵌入图片
msg.attach(MIMEText('<html><body><h1>2019请关注我的博客</h1>'
                    '<p><img src="cid:Image"></p>'
                    '</body></html>','html','utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个word文档
with open('/home/sparkfly/Desktop/image.png','rb') as f:
    mimeImage = MIMEImage(f.read())
    mimeImage.add_header('Content-ID', 'Image')
    msg.attach(mimeImage)

server = smtplib.SMTP(smtp_sever,25)
server.set_debuglevel(1) # 查看实时登录日志信息
server.login(from_addr,password)
server.sendmail(from_addr,to_addr,msg.as_string())
server.quit()
