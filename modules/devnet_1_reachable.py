#!/usr/bin/env python3

import sys
# 在crontab环境下可能会无法找到PYTHONPATH，PYTHONPATH决定python查找lib的路径
sys.path.append('/home/network-ops')
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()

from multiprocessing.pool import ThreadPool
from modules.devnet_0_ssh_snmp_reachble import ssh_sure_shell_login
from devnet2019.models import Devicedb


def sure_reachable():
    device_list = []
    for device in Devicedb.objects.all():
        device_dict = {'ip': device.ip,
                       'username': device.ssh_username,
                       'password': device.ssh_password,
                       'enable_pwd': device.enable_password,
                       'id': device.id,
                       'type_name': device.type.type_name,
                       'snmp_ro_community': device.snmp_ro_community}
        device_list.append(device_dict)

    # 多线程将 device_list 中元素提取出来(迭代)，当作 ssh_sure_shell_login 的参数使用
    pool = ThreadPool(processes=5)
    pool.map(ssh_sure_shell_login, device_list)
    pool.close()    # 关闭pool,不在加入新的线程
    pool.join()     # 等待每一个线程结束


if __name__ == '__main__':
    sure_reachable()

