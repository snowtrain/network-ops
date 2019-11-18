#!/usr/bin/env python3

from devnet2019.models import MonitorInterval


# 获得CPU最大值监控周期
try:
    cpu_max_interval = MonitorInterval.objects.get(name='cpu_max_interval').interval
except MonitorInterval.DoesNotExist:
    # 给监控周期设置默认值1小时
    c = MonitorInterval(name='cpu_max_interval', interval=1)
    c.save()
    cpu_max_interval = MonitorInterval.objects.get(name='cpu_max_interval').interval

# 获得当前CPU监控周期
try:
    cpu_interval = MonitorInterval.objects.get(name='cpu_interval').interval
except MonitorInterval.DoesNotExist:
    # 给监控周期设置默认值1小时
    c = MonitorInterval(name='cpu_interval', interval=1)
    c.save()
    cpu_interval = MonitorInterval.objects.get(name='cpu_interval').interval

# 获得内存最大值监控周期
try:
    mem_max_interval = MonitorInterval.objects.get(name='mem_max_interval').interval
except MonitorInterval.DoesNotExist:
    # 给监控周期设置默认值1小时
    m = MonitorInterval(name='mem_max_interval', interval=1)
    m.save()
    mem_max_interval = MonitorInterval.objects.get(name='mem_max_interval').interval

# 获得当前内存监控周期
try:
    mem_interval = MonitorInterval.objects.get(name='mem_interval').interval
except MonitorInterval.DoesNotExist:
    # 给监控周期设置默认值1小时
    m = MonitorInterval(name='mem_interval', interval=1)
    m.save()
    mem_interval = MonitorInterval.objects.get(name='mem_interval').interval

# 获得接口速率监控周期
try:
    speed_interval = MonitorInterval.objects.get(name='speed_interval').interval
except MonitorInterval.DoesNotExist:
    # 给监控周期设置默认值1小时
    m = MonitorInterval(name='speed_interval', interval=1)
    m.save()
    speed_interval = MonitorInterval.objects.get(name='speed_interval').interval

# 获得接口利用率监控周期
try:
    utilization_interval = MonitorInterval.objects.get(name='utilization_interval').interval
except MonitorInterval.DoesNotExist:
    # 给监控周期设置默认值1小时
    m = MonitorInterval(name='utilization_interval', interval=1)
    m.save()
    utilization_interval = MonitorInterval.objects.get(name='utilization_interval').interval
