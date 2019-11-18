#!/usr/bin/env python3

from django.shortcuts import render

from devnet2019.forms import NetFlowProtocol, NetFlowApplication
from devnet2019.models import NetflowClassicSeven, ApplicationMap, FieldTypeMap
from django.http import JsonResponse
from django.db.models import Count


def devnet_netflow(request):  # 设备配置默认页面

    return render(request, 'devnet_netflow.html', locals())


def devnet_netflow_add_protocol(request):  # 设备配置默认页面
    if request.method == 'POST':
        form = NetFlowProtocol(request.POST)
        if form.is_valid():
            p = FieldTypeMap(field_id=request.POST.get('protocol_number'),
                             field_name=request.POST.get('field_types'))
            p.save()
            successmessage = '协议添加成功'
            return render(request, 'devnet_netflow_add_protocol.html', locals())
        else:
            return render(request, 'devnet_netflow_add_protocol.html', locals())
    else:
        form = NetFlowProtocol()
        return render(request, 'devnet_netflow_add_protocol.html', locals())


def devnet_netflow_add_application(request):  # 设备配置默认页面
    if request.method == 'POST':
        form = NetFlowApplication(request.POST)
        if form.is_valid():
            a = ApplicationMap(pro_dst_port=request.POST.get('pro_dst_post'),
                               application_name=request.POST.get('application_name'))
            a.save()
            successmessage = '应用添加成功'
            return render(request, 'devnet_netflow_add_application.html', locals())
        else:
            return render(request, 'devnet_netflow_add_application.html', locals())
    else:
        form = NetFlowApplication()
        return render(request, 'devnet_netflow_add_application.html', locals())


def netflow_top_ip(request):
    # 如果想基于回话
    # source_group_by = NetflowClassicSeven.objects.values('ipv4_src_addr', 'ipv4_dst_addr').annotate(Count('ipv4_src_addr'), Count('ipv4_dst_addr'))

    # values()返回包含字典的queryset
    # annotate()：聚合数据库中全部('ipv4_src_addr')的记录，Count：计算数量
    source_group_by = NetflowClassicSeven.objects.values('ipv4_src_addr').annotate(dcount=Count('ipv4_src_addr'))

    ip_list = []
    for src in source_group_by:
        ip_list.append(src.get('ipv4_src_addr'))

    bytes_list = []
    for ip in ip_list:
        # 提取特定源IP地址的入向字节数
        ip_bytes = NetflowClassicSeven.objects.filter(ipv4_src_addr=ip)
        bytes_sum = 0
        # 把每一个源IP的字节数加起来
        for ip_byte in ip_bytes:
            bytes_sum += ip_byte.in_bytes

        # 把每一个源IP地址的字节总数添加到bytes_list中
        bytes_list.append(bytes_sum)

    # 把源IP地址和相应的字节数 通过 zip压缩到一起
    # [('10.1.1.1', 1234), ('10.1.1.2', 3444), ...]
    zip_list = [x for x in zip(ip_list, bytes_list)]

    # 通过sorted + lambda 排序, 排序键值为字节数
    sorted_ip_bytes_list = sorted(zip_list, key=lambda x: x[1], reverse=True)

    # 把排序后的列表,继续分开到源IP清单ip_list和字节数清单bytes_bytes
    ip_list = [x[0] for x in sorted_ip_bytes_list]
    bytes_list = [x[1] for x in sorted_ip_bytes_list]

    # 如果源IP数超过5, 只截取前五
    if len(ip_list) > 5:
        labels = ip_list[:5]
        datas = bytes_list[:5]
    else:  # 如果源IP数量不够5个,保留现有列表
        labels = ip_list
        datas = bytes_list

    colors = ['#ff0000', '#ffff00', '#228b22', '#3342FF', '#524b22']  # 图表颜色码列表
    # 返回JSON数据,颜色,源IP列表, 源IP累计字节数
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


def netflow_protocol(request):
    # values()返回包含字典的queryset
    # annotate()：聚合数据库中全部('protocol_id', 'dst_port')的记录，Count：计算数量
    application_group_by = NetflowClassicSeven.objects.values('protocol_id', 'dst_port').annotate(Count('protocol_id'), Count('dst_port'))
    # application_group_by = NetflowClassicSeven.objects.filter(record_datetime__gt=datetime.now() - timedelta(hours=24)).values('protocol_id', 'dst_port').annotate(Count('protocol_id'), Count('dst_port'))
    app_list = []

    # 找到出现的应用(协议,目的端口)
    for application in application_group_by:
        app_list.append([application.get('protocol_id'), application.get('dst_port')])
    protocol_list = []
    protocol_bytes = []
    for x in app_list:
        application_bytes = NetflowClassicSeven.objects.filter(protocol_id=x[0], dst_port=x[1])

        # 尝试从数据库中读取应用名，如果没有找到，就以netflow包的原始数据填充protocol_list。
        # 需要事先在数据库中写入协议名称映射关系
        try:
            protocol_list.append(ApplicationMap.objects.get(pro_dst_port=str(x[0]) + '/' + str(x[1])).application_name)
        except ApplicationMap.DoesNotExist:
            protocol_list.append(str(x[0]) + '/' + str(x[1]))

        bytes_sum = 0
        # 把每一个应用的字节数加起来
        for application_byte in application_bytes:
            bytes_sum += application_byte.in_bytes

        protocol_bytes.append(bytes_sum)
    zip_list = [x for x in zip(protocol_list, protocol_bytes)]

    # 通过sorted + lambda 排序, 排序键值为字节数
    sorted_pro_data_list = sorted(zip_list, key=lambda x: x[1], reverse=True)
    # 把排序后的列表,继续分开到应用清单protocol_list和字节数清单protocol_bytes
    protocol_list = [x[0] for x in sorted_pro_data_list]
    protocol_bytes = [x[1] for x in sorted_pro_data_list]
    # 如果应用数超过5, 只截取前五
    if len(protocol_list) > 10:
        labels = protocol_list[:10]
        datas = protocol_bytes[:10]
    else:  # 如果应用数量不够5个,保留现有列表
        labels = protocol_list
        datas = protocol_bytes

    colors = ['#ff0000', '#ffff00', '#228b22', '#3342FF', '#524b22']  # 图表颜色码列表
    # 返回JSON数据,颜色,应用名列表, 应用字节数
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})
