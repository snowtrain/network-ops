#!/usr/bin/env python3

from devnet2019.models import Thresholdcpu, Thresholdmem, Thresholdutilization, Smtplogindb, Thresholdsnmp
from devnet2019.forms import Sysconfigthreshold
from django.shortcuts import render
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


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


def threshold_mail(request):
    # html_title = Department.objects.get(name='admin').departtitle.title
    # navbar_list = []
    # for navbar in Navbar.objects.all().order_by('id'):
    #     navbar_list.append([navbar.name, navbar.url])
    # active_navbar = '系统设置'
    # sidebar_list = []
    # for sidebar in Navbar.objects.get(name='系统设置').Sidebar.all().order_by('id'):
    #     sidebar_list.append([sidebar.name, sidebar.url])
    # active_sidebar = '监控阈值与邮件通知'

    if request.method == 'POST':
        form = Sysconfigthreshold(request.POST)
        # 如果表单校验通过，就提取表单内容
        if form.is_valid():
            cpu_threshold = int(request.POST.get('cpu_threshold'))
            cpu_alarm_interval = int(request.POST.get('cpu_alarm_interval'))
            mem_threshold = int(request.POST.get('mem_threshold'))
            mem_alarm_interval = int(request.POST.get('mem_alarm_interval'))
            utilization_threshold = int(request.POST.get('utilization_threshold'))
            utilization_alarm_interval = int(request.POST.get('utilization_alarm_interval'))
            snmp_alarm_interval = int(request.POST.get('snmp_alarm_interval'))
            mailserver = request.POST.get('mailserver')
            mailusername = request.POST.get('mailusername')
            mailpassword = request.POST.get('mailpassword')
            mailfrom = request.POST.get('mailfrom')
            mailto = request.POST.get('mailto')

            # 写入 CPU 告警周期表
            c = Thresholdcpu(id=1,
                             cpu_threshold=cpu_threshold,
                             alarm_interval=cpu_alarm_interval)
            c.save()

            # 写入 MEM 告警周期表
            m = Thresholdmem(id=1,
                             mem_threshold=mem_threshold,
                             alarm_interval=mem_alarm_interval)
            m.save()

            # 写入 接口利用率 告警周期表
            u = Thresholdutilization(id=1,
                                     utilization_threshold=utilization_threshold,
                                     alarm_interval=utilization_alarm_interval)
            u.save()

            # 写入 SNMP 告警周期表
            m = Thresholdsnmp(id=1,
                              alarm_interval=snmp_alarm_interval)
            m.save()

            # 如果邮件部分表单不为空，就从
            if mailserver and mailusername and mailpassword and mailfrom and mailto:
                try:
                    old_smtp = Smtplogindb.objects.get(id=1)
                    if mailserver == old_smtp.mailserver and mailusername == old_smtp.mailusername \
                            and mailpassword == old_smtp.mailpassword and mailfrom == old_smtp.mailfrom \
                            and mailto == old_smtp.mailto:
                        smtp_changed = False
                    else:
                        smtp_changed = True
                        s = Smtplogindb(id=1,
                                        mailserver=mailserver,
                                        mailusername=mailusername,
                                        mailpassword=mailpassword,
                                        mailfrom=mailfrom,
                                        mailto=mailto)
                        s.save()
                except Smtplogindb.DoesNotExist:
                    smtp_changed = True
                    s = Smtplogindb(id=1,
                                    mailserver=mailserver,
                                    mailusername=mailusername,
                                    mailpassword=mailpassword,
                                    mailfrom=mailfrom,
                                    mailto=mailto)
                    s.save()

            cpu_info = Thresholdcpu.objects.get(id=1)
            cpu_threshold = cpu_info.cpu_threshold
            cpu_alarm_interval = cpu_info.alarm_interval
            mem_info = Thresholdmem.objects.get(id=1)
            mem_threshold = mem_info.mem_threshold
            mem_alarm_interval = mem_info.alarm_interval
            utilization_info = Thresholdutilization.objects.get(id=1)
            utilization_threshold = utilization_info.utilization_threshold
            utilization_alarm_interval = utilization_info.alarm_interval

            try:
                smtp_info = Smtplogindb.objects.get(id=1)
                mailserver = smtp_info.mailserver
                mailusername = smtp_info.mailusername
                mailpassword = smtp_info.mailpassword
                mailfrom = smtp_info.mailfrom
                mailto = smtp_info.mailto

            except Smtplogindb.DoesNotExist:
                smtp_info = ''
                mailserver = ''
                mailusername = ''
                mailpassword = ''
                mailfrom = ''
                mailto = ''
            form = Sysconfigthreshold(initial={"cpu_threshold": cpu_threshold,
                                               "cpu_alarm_interval": cpu_alarm_interval,
                                               "mem_threshold": mem_threshold,
                                               "mem_alarm_interval": mem_alarm_interval,
                                               "utilization_threshold": utilization_threshold,
                                               "utilization_alarm_interval": utilization_alarm_interval,
                                               "mailserver": mailserver,
                                               "mailusername": mailusername,
                                               "mailpassword": mailpassword,
                                               "mailfrom": mailfrom,
                                               "mailto": mailto})
            if not smtp_info:
                successmessage = '监控阈值设置完成!'
            else:
                if smtp_changed:
                    try:
                        smtp_attachment(mailserver,
                                        mailusername,
                                        mailpassword,
                                        mailfrom,
                                        mailto,
                                        'Devnet2019测试邮件!',
                                        'Devnet2019测试邮件!')
                        successmessage = '监控阈值设置完成! 并发送了测试邮件, 请确认能收到测试邮件!'
                    except Exception:
                        errormessage = '监控阈值设置完成! 但是邮件发送失败! 请确认邮件设置时候正确'
                else:
                    successmessage = '监控阈值设置完成!'

            return render(request, 'devnet_system_setting_threshold_mail.html', locals())
        else:
            return render(request, 'devnet_system_setting_threshold_mail.html', locals())

    # 初始界面
    else:
        # 尝试从数据库中取出默认 CPU 告警阈值，如果没有取到，就置空
        try:
            cpu_info = Thresholdcpu.objects.get(id=1)
            cpu_threshold = cpu_info.cpu_threshold
            cpu_alarm_interval = cpu_info.alarm_interval
        except Thresholdcpu.DoesNotExist:
            c = Thresholdcpu(id=1)
            c.save()
            cpu_info = Thresholdcpu.objects.get(id=1)
            cpu_threshold = cpu_info.cpu_threshold
            cpu_alarm_interval = cpu_info.alarm_interval

        # 尝试从数据库中取出默认 MEM 告警阈值，如果没有取到，就置空
        try:
            mem_info = Thresholdmem.objects.get(id=1)
            mem_threshold = mem_info.mem_threshold
            mem_alarm_interval = mem_info.alarm_interval
        except Thresholdmem.DoesNotExist:
            m = Thresholdmem(id=1)
            m.save()
            mem_info = Thresholdmem.objects.get(id=1)
            mem_threshold = mem_info.mem_threshold
            mem_alarm_interval = mem_info.alarm_interval

        # 尝试从数据库中取出默认 接口利用率 告警阈值，如果没有取到，就置空
        try:
            utilization_info = Thresholdutilization.objects.get(id=1)
            utilization_threshold = utilization_info.utilization_threshold
            utilization_alarm_interval = utilization_info.alarm_interval
        except Thresholdutilization.DoesNotExist:
            t = Thresholdutilization(id=1)
            t.save()
            utilization_info = Thresholdutilization.objects.get(id=1)
            utilization_threshold = utilization_info.utilization_threshold
            utilization_alarm_interval = utilization_info.alarm_interval

        # 尝试从数据库中取出默认SNMP告警周期，如果没有取到，就置空
        try:
            snmp_info = Thresholdsnmp.objects.get(id=1)
            snmp_alarm_interval = snmp_info.alarm_interval
        except Thresholdsnmp.DoesNotExist:
            m = Thresholdsnmp(id=1)
            m.save()
            snmp_info = Thresholdsnmp.objects.get(id=1)
            snmp_alarm_interval = snmp_info.alarm_interval

        # 尝试从数据库中取出默认 mail 信息，如果没有取到，就置空
        try:
            smtp_info = Smtplogindb.objects.get(id=1)
            mailserver = smtp_info.mailserver
            mailusername = smtp_info.mailusername
            mailpassword = smtp_info.mailpassword
            mailfrom = smtp_info.mailfrom
            mailto = smtp_info.mailto

        except Smtplogindb.DoesNotExist:
            smtp_info = ''
            mailserver = ''
            mailusername = ''
            mailpassword = ''
            mailfrom = ''
            mailto = ''
        form = Sysconfigthreshold(initial={"cpu_threshold": cpu_threshold,
                                           "cpu_alarm_interval": cpu_alarm_interval,
                                           "mem_threshold": mem_threshold,
                                           "mem_alarm_interval": mem_alarm_interval,
                                           "utilization_threshold": utilization_threshold,
                                           "utilization_alarm_interval": utilization_alarm_interval,
                                           "snmp_alarm_interval": snmp_alarm_interval,
                                           "mailserver": mailserver,
                                           "mailusername": mailusername,
                                           "mailpassword": mailpassword,
                                           "mailfrom": mailfrom,
                                           "mailto": mailto})

        return render(request, 'devnet_system_setting_threshold_mail.html', locals())


