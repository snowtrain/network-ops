#!/usr/bin/env python3

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()
from devnet2019.models import Smtplogindb


# 发送邮件代码
def smtp_attachment(mailserver, username, password, From, To, Subj, Main_Body, files=None):
    # 使用SSL加密SMTP发送邮件, 此函数发送的邮件有主题,有正文,还可以发送附件
    Tos = To.split(';')  # 把多个邮件接受者通过';'分开
    Date = email.utils.formatdate()  # 格式化邮件时间
    msg = MIMEMultipart()  # 产生MIME多部分的邮件信息
    msg["Subject"] = Subj  # 主题
    msg["From"] = From  # 发件人
    msg["To"] = To  # 收件人
    msg["Date"] = Date  # 发件日期

    part = MIMEText(Main_Body)
    msg.attach(part)  # 添加正文

    if files:  # 如果存在附件文件
        for file in files:  # 逐个读取文件,并添加到附件
            part = MIMEApplication(open(file, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(part)

    server = smtplib.SMTP_SSL(mailserver, 465)  # 连接邮件服务器
    server.login(username, password)  # 通过用户名和密码登录邮件服务器
    failed = server.sendmail(From, Tos, msg.as_string())  # 发送邮件
    server.quit()  # 退出会话
    if failed:
        print('Falied recipients:', failed)  # 如果出现故障，打印故障原因！
    else:
        print('邮件已经成功发出！')  # 如果没有故障发生，打印'邮件已经成功发出！


def alarm_msg(message):
    try:
        smtp_info = Smtplogindb.objects.get(id=1)
        smtp_attachment(smtp_info.mailserver,
                        smtp_info.mailusername,
                        smtp_info.mailpassword,
                        smtp_info.mailfrom,
                        smtp_info.mailto,
                        message,
                        message)
    except Smtplogindb.DoesNotExist:
        pass


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    smtp_attachment('smtp.qq.com',
                    '1204294245@qq.com',
                    'drjidptzianufgfh',
                    '1204294245@qq.com',
                    '545723083@qq.com',
                    '附件测试_主题',
                    '附件测试_正文')
