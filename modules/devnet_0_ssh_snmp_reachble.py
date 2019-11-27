#!/usr/bin/env python3

import re
import netmiko
import sys
# 在crontab环境下可能会无法找到PYTHONPATH，PYTHONPATH决定python查找lib的路径
sys.path.append('/home/network-ops')
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()

from devnet2019.models import DeviceReachable, Deviceconfig, DeviceconfigDir
from modules.devnet_0_configfile import device_types
from modules.devnet_0_snmp_get import snmp_sure_reachable

configdir = DeviceconfigDir.objects.get(id=1).dir_name


# 取可达性并写入数据库
def ssh_sure_shell_login(device):
    # snmp可达性
    snmp_reachable = snmp_sure_reachable(device.get('ip'), device.get('snmp_ro_community'))

    # 保存SNMP可达性和SSH可达性到数据库
    def save_sql(verdict):
        d = DeviceReachable(device_id=device.get('id'),
                            ssh_reachable=verdict,
                            snmp_reachable=snmp_reachable)
        d.save()

    # 判断华为或华三设备的SSH可达性
    if device.get('type_name') in device_types:
        try:
            # 建立SSH连接
            huawei_ssh = netmiko.Netmiko(device_type='huawei_ssh', ip=device.get('ip'), username=device.get('username'), password=device.get('password'))
            # 启用enable进入特权模式
            huawei_ssh.config_mode()
            # 找到当前所在层级并赋值给ssh_reachable
            ssh_reachable = huawei_ssh.find_prompt()
            # 关闭连接
            huawei_ssh.disconnect()
            # 正则匹配，确认是否进入用户模式
            if re.search(']', ssh_reachable):
                save_sql('True')
            else:
                save_sql('False')
        except Exception as a:
            print(a)
            save_sql('False')

    else:
        try:
            # 建立SSH连接
            cisco_ssh = netmiko.Netmiko(device_type='cisco_asa_ssh', ip=device.get('ip'), username=device.get('username'), password=device.get('password'), secret=device.get('enable_pwd'))
            # 启用config_mode进入配置模式
            cisco_ssh.enable()
            # 找到当前所在层级并赋值给ssh_reachable
            ssh_reachable = cisco_ssh.find_prompt()
            # 关闭连接
            cisco_ssh.disconnect()
            # 正则匹配，确认是否进入配置模式
            if re.search('#', ssh_reachable):
                save_sql('True')
            else:
                save_sql('False')
        except Exception as a:
            save_sql('False')


if __name__ == '__main__':
    f = [{'ip': '192.168.20.4', 'username': 'admin', 'password': 'YUting@123', 'enable_pwd': 'YUting@123', 'id': 4}, {'ip': '192.168.20.5', 'username': 'admin', 'password': 'YUting@123', 'enable_pwd': '', 'id': 8}]
    # ssh_sure_shell_login_cisco(f)
    # print(ssh_sure_shell_login_huawei('192.168.20.6', 'admin', 'cisco', 'YUting@123'))
