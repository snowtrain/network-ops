#!/usr/bin/env python3

import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from difflib import Differ
import os
from devnet2019.models import Devicedb, Deviceconfig, DeviceconfigDir
configdir = DeviceconfigDir.objects.get(id=1).dir_name


def device_config(request):  # 设备配置默认页面
    # 从Devicedb数据库表获取所有的设备信息的清单
    devices = Devicedb.objects.all()
    devices_list = []
    # 产生包含所有设备名称的列表devices_list
    for x in devices:
        devices_list.append({'id': x.id, 'name': x.name})
    try:
        # 取出第一个设备对象
        current_device_obj = devices[0]
        # 设备配置的默认页面，使用清单中的第一台设备
        current = current_device_obj.name
        current_device_id = current_device_obj.id
        # 在Deviceconfig中找到第一个设备的配置信息,按照时间倒序排序
        deviceconfig = Deviceconfig.objects.filter(device=current_device_obj).order_by('-backup_datetime')
        device_config_date_hash = []
        for x in deviceconfig:
            # 获取第一台设备的所有配置备份信息, 构造字典, 然后逐个添加到device_config_date_hash列表中
            device_config_date_hash.append({
                                            # 设备名称
                                            'name': current,
                                            # 配置MD5值
                                            'hash': x.hash,
                                            # 配置唯一ID
                                            'id': x.id,
                                            # 配置备份时间
                                            'date': x.backup_datetime.strftime('%Y-%m-%d %H:%M'),
                                            # 删除配置链接
                                            'delete_url': '/device_config/delete/' + str(current_device_id) + '/' + str(x.id),
                                            # 查看配置链接
                                            'show_url': '/device_config/show/' + str(current_device_id) + '/' + str(x.id),
                                            # 下载配置链接
                                            'download_url': '/device_config/download/' + str(current_device_id) + '/' + str(+ x.id)
                                            })
        # 返回device_config.html页面, 与相应数据
        return render(request, 'device_config.html', locals())

    except Exception:
        # 如果出现问题, 返回device_config.html页面
        return render(request, 'device_config.html')


def device_config_dev(request, device_id):  # 特定设备的设备配置页面
    # 从Devicedb数据库表获取所有的设备信息的清单
    devices = Devicedb.objects.all()
    devices_list = []
    # 产生包含所有设备名称的列表devices_list
    for x in devices:
        devices_list.append({'id': x.id, 'name': x.name})
    try:
        # 取出第一个设备对象
        current_device_obj = Devicedb.objects.get(id=device_id)
        # 设备配置的默认页面，使用清单中的第一台设备
        current = current_device_obj.name
        current_device_id = current_device_obj.id
        # 在Deviceconfig中找到第一个设备的配置信息,按照时间倒序排序
        deviceconfig = Deviceconfig.objects.filter(device=current_device_obj).order_by('-backup_datetime')
        device_config_date_hash = []
        for x in deviceconfig:
            # 获取第一台设备的所有配置备份信息, 构造字典, 然后逐个添加到device_config_date_hash列表中
            device_config_date_hash.append({
                                            # 设备名称
                                            'name': current,
                                            # 配置MD5值
                                            'hash': x.hash,
                                            # 配置唯一ID
                                            'id': x.id,
                                            # 配置备份时间
                                            'date': x.backup_datetime.strftime('%Y-%m-%d %H:%M'),
                                            # 删除配置链接
                                            'delete_url': '/device_config/delete/' + str(current_device_id) + '/' + str(x.id),
                                            # 查看配置链接
                                            'show_url': '/device_config/show/' + str(current_device_id) + '/' + str(x.id),
                                            # 下载配置链接
                                            'download_url': '/device_config/download/' + str(current_device_id) + '/' + str(+ x.id)
                                            })
        # 返回device_config.html页面, 与相应数据
        return render(request, 'device_config.html', locals())

    except Exception:
        # 如果出现问题, 返回device_config.html页面
        return render(request, 'device_config.html')


def device_show_config(request, device_id, id):  # 查看特定设备, 特定ID配置备份页面
    # 从数据库Deviceconfig中获取特定设备,特定ID的对象
    device = Devicedb.objects.get(id=device_id)
    deviceconfig = Deviceconfig.objects.get(device=device, id=id)

    # 提取设备名
    devicename = device.name
    # 格式化备份时间
    date = deviceconfig.backup_datetime.strftime('%Y-%m-%d %H:%M')
    # 打开指定配置文件
    config = open(configdir + deviceconfig.config_filename, 'r').read()
    # 返回show_config.html页面
    return render(request, 'show_config.html', locals())


def device_del_config(request, device_id, id):  # 删除特定设备, 特定ID配置
    # 从数据库Deviceconfig删除特定设备, 特定ID配置备份的条目
    device = Devicedb.objects.get(id=device_id)
    deviceconfig = Deviceconfig.objects.get(device=device, id=id)
    deviceconfig.delete()
    # 删除保存的配置文件
    os.remove(configdir + deviceconfig.config_filename)

    # 删除后, 重定向到查看特定设备备份配置页面
    return HttpResponseRedirect('/device_config/' + str(device_id))


def device_download_config(request, device_id, id):
    # 获取特定设备, 特定ID配置备份条目
    device = Devicedb.objects.get(id=device_id)
    deviceconfig = Deviceconfig.objects.get(device=device, id=id)
#
    # 由于下载系统为win!所以需要替换linux的换行符\n到win的换行符'\r\n'
    config_content = open(configdir + deviceconfig.config_filename, 'r').read()
    content = config_content.replace('\n', '\r\n')
    # 配置HTTP响应内容为content(文件内容), content_type='text/plain'
    response = HttpResponse(content, content_type='text/plain')
    # 'Content-Disposition' 是 MIME 协议的扩展，MIME 协议指示 MIME 用户代理如何显示附加的文件。
    # 'attachment' 表示以附件的方式打开，filename表示附件名，如果附件名存在中文需要进行编码
    response['Content-Disposition'] = 'attachment; filename={0}'.format(deviceconfig.config_filename).encode('utf-8')
    return response


def device_config_compare(request, device_id, id1, id2):
    device = Devicedb.objects.get(id=device_id)

    # 获取特定设备的配置1
    deviceconfig1 = Deviceconfig.objects.get(device=device, id=id1)
    # 使用'\r\n'或者'\n'分割设备配置1成为列表
    config1_list = re.split('\r\n|\n', open(configdir + deviceconfig1.config_filename, 'r').read())

    # 获取特定设备的配置2
    deviceconfig2 = Deviceconfig.objects.get(device=device, id=id2)
    # 使用'\r\n'或者'\n'分割设备配置2成为列表
    config2_list = re.split('\r\n|\n', open(configdir + deviceconfig2.config_filename, 'r').read())

    # 使用Python内置的Differ()进行对比
    result = Differ().compare(config1_list, config2_list)
#
    # 把比较的结果恢复到正常的文本
    compare_result = '\r\n'.join(list(result))
    devicename = device.name
#
    # 返回compare_config.html页面
    return render(request, 'compare_config.html', locals())


def device_config_backup(request):
    from modules.devnet_4_get_config_md5 import get_md5_config
    get_md5_config()
    return render(request, 'device_config.html')
