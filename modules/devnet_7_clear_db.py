#!/usr/bin/env python3

import django
import sys
# 在crontab环境下可能会无法找到PYTHONPATH，PYTHONPATH决定python查找lib的路径
sys.path.append('/home/ljtc/dev')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devnet.settings')
django.setup()
from devnet2019.models import Devicedb, DataBaseLifetime, NetflowClassicSeven
from datetime import datetime, timedelta


# 尝试查询 CPU 老化时间，如果查询不到就将老化时间设一个默认值
def get_cpu_db_lifetime():
    try:
        cpu_db_lifetime = DataBaseLifetime.objects.get(name='cpu_lifetime').lifetime
    except DataBaseLifetime.DoesNotExist:
        c = DataBaseLifetime(name='cpu_lifetime',
                             lifetime=24)
        c.save()
        cpu_db_lifetime = DataBaseLifetime.objects.get(name='cpu_lifetime').lifetime
    return cpu_db_lifetime


# 尝试查询 MEM 老化时间，如果查询不到就将老化时间设一个默认值
def get_mem_db_lifetime():
    try:
        mem_db_lifetime = DataBaseLifetime.objects.get(name='mem_lifetime').lifetime
    except DataBaseLifetime.DoesNotExist:
        m = DataBaseLifetime(name='mem_lifetime',
                             lifetime=24)
        m.save()
        mem_db_lifetime = DataBaseLifetime.objects.get(name='mem_lifetime').lifetime
    return mem_db_lifetime


# 尝试查询 可达性 老化时间，如果查询不到就将老化时间设一个默认值
def get_reachable_db_lifetime():
    try:
        reachable_db_lifetime = DataBaseLifetime.objects.get(name='reachable_lifetime').lifetime
    except DataBaseLifetime.DoesNotExist:
        m = DataBaseLifetime(name='reachable_lifetime',
                             lifetime=24)
        m.save()
        reachable_db_lifetime = DataBaseLifetime.objects.get(name='reachable_lifetime').lifetime
    return reachable_db_lifetime


# 尝试查询 接口数据 老化时间，如果查询不到就将老化时间设一个默认值
def get_interface_db_lifetime():
    try:
        interface_db_lifetime = DataBaseLifetime.objects.get(name='interface_lifetime').lifetime
    except DataBaseLifetime.DoesNotExist:
        m = DataBaseLifetime(name='interface_lifetime',
                             lifetime=24)
        m.save()
        interface_db_lifetime = DataBaseLifetime.objects.get(name='interface_lifetime').lifetime
    return interface_db_lifetime


# 尝试查询 netflow 老化时间，如果查询不到就将老化时间设一个默认值
def get_netflow_db_lifetime():
    try:
        netflow_db_lifetime = DataBaseLifetime.objects.get(name='netflow_lifetime').lifetime
    except DataBaseLifetime.DoesNotExist:
        m = DataBaseLifetime(name='netflow_lifetime',
                             lifetime=24)
        m.save()
        netflow_db_lifetime = DataBaseLifetime.objects.get(name='netflow_lifetime').lifetime
    return netflow_db_lifetime


# 清除 CPU使用率、内存使用率、接口状态、接口入向字节、出向字节 的已老化数据
def clear_db():
    for device in Devicedb.objects.all():
        need_clear_reachable_db = device.reachable.filter(record_datetime__lte=datetime.now() - timedelta(hours=get_reachable_db_lifetime()))
        need_clear_reachable_db.delete()

        need_clear_cpu_db = device.cpu_usage.filter(record_datetime__lte=datetime.now() - timedelta(hours=get_cpu_db_lifetime()))
        need_clear_cpu_db.delete()

        need_clear_mem_db = device.mem_usage.filter(record_datetime__lte=datetime.now() - timedelta(hours=get_mem_db_lifetime()))
        need_clear_mem_db.delete()

        interface_all = device.interface.all()
        for x in interface_all:
            need_clear_interface_state_db = x.interface_state.filter(record_datetime__lte=datetime.now() - timedelta(hours=get_interface_db_lifetime()))
            need_clear_interface_state_db.delete()
            need_clear_interface_in_bytes_db = x.interface_in_bytes.filter(record_datetime__lte=datetime.now() - timedelta(hours=get_interface_db_lifetime()))
            need_clear_interface_in_bytes_db.delete()
            need_clear_interface_out_bytes_db = x.interface_out_bytes.filter(record_datetime__lte=datetime.now() - timedelta(hours=get_interface_db_lifetime()))
            need_clear_interface_out_bytes_db.delete()


# 清除老化的netflow数据
def clear_netflowdb():
    need_clear_netflow_db = NetflowClassicSeven.objects.filter(record_datetime__lte=datetime.now() - timedelta(hours=get_netflow_db_lifetime()))
    need_clear_netflow_db.delete()


if __name__ == '__main__':
    clear_db()
    clear_netflowdb()
