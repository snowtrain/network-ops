from django.db import models


class Department(models.Model):
    # 名称
    name = models.CharField(max_length=100, blank=False)


class DepartTitle(models.Model):
    # 部门
    department = models.OneToOneField(Department, related_name='departtitle', blank=True, null=True, on_delete=models.CASCADE)
    # Title
    title = models.CharField(max_length=600, blank=False)


class Navbar(models.Model):
    # 名称
    name = models.CharField(max_length=100, blank=False)
    # URL
    url = models.CharField(max_length=1000, blank=True)


class Sidebar(models.Model):
    # Navbar
    navbar = models.ForeignKey(Navbar, related_name='Sidebar', blank=True, null=True, on_delete=models.CASCADE)
    # 名称
    name = models.CharField(max_length=100, blank=False)
    # URL
    url = models.CharField(max_length=1000, blank=True)


class Devicetype(models.Model):
    # 设备类型名称
    type_name = models.CharField(max_length=100, unique=True, blank=False)
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)


class SNMPtype(models.Model):
    # SNMP类型
    snmp_type = models.CharField(max_length=100, unique=True, blank=False)
    # SNMP类型名称
    snmp_name = models.CharField(max_length=100, blank=False, null=True)
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)


class DeviceSNMP(models.Model):
    # 设备类型
    device_type = models.ForeignKey(Devicetype, related_name='devicesnmp', blank=True, null=True, on_delete=models.CASCADE)
    # SNMP类型
    snmp_type = models.ForeignKey(SNMPtype, related_name='devicesnmp', blank=True, null=True, on_delete=models.CASCADE)
    # oid
    oid = models.CharField(max_length=999, blank=False, null=True)
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)


class Devicedb(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, unique=True, blank=False)
    # 设备IP地址
    ip = models.GenericIPAddressField(default='1.1.1.1', unique=True)
    # 设备描述信息
    description = models.TextField(blank=True)
    # 设备类型
    type = models.ForeignKey(Devicetype, related_name='device', blank=True, null=True, on_delete=models.CASCADE)
    # SNMP是否激活
    snmp_enable = models.BooleanField(default=False)
    # SNMP只读Community
    snmp_ro_community = models.CharField(max_length=999, blank=False)
    # SNMP读写Community
    snmp_rw_community = models.CharField(max_length=999, blank=True)
    # SSH用户名
    ssh_username = models.CharField(max_length=999, blank=False)
    # SSH密码
    ssh_password = models.CharField(max_length=999, blank=False)
    # 特权密码(ASA必须设置)
    enable_password = models.CharField(max_length=999, blank=True)
    # 修改时间
    change_datetime = models.DateTimeField(null=True, auto_now=True)
    # 创建时间
    create_datetime = models.DateTimeField(null=True, auto_now_add=True)


class DeviceReachable(models.Model):
    # 设备名称
    device = models.ForeignKey(Devicedb, related_name='reachable', blank=True, null=True, on_delete=models.CASCADE)
    # SNMP可达性
    snmp_reachable = models.BooleanField(default=False)
    # SSH可达性
    ssh_reachable = models.BooleanField(default=False)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now_add=True)


class Devicecpu(models.Model):
    # 设备
    device = models.ForeignKey(Devicedb, related_name='cpu_usage', blank=True, null=True, on_delete=models.CASCADE)
    # 当前CPU利用率
    cpu_usage = models.FloatField(default=0, blank=True)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now_add=True)


class Devicemem(models.Model):
    # 设备
    device = models.ForeignKey(Devicedb, related_name='mem_usage', blank=True, null=True, on_delete=models.CASCADE)
    # 当前内存利用率
    mem_usage = models.FloatField(default=0, blank=True)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now_add=True)


class DeviceInterface(models.Model):
    # 设备
    device = models.ForeignKey(Devicedb, related_name='interface', blank=True, null=True, on_delete=models.CASCADE)
    # 接口名称
    interface_name = models.CharField(max_length=999, blank=True, null=True)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now=True)


class DeviceInterfaceState(models.Model):
    # 设备
    interface = models.ForeignKey(DeviceInterface, related_name='interface_state', blank=True, null=True, on_delete=models.CASCADE)
    # 接口状态
    state = models.BooleanField(default=False)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now=True)


class DeviceInterfaceSpeed(models.Model):
    # 设备
    interface = models.OneToOneField(DeviceInterface, related_name='interface_speed', blank=True, null=True, on_delete=models.CASCADE)
    # 接口速率
    speed = models.BigIntegerField(default=0, blank=True, null=True)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now=True)


class DeviceInterfaceInBytes(models.Model):
    # 设备
    interface = models.ForeignKey(DeviceInterface, related_name='interface_in_bytes', blank=True, null=True, on_delete=models.CASCADE)
    # 入向字节数
    in_bytes = models.BigIntegerField(default=0, blank=True, null=True)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now=True)


class DeviceInterfaceOutBytes(models.Model):
    # 设备
    interface = models.ForeignKey(DeviceInterface, related_name='interface_out_bytes', blank=True, null=True, on_delete=models.CASCADE)
    # 出向字节数
    out_bytes = models.BigIntegerField(default=0, blank=True, null=True)
    # 记录时间
    record_datetime = models.DateTimeField(null=True, auto_now=True)