def reset_threshold_mail(request):
    # html_title = Department.objects.get(name='admin').departtitle.title
    # navbar_list = []
    # for navbar in Navbar.objects.all().order_by('id'):
    #     navbar_list.append([navbar.name, navbar.url])
    # active_navbar = '系统设置'
    # sidebar_list = []
    # for sidebar in Navbar.objects.get(name='系统设置').Sidebar.all().order_by('id'):
    #     sidebar_list.append([sidebar.name, sidebar.url])
    # active_sidebar = '监控阈值与邮件通知'

    try:
        cpu_info = Thresholdcpu.objects.get(id=1)
        cpu_info.delete()
    except Thresholdcpu.DoesNotExist:
        pass
    c = Thresholdcpu(id=1)
    c.save()
    cpu_threshold = c.cpu_threshold
    cpu_alarm_interval = c.alarm_interval

    try:
        mem_info = Thresholdmem.objects.get(id=1)
        mem_info.delete()
    except Thresholdmem.DoesNotExist:
        pass
    m = Thresholdmem(id=1)
    m.save()
    mem_threshold = m.mem_threshold
    mem_alarm_interval = m.alarm_interval

    try:
        utilization_info = Thresholdutilization.objects.get(id=1)
        utilization_info.delete()
    except Thresholdutilization.DoesNotExist:
        pass
    t = Thresholdutilization(id=1)
    t.save()
    utilization_threshold = t.utilization_threshold
    utilization_alarm_interval = t.alarm_interval

    try:
        smtp_info = Smtplogindb.objects.get(id=1)
        smtp_info.delete()
    except Smtplogindb.DoesNotExist:
        pass
    smtp_info = ''
    mailserver = ''
    mailusername = ''
    mailpassword = ''
    mailfrom = ''
    mailto = ''

    successmessage = '重置监控阈值与邮件信息到默认成功'
    form = Sysconfigthreshold(initial={"cpu_threshold": cpu_threshold,
                                       "cpu_alarm_interval": cpu_alarm_interval,
                                       "mem_threshold": mem_threshold,
                                       "mem_alarm_interval": mem_alarm_interval,
                                       "utilization_threshold": utilization_threshold,
                                       "utilization_alarm_interval": utilization_alarm_interval,
                                       "mailserver": mailserver,
                                       "mailusername": mailusername,
                                       "mailpassword": mailpassword,
                                       "mailfrom": mailfrom,
                                       "mailto": mailto})

    return render(request, 'devnet_system_setting_threshold_mail.html', locals())
