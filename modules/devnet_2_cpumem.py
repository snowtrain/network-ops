#!/usr/bin/python3

import django
import sys
# 在crontab环境下可能会无法找到PYTHONPATH，PYTHONPATH决定python查找lib的路径
sys.path.append('/home/ljtc/dev')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()
from devnet2019.models import Devicedb, Devicecpu, Devicemem, LastAlarmCPU, LastAlarmMEM, LastAlarmSNMP, Thresholdcpu, Thresholdmem, Thresholdsnmp
from modules.devnet_0_snmp_get import get_mem_cpu
from datetime import datetime
from modules.devnet_0_smtp import alarm_msg


# 得到CPU阈值、告警周期
def get_cpu_threshold():
    try:
        cpu_threshold_obj = Thresholdcpu.objects.get(id=1)
        # CPU阈值
        threshold = cpu_threshold_obj.cpu_threshold
        if not threshold:
            return False
        else:
            # 告警周期
            interval = cpu_threshold_obj.alarm_interval
            if not interval:
                return False
            else:
                return threshold, interval
    except Thresholdcpu.DoesNotExist:
        return False


# 得到内存阈值、告警周期
def get_mem_threshold():
    try:
        mem_threshold_obj = Thresholdmem.objects.get(id=1)
        # 内存阈值
        threshold = mem_threshold_obj.mem_threshold
        if not threshold:
            return False
        else:
            # 告警周期
            interval = mem_threshold_obj.alarm_interval
            if not interval:
                return False
            else:
                return threshold, interval
    except Thresholdmem.DoesNotExist:
        return False


# 得到snmp告警周期
def get_snmp_interval():
    try:
        snmp_threshold_obj = Thresholdsnmp.objects.get(id=1)
        interval = snmp_threshold_obj.alarm_interval
        if not interval:
            return False
        else:
            return interval
    except Thresholdsnmp.DoesNotExist:
        return False


# 刷新告警记录时间
def get_device_cpu_last_alarm(device_obj):
    if not get_cpu_threshold():
        return False
    # 告警周期
    interval = get_cpu_threshold()[1]
    try:
        # 获取告警记录时间
        last_alarm = LastAlarmCPU.objects.get(device=device_obj).last_alarm_datetime
        # 判断距离告警记录时间是否大于1小时
        if (datetime.now() - last_alarm).seconds > interval * 60:
            l = LastAlarmCPU.objects.get(device=device_obj)
            # 刷新告警记录时间
            l.last_alarm_datetime = datetime.now()
            l.save()
            return True
        else:
            return False
    except LastAlarmCPU.DoesNotExist:
        c = LastAlarmCPU(device=device_obj)
        c.save()
        return True


# 刷新告警记录时间
def get_device_mem_last_alarm(device_obj):
    if not get_mem_threshold():
        return False
    interval = get_mem_threshold()[1]
    try:
        last_alarm = LastAlarmMEM.objects.get(device=device_obj).last_alarm_datetime
        if (datetime.now() - last_alarm).seconds > interval * 60:
            l = LastAlarmMEM.objects.get(device=device_obj)
            l.last_alarm_datetime = datetime.now()
            l.save()

            return True
        else:
            return False
    except LastAlarmMEM.DoesNotExist:
        c = LastAlarmMEM(device=device_obj)
        c.save()
        return True


# 刷新告警记录时间
def get_device_snmp_last_alarm(device_obj):
    if not get_snmp_interval():
        return False
    # 获取告警周期，由于返回只有一个返回值，不需要用 [0] 取元素
    interval = get_snmp_interval()
    try:
        # 获取告警记录时间
        last_alarm = LastAlarmSNMP.objects.get(device=device_obj).last_alarm_datetime
        # 判断距离告警记录时间是否大于1小时
        if (datetime.now() - last_alarm).seconds > interval * 60:
            l = LastAlarmSNMP.objects.get(device=device_obj)
            # 刷新告警记录时间
            l.last_alarm_datetime = datetime.now()
            l.save()
            return True
        else:
            return False
    except LastAlarmSNMP.DoesNotExist:
        c = LastAlarmSNMP(device=device_obj)
        c.save()
        return True


# 获取CPU和内存使用率
def get_mem_cpu_todb():
    for device in Devicedb.objects.all():
        try:
            # 判断SNMP可达性
            if device.reachable.all().order_by('-id')[0].snmp_reachable:
                # 获取内存和CPU利用率
                mem_percent, cpu_percent = get_mem_cpu(device.ip)
                # 判断是否设置了CPU阈值和告警周期
                if get_cpu_threshold():
                    # 判断当前CPU利用率是否超过了阈值
                    if cpu_percent > get_cpu_threshold()[0]:
                        # 如果2次告警时间差大于1小时，就发邮件告警
                        if get_device_cpu_last_alarm(device):
                            alarm_msg("设备{0} CPU利用率超过阈值{1}%!当前的CPU利用率为{2}%".format(device.name, get_cpu_threshold()[0], cpu_percent))

                # 向数据库中写入内存利用率
                m = Devicemem(device=device, mem_usage=mem_percent)
                m.save()
                # 判断是否设置了告警阈值和告警周期
                if get_mem_threshold():
                    # 判断当前内存利用率是否超过了阈值
                    if mem_percent > get_mem_threshold()[0]:
                        # 如果2次告警时间差大于1小时，就发邮件告警
                        if get_device_mem_last_alarm(device):
                            alarm_msg("设备{0} 内存利用率超过阈值{1}%!当前的内存利用率为{2}%".format(device.name, get_mem_threshold()[0], mem_percent))

                # 向数据库中写入CPU利用率
                c = Devicecpu(device=device, cpu_usage=cpu_percent)
                c.save()
            else:
                if get_device_snmp_last_alarm(device):
                    alarm_msg("设备{0} SNMP不可达".format(device.name))
                continue
        except Exception:
            continue


if __name__ == '__main__':
    get_mem_cpu_todb()
