from django.contrib import admin
from devnet2019.models import SNMPtype, DeviceSNMP, Devicetype, ApplicationMap, FieldTypeMap, DeviceconfigDir


admin.site.register(SNMPtype)
admin.site.register(Devicetype)
admin.site.register(DeviceSNMP)
admin.site.register(ApplicationMap)
admin.site.register(FieldTypeMap)
admin.site.register(DeviceconfigDir)

