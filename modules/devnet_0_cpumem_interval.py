#!/usr/bin/env python3

from devnet2019.models import MonitorInterval


# 获得CPU告警周期
try:
    cpu_max_interval = MonitorInterval.objects.get(name='cpu_max_interval').interval
except MonitorInterval.DoesNotExist:
    # 给告警周期设置默认值1小时
    c = MonitorInterval(name='cpu_max_interval', interval=1)
    c.save()
    cpu_max_interval = MonitorInterval.objects.get(name='cpu_max_interval').interval

# 获得内存告警周期
try:
    mem_max_interval = MonitorInterval.objects.get(name='mem_max_interval').interval
except MonitorInterval.DoesNotExist:
    # 给告警周期设置默认值1小时
    m = MonitorInterval(name='mem_max_interval', interval=1)
    m.save()
    mem_max_interval = MonitorInterval.objects.get(name='mem_max_interval').interval

