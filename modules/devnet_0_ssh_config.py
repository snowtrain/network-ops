#!/usr/bin/env python3

from datetime import datetime
import hashlib
import re
import netmiko
import sys
# 在crontab环境下可能会无法找到PYTHONPATH，PYTHONPATH决定python查找lib的路径
sys.path.append('/home/ljtc/dev')
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()

from devnet2019.models import Deviceconfig, DeviceconfigDir
from modules.devnet_0_configfile import device_types, asa_cmd, ios_cmd, huawei_cmd

configdir = DeviceconfigDir.objects.get(id=1).dir_name


def ssh_single_cmd(device):
    # 保存md5到数据库，保存文件到本地
    def save_config():
        config_filename = device.get('device_name') + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M') + '_' + md5_value + '.txt'
        # 保存配置文件
        with open(configdir + config_filename, 'w') as f:
            f.write(run_config)
        # 写入配置文件的md5到数据库，用来比较配置是否有更改
        d = Deviceconfig(device_id=device.get('id'),
                         hash=md5_value,
                         config_filename=config_filename)
        d.save()

    # ASA配置备份
    if device.get('type_name') == 'ASA Firewall':
        # 建立SSH连接
        cisco_ssh = netmiko.Netmiko(device_type='cisco_asa_ssh', ip=device.get('ip'), username=device.get('username'), password=device.get('password'), secret=device.get('enable_pwd'))
        # 启用enable进入特权模式
        cisco_ssh.enable()
        # 执行命令
        result = cisco_ssh.send_config_set([asa_cmd])
        # 关闭连接
        cisco_ssh.disconnect()
        # 返回结果是列表，每一行字符串都是单独的元素
        list_run_config = result.split('\n')

        # 初始下标
        location = 0
        host_location = 0  # 用来找到hostname出现的位置，可以用global变量代替
        for i in list_run_config:
            if re.match('hostname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1

        # 截取hostname开始往后的部分
        list_run_config = list_run_config[host_location:-3]
        # 还原配置 join() 将序列使用指定字符串连接生成新的字符串
        run_config = '\n'.join(list_run_config)

        # 指定hash算法
        m = hashlib.md5()
        # 传入需要hash的内容
        m.update(run_config.encode('utf-8'))
        # 计算hash值
        md5_value = m.hexdigest()

        # 检查数据库中md5是否存在
        try:
            print('Search index ...')
            last_config_backup = Deviceconfig.objects.filter(device=device.get('id')).order_by('-id')[0]
            if last_config_backup.hash == md5_value:  # 如果本次配置的MD5值,与上一次备份配置的MD5值相同!略过此次操作
                print('The index already exists', device.get('ip'))
            else:
                print('Create index ...', device.get('ip'))
                save_config()
        except IndexError as a:
            print('Create index ...', device.get('ip'))
            save_config()

    # 华为和华三配置备份
    elif device.get('type_name') in device_types:
        # 建立SSH连接
        huawei_ssh = netmiko.Netmiko(device_type='huawei_ssh', ip=device.get('ip'), username=device.get('username'), password=device.get('password'), secret=device.get('enable_pwd'))
        # 启用enable进入特权模式
        huawei_ssh.config_mode()
        # 执行命令
        result = huawei_ssh.send_config_set([huawei_cmd])
        # 关闭连接
        huawei_ssh.disconnect()
        # 返回结果是列表，每一行字符串都是单独的元素
        list_run_config = result.split('\n')

        # 初始下标
        location = 0
        host_location = 0  # 用来找到hostname出现的位置，可以用global变量代替
        for i in list_run_config:
            if re.match('sysname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1

        # 截取hostname开始往后的部分
        list_run_config = list_run_config[host_location:-2]
        # 还原配置 join() 将序列使用指定字符串连接生成新的字符串
        run_config = '\n'.join(list_run_config)

        # 指定hash算法
        m = hashlib.md5()
        # 传入需要hash的内容
        m.update(run_config.encode('utf-8'))
        # 计算hash值
        md5_value = m.hexdigest()

        # 检查数据库中md5是否存在
        try:
            print('Search index ...')
            last_config_backup = Deviceconfig.objects.filter(device=device.get('id')).order_by('-id')[0]
            if last_config_backup.hash == md5_value:  # 如果本次配置的MD5值,与上一次备份配置的MD5值相同!略过此次操作
                print('The index already exists', device.get('ip'))
            else:
                print('Create index ...', device.get('ip'))
                save_config()
        except IndexError as a:
            print('Create index ...', device.get('ip'))
            save_config()

    # 其他思科设备配置备份
    else:
        # 建立SSH连接
        cisco_ssh = netmiko.Netmiko(device_type='cisco_ios', ip=device.get('ip'), username=device.get('username'), password=device.get('password'), secret=device.get('enable_pwd'))
        # 启用enable进入特权模式
        cisco_ssh.enable()
        # 执行命令
        result = cisco_ssh.send_config_set([ios_cmd])
        # 关闭连接
        cisco_ssh.disconnect()
        # 返回结果是列表，每一行字符串都是单独的元素
        list_run_config = result.split('\n')

        # 初始下标
        location = 0
        host_location = 0  # 用来找到hostname出现的位置，可以用global变量代替
        for i in list_run_config:
            if re.match('hostname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1

        # 截取hostname开始往后的部分
        list_run_config = list_run_config[host_location:-2]
        # 还原配置 join() 将序列使用指定字符串连接生成新的字符串
        run_config = '\n'.join(list_run_config)
        # 指定hash算法
        m = hashlib.md5()
        # 传入需要hash的内容
        m.update(run_config.encode('utf-8'))
        # 计算hash值
        md5_value = m.hexdigest()

        # 检查数据库中md5是否存在
        try:
            print('Search index ...')
            last_config_backup = Deviceconfig.objects.filter(device=device.get('id')).order_by('-id')[0]
            if last_config_backup.hash == md5_value:  # 如果本次配置的MD5值,与上一次备份配置的MD5值相同!略过此次操作
                print('The index already exists', device.get('ip'))
            else:
                print('Create index ...', device.get('ip'))
                save_config()
        except IndexError as a:
            print('Create index ...', device.get('ip'))
            save_config()


if __name__ == '__main__':
    ssh_single_cmd({'ip': '192.168.20.4', 'username': 'admin', 'password': 'xxxx', 'enable_pwd': 'xxxx', 'id': 4, 'type_name': 'ASA Firewall', 'device_name': 'ASA'})
