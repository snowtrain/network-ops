#!/usr/bin/env python3

from devnet2019.models import Devicedb, MonitorInterval
from django.shortcuts import render
import json
from datetime import datetime, timedelta


# 获取CPU监控间隔时间
def get_cpu_monitor_interval():
    try:
        cpu_monitor_interval = MonitorInterval.objects.get(name='cpu_interval').interval
    except MonitorInterval.DoesNotExist:
        m = MonitorInterval(name='cpu_interval',
                            interval=1)
        m.save()
        cpu_monitor_interval = MonitorInterval.objects.get(name='cpu_interval').interval
    return cpu_monitor_interval


def device_monitor_cpu(request):
    # 存储设备ID和设备名的列表
    devices_list = []
    for device in Devicedb.objects.all().order_by('id'):
        devices_list.append({'id': device.id, 'name': device.name})

    # 取当前设备的name
    current_obj = Devicedb.objects.all().order_by('id')[0]
    current = current_obj.name

    # 取出一定时间内的记录数据
    cpu_usage_in_monitor_interval = current_obj.cpu_usage.filter(record_datetime__gt=datetime.now() - timedelta(hours=get_cpu_monitor_interval()))

    cpu_usage = []
    cpu_record_time = []

    # sorted() 函数对所有可迭代的对象进行排序操作，key是可迭代对象内的参数，用key进行排序
    for x in sorted(cpu_usage_in_monitor_interval, key=lambda k: k.record_datetime):
        # 把每一分钟采集到的CPU利用率写入cpu_data清单
        cpu_usage.append(x.cpu_usage)
        # 把采集时间格式化然后写入cpu_time清单
        cpu_record_time.append(x.record_datetime.strftime('%H:%M'))
        # 返回'monitor_devices_cpu.html'页面,与设备清单, 当前设备, CPU利用率清单cpu_data, CPU采集时间清单cpu_time
        # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
    cpu_data = json.dumps(cpu_usage)
    cpu_time = json.dumps(cpu_record_time)
    return render(request, 'devnet_device_monitor_cpu.html', locals())


def device_monitor_cpu_device(request, device_id):
    devices_list = []
    for device in Devicedb.objects.all().order_by('id'):
        devices_list.append({'id': device.id, 'name': device.name})

    current_obj = Devicedb.objects.get(id=device_id)
    current = current_obj.name

    cpu_usage_in_monitor_interval = current_obj.cpu_usage.filter(record_datetime__gt=datetime.now() - timedelta(hours=get_cpu_monitor_interval()))

    cpu_usage = []
    cpu_record_time = []

    for x in sorted(cpu_usage_in_monitor_interval, key=lambda k: k.record_datetime):
        cpu_usage.append(x.cpu_usage)  # 把每一分钟采集到的CPU利用率写入cpu_data清单
        # 把采集时间格式化然后写入cpu_time清单
        cpu_record_time.append(x.record_datetime.strftime('%H:%M'))
        # 返回'monitor_devices_cpu.html'页面,与设备清单, 当前设备, CPU利用率清单cpu_data, CPU采集时间清单cpu_time
        # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
    cpu_data = json.dumps(cpu_usage)
    cpu_time = json.dumps(cpu_record_time)

    return render(request, 'devnet_device_monitor_cpu.html', locals())
