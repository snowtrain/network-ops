#!/usr/bin/env python3

from devnet2019.models import Devicedb, MonitorInterval
from django.shortcuts import render
import json
from datetime import datetime, timedelta


# 获取mem监控间隔时间
def get_mem_monitor_interval():
    try:
        mem_monitor_interval = MonitorInterval.objects.get(name='mem_interval').interval
    except MonitorInterval.DoesNotExist:
        m = MonitorInterval(name='mem_interval',
                            interval=1)
        m.save()
        mem_monitor_interval = MonitorInterval.objects.get(name='mem_interval').interval
    return mem_monitor_interval


def device_monitor_mem(request):
    # 存储设备ID和设备名的列表
    devices_list = []
    for device in Devicedb.objects.all().order_by('id'):
        devices_list.append({'id': device.id, 'name': device.name})

    # 取当前设备的name
    current_obj = Devicedb.objects.all().order_by('id')[0]
    current = current_obj.name

    # 取出一个小时内的记录数据
    mem_usage_in_monitor_interval = current_obj.mem_usage.filter(record_datetime__gt=datetime.now() - timedelta(hours=get_mem_monitor_interval()))

    mem_usage = []
    mem_record_time = []

    # sorted() 函数对所有可迭代的对象进行排序操作，key是可迭代对象内的参数，用key进行排序
    for x in sorted(mem_usage_in_monitor_interval, key=lambda k: k.record_datetime):
        # 把每一分钟采集到的mem利用率写入mem_data清单
        mem_usage.append(x.mem_usage)
        # 把采集时间格式化然后写入mem_time清单
        mem_record_time.append(x.record_datetime.strftime('%H:%M'))
        # 返回'monitor_devices_mem.html'页面,与设备清单, 当前设备, mem利用率清单mem_data, mem采集时间清单mem_time
        # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
    mem_data = json.dumps(mem_usage)
    mem_time = json.dumps(mem_record_time)
    return render(request, 'devnet_device_monitor_mem.html', locals())


def device_monitor_mem_device(request, device_id):
    devices_list = []
    for device in Devicedb.objects.all().order_by('id'):
        devices_list.append({'id': device.id, 'name': device.name})

    current_obj = Devicedb.objects.get(id=device_id)
    current = current_obj.name

    mem_usage_in_monitor_interval = current_obj.mem_usage.filter(record_datetime__gt=datetime.now() - timedelta(hours=get_mem_monitor_interval()))

    mem_usage = []
    mem_record_time = []

    for x in sorted(mem_usage_in_monitor_interval, key=lambda k: k.record_datetime):
        mem_usage.append(x.mem_usage)  # 把每一分钟采集到的mem利用率写入mem_data清单
        # 把采集时间格式化然后写入mem_time清单
        mem_record_time.append(x.record_datetime.strftime('%H:%M'))
        # 返回'monitor_devices_mem.html'页面,与设备清单, 当前设备, mem利用率清单mem_data, mem采集时间清单mem_time
        # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
    mem_data = json.dumps(mem_usage)
    mem_time = json.dumps(mem_record_time)

    return render(request, 'devnet_device_monitor_mem.html', locals())
