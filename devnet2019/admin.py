from django.contrib import admin
from devnet2019.models import SNMPtype, DeviceSNMP, Sidebar, Navbar, Department, DepartTitle, Devicetype, ApplicationMap


admin.site.register(SNMPtype)
admin.site.register(Devicetype)
admin.site.register(Sidebar)
admin.site.register(Navbar)
admin.site.register(DeviceSNMP)
admin.site.register(Department)
admin.site.register(DepartTitle)
admin.site.register(ApplicationMap)

