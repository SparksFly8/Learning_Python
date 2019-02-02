from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
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
with open('/home/sparkfly/Desktop/测试文档.doc','rb') as f:
    # 设置附件的MIME和文件名，这里是docx类型
    mimebase = MIMEBase('我的测试文档','docx')
    # 加上必要的头信息
    mimebase.add_header('Content-Disposition', 'attachment', filename='myDocument.docx')
    mimebase.add_header('Content-ID', 'Image')
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
