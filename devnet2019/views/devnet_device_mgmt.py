#!/usr/bin/env python3

from datetime import datetime, timedelta
from django.db.models import Max
from django.shortcuts import render, HttpResponseRedirect
from devnet2019.forms import AddDevice, AddDeviceType, EditDeviceType, EditDevice
from devnet2019.models import Devicedb, Devicetype, DeviceSNMP, SNMPtype
from modules.devnet_0_cpumem_interval import cpu_max_interval, mem_max_interval


def add_device_type(request):
    if request.method == 'POST':
        form = AddDeviceType(request.POST)
        if form.is_valid():
            device_type_name = request.POST.get('device_type_name')

            oid_list = []
            cpu_usage = request.POST.get('cpu_usage')
            oid_list.append(['cpu_usage', cpu_usage])
            mem_usage = request.POST.get('mem_usage')
            oid_list.append(['mem_usage', mem_usage])
            mem_free = request.POST.get('mem_free')
            oid_list.append(['mem_free', mem_free])
            if_name = request.POST.get('if_name')
            oid_list.append(['if_name', if_name])
            if_speed = request.POST.get('if_speed')
            oid_list.append(['if_speed', if_speed])
            if_state = request.POST.get('if_state')
            oid_list.append(['if_state', if_state])
            if_in_bytes = request.POST.get('if_in_bytes')
            oid_list.append(['if_in_bytes', if_in_bytes])
            if_out_bytes = request.POST.get('if_out_bytes')
            oid_list.append(['if_out_bytes', if_out_bytes])

            # 设备类型表指保存设备name
            d = Devicetype(type_name=device_type_name)
            d.save()

            # 提取OID列表分别写入
            for x in oid_list:
                # 第一次添加设备类型前将下面2行恢复，否则snmptype表无数据
                # f = SNMPtype(snmp_type=x[0])
                # f.save()
                ds = DeviceSNMP(device_type=d,
                                snmp_type=SNMPtype.objects.get(snmp_type=x[0]),
                                oid=x[1])
                ds.save()
            successmessage = '设备类型添加成功!'
            return render(request, 'devnet_add_device_type.html', locals())
        else:
            return render(request, 'devnet_add_device_type.html', locals())
    else:
        form = AddDeviceType()
        return render(request, 'devnet_add_device_type.html', locals())


def show_device_type(request):
    device_type_list = []
    for devicetype in Devicetype.objects.all().order_by('id'):
        device_type_dict = {'id_delete': '/device_mgmt/deletedevicetype/' + str(devicetype.id),
                            'id_edit': '/device_mgmt/editdevicetype/' + str(devicetype.id),
                            'name': devicetype.type_name}
        device_type_list.append(device_type_dict)
    return render(request, 'devnet_show_device_type.html', locals())


def edit_device_type(request, device_type_id):
    if request.method == 'POST':
        form = EditDeviceType(request.POST)
        if form.is_valid():
            if request.user.has_perm('devnet2019.change_devicedb'):
                device_id = request.POST.get('device_id')
                device_type_name = request.POST.get('device_type_name')

                # 修改设备类型名称
                d1 = Devicetype(id=request.POST.get('device_id'),
                                type_name=request.POST.get('device_type_name'))
                d1.save()

                # 存储OID列表，包含OID_name和OID
                oid_list = []
                cpu_usage = request.POST.get('cpu_usage')
                oid_list.append(['cpu_usage', cpu_usage])
                mem_usage = request.POST.get('mem_usage')
                oid_list.append(['mem_usage', mem_usage])
                mem_free = request.POST.get('mem_free')
                oid_list.append(['mem_free', mem_free])
                if_name = request.POST.get('if_name')
                oid_list.append(['if_name', if_name])
                if_speed = request.POST.get('if_speed')
                oid_list.append(['if_speed', if_speed])
                if_state = request.POST.get('if_state')
                oid_list.append(['if_state', if_state])
                if_in_bytes = request.POST.get('if_in_bytes')
                oid_list.append(['if_in_bytes', if_in_bytes])
                if_out_bytes = request.POST.get('if_out_bytes')
                oid_list.append(['if_out_bytes', if_out_bytes])

                d = Devicetype.objects.get(id=device_id)

                for x in oid_list:
                    device_snmp_oid = d.devicesnmp.get(snmp_type__snmp_type=x[0])
                    device_snmp_oid.oid = x[1]
                    device_snmp_oid.save()
            else:
                err = '没有权限'
                return render(request, '404.html', locals())
            successmessage = '设备类型编辑成功!'
            return render(request, 'devnet_edit_device_type.html', locals())

        else:
            return render(request, 'devnet_edit_device_type.html', locals())
    else:
        dt = Devicetype.objects.get(id=device_type_id)
        # django数据库双下划线操作。
        # django数据库中没有连表的操作，没有sqlalchemy中的join操作，它使用了一种更简洁的操作‘__’, 双下划线。
        # 使用双下划线可以完成连表操作，可以正向查询，也可以反向查询。
        form = EditDeviceType(initial={'device_id': device_type_id,
                                       'device_type_name': dt.type_name,
                                       'cpu_usage': dt.devicesnmp.get(snmp_type__snmp_type='cpu_usage').oid,
                                       'mem_usage': dt.devicesnmp.get(snmp_type__snmp_type='mem_usage').oid,
                                       'mem_free': dt.devicesnmp.get(snmp_type__snmp_type='mem_free').oid,
                                       'if_name': dt.devicesnmp.get(snmp_type__snmp_type='if_name').oid,
                                       'if_speed': dt.devicesnmp.get(snmp_type__snmp_type='if_speed').oid,
                                       'if_state': dt.devicesnmp.get(snmp_type__snmp_type='if_state').oid,
                                       'if_in_bytes': dt.devicesnmp.get(snmp_type__snmp_type='if_in_bytes').oid,
                                       'if_out_bytes': dt.devicesnmp.get(snmp_type__snmp_type='if_out_bytes').oid,
                                       })
        return render(request, 'devnet_edit_device_type.html', locals())


