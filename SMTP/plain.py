from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
# SMTP服务器以及相关配置信息
smtp_sever = 'smtp.163.com'
from_addr = 'xxx@163.com'
password = 'xxxx' # 授权码
to_addr = 'xxx@foxmail.com'

# 1.创建邮件(写好邮件内容、发送人、收件人和标题等)
msg = MIMEText('I Love You','plain','utf-8')
msg['From'] = formataddr(('若水',from_addr)) # 发件人昵称和邮箱
msg['To'] = formataddr(('小伙伴',to_addr))　# 收件人昵称和邮箱
msg['Subject'] = '2019你好'　              # 邮件标题
# 2.登录账号
sever = smtplib.SMTP(smtp_sever,25) # 明文传输端口号是25
sever.login(from_addr,password)
# 3.发送邮件
sever.sendmail(from_addr,to_addr,msg.as_string())
sever.quit()
