#!/usr/bin/env python3

import django
import sys
# 在crontab环境下可能会无法找到PYTHONPATH，PYTHONPATH决定python查找lib的路径
sys.path.append('/home/ljtc/dev')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()

from devnet2019.models import Devicedb, DeviceInterface, DeviceInterfaceState, DeviceInterfaceSpeed, DeviceInterfaceInBytes, DeviceInterfaceOutBytes
from devnet2019.models import Thresholdutilization
from devnet2019.models import LastAlarmUtilization
from modules.devnet_0_snmp_get import get_interface_info
from datetime import datetime
from modules.devnet_0_smtp import alarm_msg


# 接口告警阈值和告警周期
def get_utilization_threshold():
    try:
        # 接口利用率 告警阈值
        utilization_threshold_obj = Thresholdutilization.objects.get(id=1)
        threshold = utilization_threshold_obj.utilization_threshold
        # 判断是否有告警阈值
        if not threshold:
            return False
        else:
            # 接口利用率 告警周期
            interval = utilization_threshold_obj.alarm_interval
            # 判断是否有告警周期
            if not interval:
                return False
            else:
                return threshold, interval
    except Thresholdutilization.DoesNotExist:
        return False


# 刷新告警记录时间
def get_utilization_last_alarm(interface_obj):
    if not get_utilization_threshold():
        return False
    # 获取告警周期
    interval = get_utilization_threshold()[1]
    try:
        # 获取上一次告警记录时间
        last_alarm = LastAlarmUtilization.objects.get(interface=interface_obj).last_alarm_datetime
        # 判断两次告警间隔是否大于1小时
        if (datetime.now() - last_alarm).seconds > (interval * 60):
            l = LastAlarmUtilization.objects.get(interface=interface_obj)
            # 刷新告警记录时间
            l.last_alarm_datetime = datetime.now()
            l.save()
            return True
        else:
            return False
    except LastAlarmUtilization.DoesNotExist:
        c = LastAlarmUtilization(interface=interface_obj)
        c.save()
        return True


# 获取接口数量
def get_interface_todb():
    for device in Devicedb.objects.all():
        try:
            # 如果设备snmp可达
            if device.reachable.all().order_by('-id')[0].snmp_reachable:
                # 通过zip()函数得到所有接口数据列表
                interface_info_list = get_interface_info(device.ip)
                for x in interface_info_list:
                    # 如果第一次采集信息，无法从DeviceInterface表中取得接口名。之后的采集都可以直接从表中取出接口名
                    try:
                        i = DeviceInterface.objects.get(device=device, interface_name=x.get('name'))
                        i.interface_speed.speed = x.get('speed')
                        i.interface_speed.save()
                    # DoesNotExist 这个异常就是取不到表中数据
                    except DeviceInterface.DoesNotExist:
                        i = DeviceInterface(device=device, interface_name=x.get('name'))
                        i.save()
                        interface_speed = DeviceInterfaceSpeed(interface=i, speed=x.get('speed'))
                        interface_speed.save()

                    # 向接口状态表写入数据
                    interface_state = DeviceInterfaceState(interface=i, state=x.get('state'))
                    interface_state.save()

                    # 向入接口字节表写入数据
                    in_bytes = DeviceInterfaceInBytes(interface=i, in_bytes=x.get('in_bytes'))
                    in_bytes.save()

                    # 判断是否设置了告警周期和告警阈值
                    if get_utilization_threshold():
                        if DeviceInterfaceInBytes.objects.filter(interface=i):
                            # 倒序取一个接口的所有入向字节数
                            last_record = DeviceInterfaceInBytes.objects.filter(interface=i).order_by('-id')
                            # 取数据库中的最近的一条数据
                            last_0_bytes = last_record[0].in_bytes
                            # 取数据库中的最近的一条数据记录时间
                            last_0_time = last_record[0].record_datetime
                            # 取数据库中的上一条数据
                            last_1_bytes = last_record[1].in_bytes
                            # 取数据库中的上一条数据记录时间
                            last_1_time = last_record[1].record_datetime
                            # 计算接口利用率
                            # * 8 是将采集到的Bytes转换为bit，/ 数据采集周期。得到的即是速率 bits/s
                            # * 100 是将利用率单位转为%
                            utilization_now = (((last_0_bytes - last_1_bytes) * 8) / (last_0_time - last_1_time).seconds / x.get('speed')) * 100
                            # 判断当前利用率是否超过了告警阈值
                            if utilization_now > get_utilization_threshold()[0]:
                                # 当2次告警周期大于1小时就发邮件，round(x, 2)是控制浮点数的单位为小数点后两位
                                if get_utilization_last_alarm(i):
                                    alarm_msg("设备{0} 接口{1} 入向利用率超过阈值{2}%!当前的利用率为{3}%".format(
                                                                                                        device.name,
                                                                                                        i.interface_name,
                                                                                                        get_utilization_threshold()[0],
                                                                                                        round(utilization_now, 2)
                                                                                                      ))
                    # 向出接口字节表写入数据
                    out_bytes = DeviceInterfaceOutBytes(interface=i, out_bytes=x.get('out_bytes'))
                    out_bytes.save()

                    # 判断是否设置了告警周期和告警阈值
                    if get_utilization_threshold():
                        if DeviceInterfaceOutBytes.objects.filter(interface=i):
                            # 倒序取一个接口的所有出向字节数
                            last_record = DeviceInterfaceOutBytes.objects.filter(interface=i).order_by('-id')
                            # 取数据库中的最近的一条数据
                            last_0_bytes = last_record[0].out_bytes
                            # 取数据库中的最近的一条数据记录时间
                            last_0_time = last_record[0].record_datetime
                            # 取数据库中的上一条数据
                            last_1_bytes = last_record[1].out_bytes
                            # 取数据库中的上一条数据记录时间
                            last_1_time = last_record[1].record_datetime
                            # 计算出接口利用率
                            utilization_now = (((last_0_bytes - last_1_bytes) * 8) / (last_0_time - last_1_time).seconds / x.get('speed')) * 100
                            # 判断当前速率是否超过了告警阈值
                            if utilization_now > get_utilization_threshold()[0]:
                                # 当2次告警周期大于1小时就发邮件
                                if get_utilization_last_alarm(i):
                                    alarm_msg("设备{0} 接口{1} 出向利用率超过阈值{2}%!当前的利用率为{3}%".format(
                                                                                                        device.name,
                                                                                                        i.interface_name,
                                                                                                        get_utilization_threshold()[0],
                                                                                                        round(utilization_now, 2)))

            else:
                continue
        except Exception as a:
            print(a)
            continue


if __name__ == '__main__':
    # print(get_utilization_threshold())
    get_interface_todb()