def delete_device_type(request, device_type_id):
    if request.user.has_perm('devnet2019.delete_devicetype'):
        d = Devicetype.objects.get(id=device_type_id)
        d.delete()
    else:
        err = '没有权限'
        return render(request, '404.html', locals())
    return HttpResponseRedirect('/device_mgmt/show_device_type/')


def add_device(request):
    if request.method == 'POST':
        form = AddDevice(request.POST)
        if form.is_valid():
            # 把设备信息写入Devicedb数据库
            d1 = Devicedb(name=request.POST.get('name'),
                          ip=request.POST.get('ip'),
                          description=request.POST.get('description'),
                          type=Devicetype.objects.get(id=int(request.POST.get('type'))),
                          snmp_enable=request.POST.get('snmp_enable'),
                          snmp_ro_community=request.POST.get('snmp_ro_community'),
                          snmp_rw_community=request.POST.get('snmp_rw_community'),
                          ssh_username=request.POST.get('ssh_username'),
                          ssh_password=request.POST.get('ssh_password'),
                          enable_password=request.POST.get('enable_password'), )
            d1.save()
            successmessage = '设备添加成功!'
            # locls()返回一个包含当前作用域里面的所有变量和它们的值的字典。
            return render(request, 'devnet_add_device.html', locals())
        else:
            return render(request, 'devnet_add_device.html', locals())
    else:
        form = AddDevice()
        return render(request, 'devnet_add_device.html', locals())


