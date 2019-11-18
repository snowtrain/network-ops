#!/usr/bin/env python3

from devnet2019.models import MonitorInterval
from devnet2019.forms import SysconfigmonitorintervalForm
from django.shortcuts import render
from django.http import HttpResponseRedirect


def monitor_interval(request):
    if request.method == 'POST':
        form = SysconfigmonitorintervalForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把客户提交的监控周期写入数据库
        if form.is_valid():
            cpu_interval = request.POST.get('cpu_interval')
            cpu_max_interval = request.POST.get('cpu_max_interval')
            mem_interval = request.POST.get('mem_interval')
            mem_max_interval = request.POST.get('mem_max_interval')
            speed_interval = request.POST.get('speed_interval')
            utilization_interval = request.POST.get('utilization_interval')

            cpu_interval_result = MonitorInterval.objects.get(name='cpu_interval')
            cpu_interval_result.interval = cpu_interval
            cpu_interval_result.save()
            cpu_max_interval_result = MonitorInterval.objects.get(name='cpu_max_interval')
            cpu_max_interval_result.interval = cpu_max_interval
            cpu_max_interval_result.save()
            mem_interval_result = MonitorInterval.objects.get(name='mem_interval')
            mem_interval_result.interval = mem_interval
            mem_interval_result.save()
            mem_max_interval_result = MonitorInterval.objects.get(name='mem_max_interval')
            mem_max_interval_result.interval = mem_max_interval
            mem_max_interval_result.save()
            speed_interval_result = MonitorInterval.objects.get(name='speed_interval')
            speed_interval_result.interval = speed_interval
            speed_interval_result.save()
            utilization_interval_result = MonitorInterval.objects.get(name='utilization_interval')
            utilization_interval_result.interval = utilization_interval
            utilization_interval_result.save()

            cpu_interval_changed = MonitorInterval.objects.get(name='cpu_interval').interval
            cpu_max_interval_changed = MonitorInterval.objects.get(name='cpu_max_interval').interval
            mem_interval_changed = MonitorInterval.objects.get(name='mem_interval').interval
            mem_max_interval_changed = MonitorInterval.objects.get(name='mem_max_interval').interval
            speed_interval_changed = MonitorInterval.objects.get(name='speed_interval').interval
            utilization_interval_changed = MonitorInterval.objects.get(name='utilization_interval').interval

            form = SysconfigmonitorintervalForm(initial={'cpu_interval': cpu_interval_changed,  # initial填写初始值
                                                         'cpu_max_interval': cpu_max_interval_changed,
                                                         'mem_interval': mem_interval_changed,
                                                         'mem_max_interval': mem_max_interval_changed,
                                                         'speed_interval': speed_interval_changed,
                                                         'utilization_interval': utilization_interval_changed})
            successmessage = '系统监控周期修改成功!'
            # 返回'sysconfig_monitor_interval.html'页面,与表单给客户
            return render(request, 'devnet_system_setting_monitor_interval.html', locals())
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'devnet_system_setting_monitor_interval.html', locals())

    # 如果不是POST,就是GET,表示为初始访问, 把监控周期在数据库中的值,通过初始值的方式展现
    else:
        try:
            cpu_interval = MonitorInterval.objects.get(name='cpu_interval').interval
        except MonitorInterval.DoesNotExist:
            cpu_interval = 1
            c = MonitorInterval(name='cpu_interval', interval=cpu_interval)
            c.save()

        try:
            cpu_max_interval = MonitorInterval.objects.get(name='cpu_max_interval').interval
        except MonitorInterval.DoesNotExist:
            cpu_max_interval = 1
            cm = MonitorInterval(name='cpu_max_interval', interval=cpu_max_interval)
            cm.save()

        try:
            mem_interval = MonitorInterval.objects.get(name='mem_interval').interval
        except MonitorInterval.DoesNotExist:
            mem_interval = 1
            m = MonitorInterval(name='mem_interval', interval=mem_interval)
            m.save()

        try:
            mem_max_interval = MonitorInterval.objects.get(name='mem_max_interval').interval
        except MonitorInterval.DoesNotExist:
            mem_max_interval = 1
            mm = MonitorInterval(name='mem_max_interval', interval=mem_max_interval)
            mm.save()

        try:
            speed_interval = MonitorInterval.objects.get(name='speed_interval').interval
        except MonitorInterval.DoesNotExist:
            speed_interval = 1
            s = MonitorInterval(name='speed_interval', interval=speed_interval)
            s.save()

        try:
            utilization_interval = MonitorInterval.objects.get(name='utilization_interval').interval
        except MonitorInterval.DoesNotExist:
            utilization_interval = 1
            u = MonitorInterval(name='utilization_interval', interval=utilization_interval)
            u.save()

        form = SysconfigmonitorintervalForm(initial={'cpu_interval': cpu_interval,  # initial填写初始值
                                                     'cpu_max_interval': cpu_max_interval,
                                                     'mem_interval': mem_interval,
                                                     'mem_max_interval': mem_max_interval,
                                                     'speed_interval': speed_interval,
                                                     'utilization_interval': utilization_interval})

        # 返回'sysconfig_monitor_interval.html'页面,与表单给客户
        return render(request, 'devnet_system_setting_monitor_interval.html', locals())


def reset_monitor_interval(request):
    if request.method == 'POST':  # 如果收到客户重置监控周期的POST请求
        cpu_interval_result = MonitorInterval.objects.get(name='cpu_interval')
        cpu_interval_result.interval = 1
        cpu_interval_result.save()
        cpu_max_interval_result = MonitorInterval.objects.get(name='cpu_max_interval')
        cpu_max_interval_result.interval = 1
        cpu_max_interval_result.save()
        mem_interval_result = MonitorInterval.objects.get(name='mem_interval')
        mem_interval_result.interval = 1
        mem_interval_result.save()
        mem_max_interval_result = MonitorInterval.objects.get(name='mem_max_interval')
        mem_max_interval_result.interval = 1
        mem_max_interval_result.save()
        speed_interval_result = MonitorInterval.objects.get(name='speed_interval')
        speed_interval_result.interval = 1
        speed_interval_result.save()
        utilization_interval_result = MonitorInterval.objects.get(name='utilization_interval')
        utilization_interval_result.interval = 1
        utilization_interval_result.save()

        cpu_interval_changed = MonitorInterval.objects.get(name='cpu_interval').interval
        cpu_max_interval_changed = MonitorInterval.objects.get(name='cpu_max_interval').interval
        mem_interval_changed = MonitorInterval.objects.get(name='mem_interval').interval
        mem_max_interval_changed = MonitorInterval.objects.get(name='mem_max_interval').interval
        speed_interval_changed = MonitorInterval.objects.get(name='speed_interval').interval
        utilization_interval_changed = MonitorInterval.objects.get(name='utilization_interval').interval

        form = SysconfigmonitorintervalForm(initial={'cpu_interval': cpu_interval_changed,  # initial填写初始值
                                                     'cpu_max_interval': cpu_max_interval_changed,
                                                     'mem_interval': mem_interval_changed,
                                                     'mem_max_interval': mem_max_interval_changed,
                                                     'speed_interval': speed_interval_changed,
                                                     'utilization_interval': utilization_interval_changed})
        successmessage = '重置系统监控周期到默认成功!'
        # 返回'sysconfig_monitor_interval.html'页面,与表单给客户
        return render(request, 'devnet_system_setting_monitor_interval.html', locals())

    else:
        return HttpResponseRedirect('/system_setting/monitor_interval')
