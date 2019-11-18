#!/usr/bin/env python3

from devnet2019.models import DataBaseLifetime
from devnet2019.forms import SysconfigdatabaselifetimeForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def database_lifetime(request):
    if request.method == 'POST':
        form = SysconfigdatabaselifetimeForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把客户提交的监控周期写入数据库
        if form.is_valid():
            reachable_lifetime = request.POST.get('reachable_lifetime')
            cpu_lifetime = request.POST.get('cpu_lifetime')
            mem_lifetime = request.POST.get('mem_lifetime')
            interface_lifetime = request.POST.get('interface_lifetime')
            netflow_lifetime = request.POST.get('netflow_lifetime')

            reachable_lifetime_result = DataBaseLifetime.objects.get(name='reachable_lifetime')
            reachable_lifetime_result.lifetime = reachable_lifetime
            reachable_lifetime_result.save()
            cpu_lifetime_result = DataBaseLifetime.objects.get(name='cpu_lifetime')
            cpu_lifetime_result.lifetime = cpu_lifetime
            cpu_lifetime_result.save()
            mem_lifetime_result = DataBaseLifetime.objects.get(name='mem_lifetime')
            mem_lifetime_result.lifetime = mem_lifetime
            mem_lifetime_result.save()
            interface_lifetime_result = DataBaseLifetime.objects.get(name='interface_lifetime')
            interface_lifetime_result.lifetime = interface_lifetime
            interface_lifetime_result.save()
            netflow_lifetime_result = DataBaseLifetime.objects.get(name='netflow_lifetime')
            netflow_lifetime_result.lifetime = netflow_lifetime
            netflow_lifetime_result.save()

            reachable_lifetime_changed = DataBaseLifetime.objects.get(name='reachable_lifetime').lifetime
            cpu_lifetime_changed = DataBaseLifetime.objects.get(name='cpu_lifetime').lifetime
            mem_lifetime_changed = DataBaseLifetime.objects.get(name='mem_lifetime').lifetime
            interface_lifetime_changed = DataBaseLifetime.objects.get(name='interface_lifetime').lifetime
            netflow_lifetime_changed = DataBaseLifetime.objects.get(name='netflow_lifetime').lifetime

            form = SysconfigdatabaselifetimeForm(initial={'reachable_lifetime': reachable_lifetime_changed,  # initial填写初始值
                                                          'cpu_lifetime': cpu_lifetime_changed,
                                                          'mem_lifetime': mem_lifetime_changed,
                                                          'interface_lifetime': interface_lifetime_changed,
                                                          'netflow_lifetime': netflow_lifetime_changed})
            successmessage = '数据库老化时间修改成功!'
            # 返回'sysconfig_monitor_interval.html'页面,与表单给客户
            return render(request, 'devnet_system_setting_database_lifetime.html', locals())
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'devnet_system_setting_database_lifetime.html', locals())
    else:  # 如果不是POST,就是GET,表示为初始访问, 把监控周期在数据库中的值,通过初始值的方式展现给客户看
        try:
            reachable_lifetime = DataBaseLifetime.objects.get(name='reachable_lifetime').lifetime
        except DataBaseLifetime.DoesNotExist:
            reachable_lifetime = 24
            r = DataBaseLifetime(name='reachable_lifetime', lifetime=reachable_lifetime)
            r.save()
        try:
            cpu_lifetime = DataBaseLifetime.objects.get(name='cpu_lifetime').lifetime
        except DataBaseLifetime.DoesNotExist:
            cpu_lifetime = 24
            c = DataBaseLifetime(name='cpu_lifetime', lifetime=cpu_lifetime)
            c.save()
        try:
            mem_lifetime = DataBaseLifetime.objects.get(name='mem_lifetime').lifetime
        except DataBaseLifetime.DoesNotExist:
            mem_lifetime = 24
            m = DataBaseLifetime(name='mem_lifetime', lifetime=mem_lifetime)
            m.save()
        try:
            interface_lifetime = DataBaseLifetime.objects.get(name='interface_lifetime').lifetime
        except DataBaseLifetime.DoesNotExist:
            interface_lifetime = 24
            i = DataBaseLifetime(name='interface_lifetime', lifetime=interface_lifetime)
            i.save()
        try:
            netflow_lifetime = DataBaseLifetime.objects.get(name='netflow_lifetime').lifetime
        except DataBaseLifetime.DoesNotExist:
            netflow_lifetime = 24
            n = DataBaseLifetime(name='netflow_lifetime', lifetime=netflow_lifetime)
            n.save()

        form = SysconfigdatabaselifetimeForm(initial={'reachable_lifetime': reachable_lifetime,  # initial填写初始值
                                                      'cpu_lifetime': cpu_lifetime,
                                                      'mem_lifetime': mem_lifetime,
                                                      'interface_lifetime': interface_lifetime,
                                                      'netflow_lifetime': netflow_lifetime})
        # 返回'sysconfig_monitor_interval.html'页面,与表单给客户
        return render(request, 'devnet_system_setting_database_lifetime.html', locals())


@login_required
def reset_database_lifetime(request):

    if request.method == 'POST':  # 如果收到客户重置监控周期的POST请求
        if request.user.has_perm('devnet2019.change_databaselifetime'):
            reachable_lifetime_result = DataBaseLifetime.objects.get(name='reachable_lifetime')
            reachable_lifetime_result.lifetime = 24
            reachable_lifetime_result.save()
            cpu_lifetime_result = DataBaseLifetime.objects.get(name='cpu_lifetime')
            cpu_lifetime_result.lifetime = 24
            cpu_lifetime_result.save()
            mem_lifetime_result = DataBaseLifetime.objects.get(name='mem_lifetime')
            mem_lifetime_result.lifetime = 24
            mem_lifetime_result.save()
            interface_lifetime_result = DataBaseLifetime.objects.get(name='interface_lifetime')
            interface_lifetime_result.lifetime = 24
            interface_lifetime_result.save()
            netflow_lifetime_result = DataBaseLifetime.objects.get(name='netflow_lifetime')
            netflow_lifetime_result.lifetime = 24
            netflow_lifetime_result.save()

            reachable_lifetime_changed = DataBaseLifetime.objects.get(name='reachable_lifetime').lifetime
            cpu_lifetime_changed = DataBaseLifetime.objects.get(name='cpu_lifetime').lifetime
            mem_lifetime_changed = DataBaseLifetime.objects.get(name='mem_lifetime').lifetime
            interface_lifetime_changed = DataBaseLifetime.objects.get(name='interface_lifetime').lifetime
            netflow_lifetime_changed = DataBaseLifetime.objects.get(name='netflow_lifetime').lifetime

            form = SysconfigdatabaselifetimeForm(initial={'reachable_lifetime': reachable_lifetime_changed,  # initial填写初始值
                                                          'cpu_lifetime': cpu_lifetime_changed,
                                                          'mem_lifetime': mem_lifetime_changed,
                                                          'interface_lifetime': interface_lifetime_changed,
                                                          'netflow_lifetime': netflow_lifetime_changed})
        else:
            err = '没有权限'
            return render(request, '404.html', locals())
        successmessage = '重置系统数据库老化时间到默认成功!'
        # 返回'sysconfig_monitor_interval.html'页面,与表单
        return render(request, 'devnet_system_setting_database_lifetime.html', locals())

    else:
        return HttpResponseRedirect('/system_setting/database_lifetime')