def show_device(request):
    # 查询整个Devicedb信息
    result = Devicedb.objects.all()
    devices_list = []
    # 获取每个设备信息
    for x in result:
        # 产生设备信息的字典
        devices_dict = {'id_delete': "/device_mgmt/deletedevice/" + str(x.id),  # 删除设备URL
                        'id_edit': "/device_mgmt/editdevice/" + str(x.id),      # 编辑设备URL
                        'name': x.name,                                         # 设备名称
                        'ip': x.ip}                                             # 设备IP地址
        try:
            # 取最新的SNMP和SSH可达信息
            reachable_info = x.reachable.all().order_by('-id')[0]
            if reachable_info.snmp_reachable:
                devices_dict['snmp_reachable'] = '正常'
            else:
                devices_dict['snmp_reachable'] = '失败'

            if reachable_info.ssh_reachable:
                devices_dict['ssh_reachable'] = '正常'
            else:
                devices_dict['ssh_reachable'] = '失败'
        except IndexError:
            devices_dict['snmp_reachable'] = '失败'
            devices_dict['ssh_reachable'] = '失败'

        try:
            # 取CPU最大利用率。
            # record_datetime__gt表示数据库记录时间record_datetime大于上一次告警时间
            # timedelta代表两个datetime之间的时间。
            # datetime.now() - timedelta(hours=cpu_max_interval)是当前时间减去告警周期（默认一个小时）
            # Max获取指定对象的最大值
            devices_dict['cpu_max'] = x.cpu_usage.filter(
                record_datetime__gt=datetime.now() - timedelta(hours=cpu_max_interval)).aggregate(Max('cpu_usage')).get('cpu_usage__max')
            # 取当前CPU利用率
            devices_dict['cpu_current'] = x.cpu_usage.filter(record_datetime__gt=datetime.now() - timedelta(minutes=1)).order_by('-id')[0].cpu_usage
        except IndexError:
            devices_dict['cpu_max'] = 'None'
            devices_dict['cpu_current'] = 'None'

        try:
            # 取内存最大利用率。
            # record_datetime__gt表示数据库记录时间record_datetime大于上一次告警时间
            # timedelta代表两个datetime之间的时间。
            # datetime.now() - timedelta(hours=cpu_max_interval)是当前时间减去告警周期（默认一个小时）
            # Max获取指定对象的最大值
            devices_dict['mem_max'] = x.mem_usage.filter(
                record_datetime__gt=datetime.now() - timedelta(hours=mem_max_interval)).aggregate(Max('mem_usage')).get('mem_usage__max')
            # 取当前内存利用率
            devices_dict['mem_current'] = x.mem_usage.filter(record_datetime__gt=datetime.now() - timedelta(minutes=1)).order_by('-id')[0].mem_usage
        except IndexError:
            devices_dict['mem_max'] = 'None'
            devices_dict['mem_current'] = 'None'

        if_count = 0
        for if_info in x.interface.all():
            try:
                # 如果再1分钟内接口状态为UP并且接口双向bytes不为空，则将接口数量加1
                if if_info.interface_state.filter(record_datetime__gt=datetime.now() - timedelta(minutes=1)).order_by('-id')[0].state and \
                        if_info.interface_in_bytes.filter(record_datetime__gt=datetime.now() - timedelta(minutes=1)).order_by('-id')[0].in_bytes and \
                        if_info.interface_out_bytes.filter(record_datetime__gt=datetime.now() - timedelta(minutes=1)).order_by('-id')[0].out_bytes:
                    if_count += 1
            except IndexError:
                if_count = 0

        devices_dict['ifs'] = if_count
        # 把设备信息添加到字典,再添加到devices_list清单
        devices_list.append(devices_dict)
    return render(request, 'devnet_show_devices.html', locals())


def edit_device(request, device_id):
    if request.method == 'POST':
        form = EditDevice(request.POST)
        type = Devicetype.objects.get(id=int(request.POST.get('type')))
        if form.is_valid():
            # 判断用户是否有变更该表的权限
            if request.user.has_perm('devnet2019.change_devicedb'):
                d1 = Devicedb(id=request.POST.get('id'),
                              name=request.POST.get('name'),
                              ip=request.POST.get('ip'),
                              description=request.POST.get('description'),
                              type=Devicetype.objects.get(id=int(request.POST.get('type'))),
                              snmp_enable=request.POST.get('snmp_enable'),
                              snmp_ro_community=request.POST.get('snmp_ro_community'),
                              snmp_rw_community=request.POST.get('snmp_rw_community'),
                              ssh_username=request.POST.get('ssh_username'),
                              ssh_password=request.POST.get('ssh_password'),
                              enable_password=request.POST.get('enable_password'), )
                d1.save()
                successmessage = '设备修改成功!'
            else:
                err = '没有权限'
                return render(request, '404.html', locals())

            # locls()返回一个包含当前作用域里面的所有变量和它们的值的字典。
            return render(request, 'devnet_edit_device.html', locals())
        else:
            return render(request, 'devnet_edit_device.html', locals())
    else:
        d = Devicedb.objects.get(id=device_id)
        form = EditDevice(initial={'id': d.id,
                                   'name': d.name,
                                   'ip': d.ip,
                                   'description': d.description,
                                   'type': d.type.id,
                                   'snmp_enable': d.snmp_enable,
                                   'snmp_ro_community': d.snmp_ro_community,
                                   'snmp_rw_community': d.snmp_rw_community,
                                   'ssh_username': d.ssh_username,
                                   'ssh_password': d.ssh_password,
                                   'enable_password': d.enable_password
                                   })
        return render(request, 'devnet_edit_device.html', locals())


def delete_device(request, device_id):
    if request.user.has_perm('devnet2019.delete_devicedb'):
        d = Devicedb.objects.get(id=device_id)
        d.delete()
    else:
        err = '没有权限'
        return render(request, '404.html', locals())
    return HttpResponseRedirect('/device_mgmt/show_device.html')

