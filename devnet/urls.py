"""devnet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from devnet2019.views import devnet_home, devnet_device_mgmt, devnet_device_monitor_cpu, \
    devnet_device_monitor_mem, device_monitor_if_speed, device_monitor_if_utilization, \
    device_config, devnet_netflow, devnet_topology, devnet_system_setting_database_lifetime, \
    devnet_system_setting_monitor_interval, devnet_system_setting_threshold_mail, devnet_account, \
    devnet_home_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', devnet_home.home),
    # 主页获取设备健康摘要JSON数据的URL链接
    path('home/reachable', devnet_home_data.health_reachable),
    path('home/cpu', devnet_home_data.health_cpu),
    path('home/mem', devnet_home_data.health_mem),

    # 增加设备
    path('device_mgmt/add_device/', devnet_device_mgmt.add_device),

    # 查看设备
    path('device_mgmt/show_device/', devnet_device_mgmt.show_device),

    # 编辑设备
    path('device_mgmt/editdevice/<int:device_id>', devnet_device_mgmt.edit_device),

    # 删除设备
    path('device_mgmt/deletedevice/<int:device_id>', devnet_device_mgmt.delete_device),

    # 增加设备类型
    path('device_mgmt/add_device_type/', devnet_device_mgmt.add_device_type),

    # 查看设备类型
    path('device_mgmt/show_device_type/', devnet_device_mgmt.show_device_type),

    # 编辑设备类型
    path('device_mgmt/editdevicetype/<int:device_type_id>', devnet_device_mgmt.edit_device_type),

    # 删除设备类型
    path('device_mgmt/deletedevicetype/<int:device_type_id>', devnet_device_mgmt.delete_device_type),

    # CPU监控
    path('device_monitor/cpu/', devnet_device_monitor_cpu.device_monitor_cpu),
    path('device_monitor/cpu/<int:device_id>', devnet_device_monitor_cpu.device_monitor_cpu_device),

    # 内存监控
    path('device_monitor/mem/', devnet_device_monitor_mem.device_monitor_mem),
    path('device_monitor/mem/<int:device_id>', devnet_device_monitor_mem.device_monitor_mem_device),

    # 接口速率监控
    path('device_monitor/if_speed/', device_monitor_if_speed.device_monitor_if_speed),
    path('device_monitor/if_speed/<int:device_id>', device_monitor_if_speed.device_monitor_if_speed_device),
    path('device_monitor/if_speed/<int:interface_id>/<str:direction>', device_monitor_if_speed.device_monitor_if_speed_device_ajax),

    # 接口利用率监控
    path('device_monitor/if_utilization/', device_monitor_if_utilization.device_monitor_if_utilization),
    path('device_monitor/if_utilization/<int:device_id>', device_monitor_if_utilization.device_monitor_if_utilization_device),
    path('device_monitor/if_utilization/<int:interface_id>/<str:direction>', device_monitor_if_utilization.device_monitor_if_utilization_device_ajax),

    # 设备配置备份
    path('device_config/', device_config.device_config),
    path('device_config/backup/', device_config.device_config_backup),
    path('device_config/<int:device_id>', device_config.device_config_dev),
    path('device_config/show/<int:device_id>/<int:id>', device_config.device_show_config),  # 查看特定设备,特定配置备份页面
    path('device_config/delete/<int:device_id>/<int:id>', device_config.device_del_config),  # 删除特定设备的配置备份页面
    path('device_config/download/<int:device_id>/<int:id>', device_config.device_download_config),  # 下载特定设备的配置备份页面
    path('device_config/compare/<int:device_id>/<int:id1>/<int:id2>', device_config.device_config_compare),  # 比较设备配置备份页面

    # netflow
    path('netflow/', devnet_netflow.devnet_netflow),  # Netflow信息
    path('netflow/add_protocol/', devnet_netflow.devnet_netflow_add_protocol),  # Netflow信息
    path('netflow/add_application/', devnet_netflow.devnet_netflow_add_application),  # Netflow信息
    path('netflow/protocol', devnet_netflow.netflow_protocol),  # TOP协议
    path('netflow/top_ip', devnet_netflow.netflow_top_ip),  # TOP IP
    #
    # 拓扑图
    path('topology/', devnet_topology.devnet_topology),
    path('topology_json/', devnet_topology.devnet_topology_json),

    # 系统设置
    path('system_setting/monitor_interval', devnet_system_setting_monitor_interval.monitor_interval),
    path('system_setting/reset_monitor_interval', devnet_system_setting_monitor_interval.reset_monitor_interval),
    path('system_setting/database_lifetime', devnet_system_setting_database_lifetime.database_lifetime),
    path('system_setting/reset_database_lifetime', devnet_system_setting_database_lifetime.reset_database_lifetime),
    path('system_setting/threshold_mail', devnet_system_setting_threshold_mail.threshold_mail),
    path('system_setting/reset_threshold_mail', devnet_system_setting_threshold_mail.reset_threshold_mail),

    # 登录相关界面
    path('accounts/login/', devnet_account.network_login),
    path('accounts/logout/', devnet_account.network_logout),
    path('accounts/register/', devnet_account.network_register),


]