class MonitorInterval(models.Model):
    # 名称
    name = models.CharField(max_length=100, blank=False)
    # 监控周期
    interval = models.IntegerField(blank=False)


class DataBaseLifetime(models.Model):
    # 名称
    name = models.CharField(max_length=100, blank=False)
    # 老化时间
    lifetime = models.IntegerField(blank=False)


class Thresholdcpu(models.Model):
    # CPU 告警阈值
    cpu_threshold = models.IntegerField(default=0, blank=True, null=True)
    # CPU 告警周期
    alarm_interval = models.IntegerField(default=0, blank=True, null=True)


class Thresholdmem(models.Model):
    # 内存 告警阈值
    mem_threshold = models.IntegerField(default=0, blank=True, null=True)
    # 内存 告警周期
    alarm_interval = models.IntegerField(default=0, blank=True, null=True)


class Thresholdsnmp(models.Model):
    # SNMP 告警周期
    alarm_interval = models.IntegerField(default=0, blank=True, null=True)


class Thresholdutilization(models.Model):
    # 接口利用率 告警阈值
    utilization_threshold = models.IntegerField(default=0, blank=True, null=True)
    # 接口利用率 告警周期
    alarm_interval = models.IntegerField(default=0, blank=True, null=True)


class Smtplogindb(models.Model):
    # SMTP邮件服务器
    mailserver = models.CharField(max_length=999, blank=True, null=True)
    # SMTP邮件服务器认证用户名
    mailusername = models.CharField(max_length=999, blank=True, null=True)
    # SMTP邮件服务器认证密码
    mailpassword = models.CharField(max_length=999, blank=True, null=True)
    # 发件人
    mailfrom = models.CharField(max_length=999, blank=True, null=True)
    # 收件人
    mailto = models.CharField(max_length=999, blank=True, null=True)


class LastAlarmCPU(models.Model):
    # 设备
    device = models.OneToOneField(Devicedb, related_name='cpu_last_alarm', blank=True, null=True, on_delete=models.CASCADE)
    # 上次一告警
    last_alarm_datetime = models.DateTimeField(null=True, auto_now=True)


class LastAlarmMEM(models.Model):
    # 设备
    device = models.OneToOneField(Devicedb, related_name='mem_last_alarm', blank=True, null=True, on_delete=models.CASCADE)
    # 上次一告警
    last_alarm_datetime = models.DateTimeField(null=True, auto_now=True)


class LastAlarmUtilization(models.Model):
    # 设备
    interface = models.OneToOneField(DeviceInterface, related_name='utilization_last_alarm', blank=True, null=True, on_delete=models.CASCADE)
    # 上次一告警
    last_alarm_datetime = models.DateTimeField(null=True, auto_now=True)


class LastAlarmSNMP(models.Model):
    # 设备
    device = models.OneToOneField(Devicedb, related_name='snmp_last_alarm', blank=True, null=True, on_delete=models.CASCADE)
    # 上次一告警
    last_alarm_datetime = models.DateTimeField(null=True, auto_now=True)


# 保存设备配置,配置HASH和时间
class Deviceconfig(models.Model):
    # 设备
    device = models.ForeignKey(Devicedb, related_name='config', blank=True, null=True, on_delete=models.CASCADE)
    # 配置HASH值,便于快速比较
    hash = models.CharField(max_length=200, blank=False)
    # 保存的设备配置文件名
    config_filename = models.CharField(max_length=200, blank=False)
    # 备份配置的时间
    backup_datetime = models.DateTimeField(auto_now_add=True)


# 设备配置备份目录
class DeviceconfigDir(models.Model):
    # 设备配置备份目录
    dir_name = models.CharField(max_length=200, blank=False)


# 协议映射
class ApplicationMap(models.Model):
    pro_dst_port = models.CharField(max_length=200, unique=True, blank=False)
    application_name = models.CharField(max_length=200, blank=False)


# 字段映射
class FieldTypeMap(models.Model):
    field_id = models.IntegerField(blank=False, unique=True)
    field_name = models.CharField(max_length=200, null=True, blank=True)


# Netflow数据
class NetflowClassicSeven(models.Model):
    ipv4_src_addr = models.GenericIPAddressField(protocol='IPv4')
    ipv4_dst_addr = models.GenericIPAddressField(protocol='IPv4')
    # ipv6_src_addr = models.GenericIPAddressField(protocol='IPv6')
    # ipv6_dst_addr = models.GenericIPAddressField(protocol='IPv6')
    protocol_id = models.IntegerField(blank=False)
    src_port = models.IntegerField(blank=False)
    dst_port = models.IntegerField(blank=False)
    input_interface_id = models.IntegerField(blank=False)
    in_bytes = models.BigIntegerField(blank=False)
    application = models.ForeignKey(ApplicationMap, related_name='netflow_app', blank=True, null=True, on_delete=models.SET_NULL)
    record_datetime = models.DateTimeField(null=True, auto_now=True)
