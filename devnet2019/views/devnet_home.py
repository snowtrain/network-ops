#!/usr/bin/env python3
from datetime import datetime, timedelta

from django.db.models import Max
from django.shortcuts import render
import numpy as np
from devnet2019.models import Devicedb, DeviceInterface
from modules.devnet_0_cpumem_interval import cpu_max_interval, mem_max_interval


def home(request):
    devices_cpu_list = []
    devices_mem_list = []
    top_5_if_utilization_rx_dict = []
    top_5_if_utilization_tx_dict = []
    for device in Devicedb.objects.all():
        # 获取数据库中监控周期内的CPU最大利用率
        cpu_max = device.cpu_usage.filter(record_datetime__gt=datetime.now() - timedelta(hours=cpu_max_interval)).aggregate(Max('cpu_usage')).get('cpu_usage__max')

        try:
            # 当前最新 CPU 使用率
            cpu_current = device.cpu_usage.all().order_by('-id')[0].cpu_usage
            # 映射成 设备名、CPU最大利用率、当前利用率 的字典并放进汇总列表
            devices_cpu_list.append({'name': device.name, 'cpu_max': cpu_max, 'cpu_current': cpu_current})
            # 对 cpu_max 对列表排序
            devices_cpu_list = sorted(devices_cpu_list, key=lambda y: y['cpu_max'], reverse=True)
            # 取前5位
            devices_cpu_list = devices_cpu_list[:5]
        except IndexError:
            continue
        except TypeError:
            continue

        try:
            # 获取数据库中监控周期内的CPU最大利用率
            mem_max = device.mem_usage.filter(record_datetime__gt=datetime.now() - timedelta(hours=mem_max_interval)).aggregate(Max('mem_usage')).get('mem_usage__max')
            # 当前最新 MEM 使用率
            mem_current = device.mem_usage.all().order_by('-id')[0].mem_usage
            # 映射成 设备名、CPU最大利用率、当前利用率 的字典并放进汇总列表
            devices_mem_list.append({'name': device.name, 'mem_max': mem_max, 'mem_current': mem_current})
            # 对 cpu_max 对列表排序
            devices_mem_list = sorted(devices_mem_list, key=lambda y: y['mem_max'], reverse=True)
            # 取前5位
            devices_mem_list = devices_mem_list[:5]
        except IndexError:
            continue
        except TypeError:
            continue

    active_inteface = []
    for interface in DeviceInterface.objects.all():
        try:
            # 获取活动接口
            if interface.interface_out_bytes.order_by('-id')[0].out_bytes > 0 and interface.interface_in_bytes.order_by('-id')[0].in_bytes > 0:
                active_inteface.append(interface)
            else:
                continue
        except Exception:
            continue
    for interface in active_inteface:
        # 如方向利用率
        interface_in_data = interface.interface_in_bytes.filter(record_datetime__gt=datetime.now() - timedelta(hours=1))
        in_bytes_list = []
        in_bytes_time = []
        # 对入向接口排序并提取字节数、记录时间
        for x in sorted(interface_in_data, key=lambda k: k.record_datetime):
            in_bytes_list.append(x.in_bytes)
            in_bytes_time.append(x.record_datetime)

        # 入向字节差列表
        diff_if_in_bytes_list = list(np.diff(in_bytes_list))

        # 入向时间差列表
        diff_if_in_record_time_list = [x.seconds for x in np.diff(in_bytes_time)]

        # 压缩得到 (字节差,时间差) 的可迭代对象
        zip_in_list = zip(diff_if_in_bytes_list, diff_if_in_record_time_list)

        # 提取接口速率
        interface_speed = interface.interface_speed.speed

        # 计算入向接口利用率列表
        utilization_in_data = list(map(lambda x: round(((x[0] * 8) / x[1] / interface_speed) * 100, 2), zip_in_list))
        try:
            # 向top列表增加数据
            top_5_if_utilization_rx_dict.append({'name': interface.device.name, 'ifname': interface.interface_name, 'rx_max': max(utilization_in_data), 'rx_current': utilization_in_data[-1]})
        except ValueError:
            top_5_if_utilization_rx_dict.append({'name': interface.device.name, 'ifname': interface.interface_name, 'rx_max': 0, 'rx_current': 0})

        # 出方向利用率
        interface_out_data = interface.interface_out_bytes.filter(record_datetime__gt=datetime.now() - timedelta(hours=1))
        out_bytes_list = []
        out_bytes_time = []
        # 对出向接口排序并提取字节数、记录时间
        for x in sorted(interface_out_data, key=lambda k: k.record_datetime):
            out_bytes_list.append(x.out_bytes)
            out_bytes_time.append(x.record_datetime)

        # 入向字节差列表
        diff_if_out_bytes_list = list(np.diff(out_bytes_list))

        # 入向字时间差列表
        diff_if_out_record_time_list = [x.seconds for x in np.diff(out_bytes_time)]

        # 压缩得到 (字节差,时间差) 的可迭代对象
        zip_out_list = zip(diff_if_out_bytes_list, diff_if_out_record_time_list)

        # 计算出向接口利用率列表
        utilization_out_data = list(map(lambda x: round(((x[0] * 8) / x[1] / interface_speed) * 100, 2), zip_out_list))
        try:
            # 向top列表增加数据
            top_5_if_utilization_tx_dict.append({'name': interface.device.name, 'ifname': interface.interface_name, 'tx_max': max(utilization_out_data), 'tx_current': utilization_out_data[-1]})
        except ValueError:
            top_5_if_utilization_tx_dict.append({'name': interface.device.name, 'ifname': interface.interface_name, 'tx_max': 0, 'tx_current': 0})
    top_3_if_utilization_rx_dict = sorted(top_5_if_utilization_rx_dict, key=lambda y: y['rx_max'], reverse=True)
    top_3_if_utilization_rx_dict = top_3_if_utilization_rx_dict[:3]

    top_3_if_utilization_tx_dict = sorted(top_5_if_utilization_tx_dict, key=lambda y: y['tx_max'], reverse=True)
    top_3_if_utilization_tx_dict = top_3_if_utilization_tx_dict[:3]
    return render(request, 'devnet_home.html', locals())
