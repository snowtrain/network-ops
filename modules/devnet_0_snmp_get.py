#!/usr/bin/env python3

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()
from pysnmp.hlapi import *
from devnet2019.models import Devicedb, SNMPtype
from pysnmp.entity.rfc3413.oneliner import cmdgen
from modules.devnet_0_configfile import device_types


def snmpv2_get(ip, community, oid, port=161):
    iterator = getCmd(SnmpEngine(),
                      CommunityData(community),  # 配置community
                      UdpTransportTarget((ip, port)),  # 配置目的地址和端口号
                      ContextData(),
                      ObjectType(ObjectIdentity(oid)))  # 读取的OID

    # varBinds是列表，列表中的每个元素的类型是ObjectType（该类型的对象表示MIB variable）
    errorindication, errorstatus, errorindex, varbinds = next(iterator)

    # 错误处理
    if errorindication:
        print(errorindication)
    elif errorstatus:
        print('%s at %s' % (errorstatus, errorindex and varbinds[int(errorindex) - 1][0] or '?'))

    # 如果返回结果有多行,需要拼接后返回
    result = ""
    for varBind in varbinds:
        result = result + varBind.prettyPrint()  # 返回结果！
    # 返回的为一个元组,OID与字符串结果
    return result.split("=")[0].strip(), result.split("=")[1].strip()


def snmpv2_getnext(ip, community, oid, port=161):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorindex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData(community),  # 设置community
        cmdgen.UdpTransportTarget((ip, port)), oid, )  # 设置IP地址、端口号和OID

    # 错误处理
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorindex and varBinds[int(errorindex) - 1][0] or '?'
        )
              )

    result = []
    # varBindTable是个list，元素的个数可能有好多个。它的元素也是list，这个list里的元素是ObjectType，个数只有1个。
    for varBindTableRow in varBindTable:
        for item in varBindTableRow:
            result.append((item.prettyPrint().split("=")[0].strip(), item.prettyPrint().split("=")[1].strip()))
    return result


def snmp_sure_reachable(ip, community):
    try:
        if "SNMPv2-MIB::sysDescr.0" == snmpv2_get(ip, community, "1.3.6.1.2.1.1.1.0", port=161)[0]:
            snmp_reachable = True
        else:
            snmp_reachable = False
    except IndexError:
        snmp_reachable = False
    return snmp_reachable


# 获取CPU、内存数值
def get_mem_cpu(ip):
    device = Devicedb.objects.get(ip=ip)

    # 从数据库中取得snpy_type和oid
    cpu_usage_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='cpu_usage')).oid
    mem_usage_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='mem_usage')).oid
    mem_free_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='mem_free')).oid

    ro_community = device.snmp_ro_community

    # 拿到当前内存已用值
    used = int(snmpv2_get(ip, ro_community, mem_usage_oid)[1])
    # 拿到当前内存剩余值
    free = int(snmpv2_get(ip, ro_community, mem_free_oid)[1])
    # 拿到CPU利用率
    cpu = int(snmpv2_get(ip, ro_community, cpu_usage_oid)[1])

    # 华为设备没有已用内存OID，used=全部内存，free=剩余内存只有全部内存OID和剩余内存OID
    if device.type.type_name in device_types:
        return round(float((used - free) / used) * 100, 2), cpu
    else:
        # 返回计算后的内存利用率和CPU利用率
        return round(float(used/(free + used)) * 100, 2), cpu


def get_interface_info(ip):
    device = Devicedb.objects.get(ip=ip)
    # 提取OID
    if_name_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='if_name')).oid
    if_speed_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='if_speed')).oid
    if_state_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='if_state')).oid
    if_in_bytes_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='if_in_bytes')).oid
    if_out_bytes_oid = device.type.devicesnmp.get(snmp_type=SNMPtype.objects.get(snmp_type='if_out_bytes')).oid

    # 通过snmp的get_next_request获得一个OID下的所有子节点，返回值是列表
    if_name_list = [x[1] for x in snmpv2_getnext(ip, device.snmp_ro_community, if_name_oid)]

    # 接口速率列表
    if_speed_list = [int(x[1]) for x in snmpv2_getnext(ip, device.snmp_ro_community, if_speed_oid)]

    # 接口状态列表
    if_state_list = [int(x[1]) for x in snmpv2_getnext(ip, device.snmp_ro_community, if_state_oid)]

    # 入接口bytes列表
    if_in_bytes_list = [int(x[1]) for x in snmpv2_getnext(ip, device.snmp_ro_community, if_in_bytes_oid)]

    # 出接口bytes列表
    if_out_bytes_list = [int(x[1]) for x in snmpv2_getnext(ip, device.snmp_ro_community, if_out_bytes_oid)]

    # zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象，可以使用list或将对象转换成列表或者for循环等方式取出数据
    if_all = zip(if_name_list, if_state_list, if_speed_list, if_in_bytes_list, if_out_bytes_list)

    if_all_list = []
    # 构建关于接口数据的数据字典，将所有接口字典加入列表
    for x in if_all:
        if_dict = {'name': x[0],
                   'state': True if x[1] == 1 else False,
                   'speed': x[2],
                   'in_bytes': x[3],
                   'out_bytes': x[4]}
        if_all_list.append(if_dict)
    return if_all_list


if __name__ == '__main__':
    # # print(snmp_sure_reachable('192.168.1.104', 'qytangro'))
    # print(get_mem_cpu('192.168.20.3'))
    print(snmpv2_get('192.168.20.3', 'snowro', '1.3.6.1.4.1.9.9.109.1.1.1.1.7.1'))
    print(snmpv2_get('192.168.20.3', 'snowro', '1.3.6.1.4.1.9.9.109.1.1.1.1.12.1'))
    print(snmpv2_get('192.168.20.3', 'snowro', '1.3.6.1.4.1.9.9.109.1.1.1.1.13.1'))
    # print(get_interface_info('192.168.20.6'))
