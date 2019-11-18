#!/usr/bin/env python3

from django.http import JsonResponse
from devnet2019.models import Devicedb


def health_reachable(request):  # 为首页的"设备健康摘要" 饼状图提供JSON数据
    # 从Device_reachable表,获取所有设备可达性信息
    devices = Devicedb.objects.all()
    green_devices = 0
    yellow_devices = 0
    red_devices = 0
    for x in devices:
        try:
            device_reachable = x.reachable.all().order_by('-id')[0]
        except Exception:
            continue
        # 如果SSH与SNMP都可达, 绿色设备数量加1
        if device_reachable.ssh_reachable and device_reachable.snmp_reachable:
            green_devices += 1
        # 如果SSH与SNMP都不可达, 红色设备数量加1
        elif not device_reachable.ssh_reachable and not device_reachable.snmp_reachable:
            red_devices += 1
        # 其余为黄色设备
        else:
            yellow_devices += 1
    colors = ['#228b22', '#ffff00', '#ff0000']  # 颜色代码清单[绿, 黄, 红]
    labels = ['正常', 'SNMP或SSH不可达', '全部不可达']
    datas = [green_devices, yellow_devices, red_devices]  # 设备数量清单
    # 返回JSON数据, 给首页的"设备健康摘要"饼状图
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


def health_cpu(request):  # 为首页的"CPU利用率摘要" 饼状图提供JSON数据
    # 从Devicecpumem表,获取所有设备的CPU和内存利用率信息
    devices = Devicedb.objects.all()
    green_devices = 0
    yellow_devices = 0
    red_devices = 0
    for x in devices:
        try:
            device_cpu = x.cpu_usage.all().order_by('-id')[0]
        except Exception:
            continue
        # 如果当前CPU利用率超过70%, 红色设备加1
        if device_cpu.cpu_usage >= 70:
            red_devices += 1
        # 如果当前CPU利用率在70% 与 30%之间, 黄色设备加1
        elif 70 > device_cpu.cpu_usage >= 30:
            yellow_devices += 1
        # 其余为绿色设备
        else:
            green_devices += 1
    colors = ['#228b22', '#ffff00', '#ff0000']  # 颜色代码清单[绿, 黄, 红]
    labels = ['低于30%', '30%到70%之间', '高于70%']
    datas = [green_devices, yellow_devices, red_devices]  # 设备数量清单
    # 返回JSON数据, 给首页的"CPU利用率摘要"饼状图
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


def health_mem(request):  # 为首页的"内存利用率摘要" 饼状图提供JSON数据
    # 从Devicecpumem表,获取所有设备的CPU和内存利用率信息
    devices = Devicedb.objects.all()
    green_devices = 0
    yellow_devices = 0
    red_devices = 0
    for x in devices:
        try:
            device_mem = x.mem_usage.all().order_by('-id')[0]
        except Exception:
            continue
        # 如果当前内存利用率超过70%, 红色设备加1
        if device_mem.mem_usage >= 70:
            red_devices += 1
        # 如果当前内存利用率在70% 与 30%之间, 黄色设备加1
        elif 70 > device_mem.mem_usage >= 30:
            yellow_devices += 1
        # 其余为绿色设备
        else:
            green_devices += 1
    colors = ['#228b22', '#ffff00', '#ff0000']  # 颜色代码清单[绿, 黄, 红]
    labels = ['低于30%', '30%到70%之间', '高于70%']
    datas = [green_devices, yellow_devices, red_devices]  # 设备数量清单
    # 返回JSON数据, 给首页的"内存利用率摘要"饼状图
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})
