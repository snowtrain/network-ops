#!/usr/bin/env python3

import django
import os
# 添加Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()
import sys
# 在crontab环境下可能会无法找到PYTHONPATH，PYTHONPATH决定python查找lib的路径
sys.path.append('/home/network-ops')
from multiprocessing.pool import ThreadPool
from devnet2019.models import Devicedb, DeviceconfigDir
from modules.devnet_0_ssh_config import ssh_single_cmd

configdir = DeviceconfigDir.objects.get(id=1).dir_name


def get_md5_config():
    devices_list = []
    # 从Devicedb数据库表获取所有的设备信息的清单
    for devices in Devicedb.objects.all():
        # 获取每台设备信息, 构造字典, 然后逐个添加到devices_list列表中
        device_dict = {'ip': devices.ip,
                       'username': devices.ssh_username,
                       'password': devices.ssh_password,
                       'enable_pwd': devices.enable_password,
                       'id': devices.id,
                       'type_name': devices.type.type_name,
                       'device_name': devices.name,
}
        devices_list.append(device_dict)

    # 多线程将 device_list 中元素提取出来(迭代)，当作 ssh_single_cmd 的参数使用
    pool = ThreadPool(processes=5)
    pool.map(ssh_single_cmd, devices_list)
    pool.close()    # 关闭pool,不在加入新的线程
    pool.join()     # 等待每一个线程结束


if __name__ == '__main__':
    get_md5_config()
