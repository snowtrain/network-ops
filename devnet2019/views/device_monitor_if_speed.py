#!/usr/bin/env python3

from devnet2019.models import Devicedb, DeviceInterface, MonitorInterval
from django.shortcuts import render
from datetime import datetime, timedelta
import numpy as np
from django.http import JsonResponse


# 获取速率监控间隔
def get_speed_monitor_interval():
    try:
        speed_monitor_interval = MonitorInterval.objects.get(name='speed_interval').interval
    except MonitorInterval.DoesNotExist:
        m = MonitorInterval(name='speed_interval',
                            interval=1)
        m.save()
        speed_monitor_interval = MonitorInterval.objects.get(name='speed_interval').interval
    return speed_monitor_interval


def device_monitor_if_speed(request):
    devices_list = []
    # 取出每个设备对象的id和name
    for device in Devicedb.objects.all().order_by('id'):
        devices_list.append({'id': device.id, 'name': device.name})

    # 取当前设备的name
    current_obj = Devicedb.objects.all().order_by('id')[0]
    current = current_obj.name

    device_id = current_obj.id
    if_list = []

    # 取当前设备的所有接口
    for interface in current_obj.interface.all():
        # 如果在最新的数据条目中接口的双向字节数不为空，接口状态为True，就构造接口id和接口name的字典
        if interface.interface_in_bytes.all().order_by('-id')[0].in_bytes and \
                interface.interface_out_bytes.all().order_by('-id')[0].out_bytes and \
                interface.interface_state.all().order_by('-id')[0].state:
            if_dict = {'id': interface.id, 'name': interface.interface_name}
        else:
            continue
        # 放进接口列表
        if_list.append(if_dict)

    return render(request, 'devnet_device_monitor_if_speed.html', locals())


def device_monitor_if_speed_device(request, device_id):
    devices_list = []
    # 取出每个设备对象的id和name
    for device in Devicedb.objects.all().order_by('id'):
        devices_list.append({'id': device.id, 'name': device.name})

    # 取当前设备的name
    current_obj = Devicedb.objects.get(id=device_id)
    current = current_obj.name

    if_list = []
    for interface in current_obj.interface.all():
        try:
            # 如果在最新的数据条目中接口的双向字节数不为空，接口状态为True，就构造接口id和接口name的字典
            if interface.interface_in_bytes.all().order_by('-id')[0].in_bytes and \
                    interface.interface_out_bytes.all().order_by('-id')[0].out_bytes and \
                    interface.interface_state.all().order_by('-id')[0].state:
                if_dict = {'id': interface.id, 'name': interface.interface_name}
            else:
                continue
            if_list.append(if_dict)
        except IndexError:
            continue

    return render(request, 'devnet_device_monitor_if_speed.html', locals())


def device_monitor_if_speed_device_ajax(request, interface_id, direction):
    # 取指定接口对象
    interface_obj = DeviceInterface.objects.get(id=interface_id)
    # 取指定接口name
    ifname = interface_obj.interface_name

    # 出/入向字节列表
    bytes_list = []
    # 出/入向记录时间列表
    time_list = []
    # 出/入向格式化时间列表
    time_strf_list = []

    if direction == 'rx':
        # 取1小时内的指定接口入向数据
        bytes_data = interface_obj.interface_in_bytes.filter(record_datetime__gt=datetime.now() - timedelta(hours=get_speed_monitor_interval()))
        # 以数据记录时间排序，将数据分别加入列表
        for x in sorted(bytes_data, key=lambda k: k.record_datetime):
            bytes_list.append(x.in_bytes)
            time_list.append(x.record_datetime)
            time_strf_list.append(x.record_datetime.strftime('%H:%M:%S'))

    elif direction == 'tx':
        # 取1小时内的指定接口出向数据
        bytes_data = interface_obj.interface_out_bytes.filter(record_datetime__gt=datetime.now() - timedelta(hours=get_speed_monitor_interval()))
        # 以数据记录时间排序，将数据分别加入列表
        for x in sorted(bytes_data, key=lambda k: k.record_datetime):
            bytes_list.append(x.out_bytes)
            time_list.append(x.record_datetime)
            time_strf_list.append(x.record_datetime.strftime('%H:%M:%S'))

    # numpy的diff计算列表的差值
    # b = list(np.diff([1, 6, 7, 8, 12]))
    # print(b)
    # [5, 1, 1, 4]
    # 通过这种方式获取每次得到的字节数的差值
    diff_if_bytes_list = list(np.diff(bytes_list))

    # 计算每个时间对象的秒数的差值，提取秒数放入列表
    diff_record_time_list = [x.seconds for x in np.diff(time_list)]

    # 计算速率
    # * 8 得到bit数
    # /1000 计算kb
    # / x[1] 时间差，计算kbps
    # round(x, 2) 保留两位小数
    # zip把字节差列表 和 时间差列表 压到一起

    zip_list = []
    for z in zip(diff_if_bytes_list, diff_record_time_list):
        # 过滤字节数为0的元组
        if z[0] < 0:
            continue
        else:
            zip_list.append(z)

    # 计算速率，lambda 需要一个表达式和任意数量的变量，但只能返回一个表达式的值。这里返回的即是速率
    speed_data = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2), zip_list))
    speed_time = time_strf_list[1:]
    # 返回一个JSON对象
    return JsonResponse({"ifname": ifname, "speed_data": speed_data, "speed_time": speed_time})
