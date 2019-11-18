from django import forms
from django.core.validators import RegexValidator
from devnet2019.models import Devicetype, Devicedb, FieldTypeMap, ApplicationMap


# 添加设备类型
class AddDeviceType(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'

    # 设备类型名称
    device_type_name = forms.CharField(label='设备类型名称',
                                       widget=forms.TextInput(attrs={"class": "form-control"}))

    # CPU利用率
    cpu_usage = forms.CharField(label='CPU利用率 OID',
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    # 内存使用
    mem_usage = forms.CharField(label='内存使用 OID',
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    # 内存闲置
    mem_free = forms.CharField(label='内存闲置 OID',
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口名称
    if_name = forms.CharField(label='接口名称 OID',
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口速率
    if_speed = forms.CharField(label='接口速率 OID',
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口状态
    if_state = forms.CharField(label='接口状态 OID',
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口入向字节数
    if_in_bytes = forms.CharField(label='接口入向字节数 OID',
                                  widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口出向字节数
    if_out_bytes = forms.CharField(label='接口出向字节数 OID',
                                   widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_device_type_name(self):
        device_type_name = self.cleaned_data['device_type_name']
        try:
            Devicetype.objects.get(type_name=device_type_name)
            raise forms.ValidationError("设备类型已存在!")
        except Devicetype.DoesNotExist:
            return device_type_name


# 编辑设备类型
class EditDeviceType(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'

    device_id = forms.IntegerField(label='设备类型ID',
                                   required=True,
                                   widget=forms.TextInput(attrs={"class": "form-control", 'readonly': True}))

    # 设备类型名称
    device_type_name = forms.CharField(label='设备类型名称',
                                       widget=forms.TextInput(attrs={"class": "form-control"}))

    # CPU利用率
    cpu_usage = forms.CharField(label='CPU一分钟利用率 OID',
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    # 内存使用
    mem_usage = forms.CharField(label='内存使用 OID',
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    # 内存闲置
    mem_free = forms.CharField(label='内存闲置 OID',
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口名称
    if_name = forms.CharField(label='接口名称 OID',
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口速率
    if_speed = forms.CharField(label='接口速率 OID',
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口状态
    if_state = forms.CharField(label='接口状态 OID',
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口入向字节数
    if_in_bytes = forms.CharField(label='接口入向字节数 OID',
                                  widget=forms.TextInput(attrs={"class": "form-control"}))

    # 接口出向字节数
    if_out_bytes = forms.CharField(label='接口出向字节数 OID',
                                   widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_device_type_name(self):
        device_type_name = self.cleaned_data['device_type_name']
        device_id = self.cleaned_data['device_id']
        try:
            if device_id != Devicetype.objects.get(type_name=device_type_name).id:
                raise forms.ValidationError("设备类型已存在!")
            else:
                return device_type_name
        except Devicetype.DoesNotExist:
            return device_type_name


# 添加设备表单
class AddDevice(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    name = forms.CharField(max_length=100,
                           min_length=2,
                           label='设备名称',
                           required=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    # 类型为GenericIPAddressField,可以对输入的IP地址进行校验
    ip = forms.GenericIPAddressField(required=True,
                                     label='IP地址',
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="设备描述",
                                  required=False,
                                  # 输入为Textarea,支持多行输入,"rows": 3 控制展示的行数
                                  widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    # 选择的设备类型
    type_choices = []
    devicetype = Devicetype.objects.all()
    for x in devicetype:
        type_choices.append([x.id, x.type_name])
    type = forms.CharField(label='设备类型',
                           required=True,
                           widget=forms.Select(choices=type_choices,
                                               attrs={"class": "form-control"}))
    TRUE_FALSE_CHOICES = ((True, 'Yes'), (False, 'No'))
    snmp_enable = forms.ChoiceField(label='是否激活SNMP',
                                    required=True,
                                    choices=TRUE_FALSE_CHOICES,
                                    initial=False,
                                    widget=forms.Select(attrs={"class": "required checkbox form-control"}))
    community_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                     message="SNMP community 只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    snmp_ro_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP只读',
                                        required=True,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    snmp_rw_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP读写',
                                        required=False,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    username_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="用户名只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_username = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH用户名',
                                   required=True,
                                   validators=[username_regex],
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_password = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH密码',
                                   required=True,
                                   validators=[password_regex],
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    enable_password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                           message="特权密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    enable_password = forms.CharField(max_length=100,
                                      min_length=2,
                                      label='特权密码',
                                      required=False,
                                      validators=[enable_password_regex],
                                      widget=forms.PasswordInput(attrs={"class": "form-control"}))

    # 校验设备名称不能重复, 在此系统中,设备并没有指定唯一ID,设备名就是唯一ID,不能重复
    def clean_name(self):
        name = self.cleaned_data['name']  # 提取客户输入的设备名
        # 在数据库中查找是否存在这个设备名，exists()：判断查询集中是否有数据，如果有就返回true，没有返回false
        existing = Devicedb.objects.filter(name=name).exists()
        # 如果存在就显示校验错误信息
        if existing:
            raise forms.ValidationError("设备名不能重复")
        # 如果校验成功就返回设备名
        return name

    # 校验IP地址不能重复
    def clean_ip(self):
        ip = self.cleaned_data['ip']  # 提取客户输入的设备IP
        # 在数据库中查找是否存在这个设备IP
        existing = Devicedb.objects.filter(
            ip=ip
        ).exists()
        # 如果存在就显示校验错误信息
        if existing:
            raise forms.ValidationError("设备IP不能重复")
        # 如果校验成功就返回设备IP
        return ip

    # 确认激活SNMP,才能设置只读Community
    def clean_snmp_ro_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_ro_community = self.cleaned_data['snmp_ro_community']
        if snmp_enable == 'True' and snmp_ro_community:
            return snmp_ro_community
        else:
            raise forms.ValidationError("设置只读Community之前请激活SNMP")

    # 确认激活SNMP,才能设置读写Community
    def clean_snmp_rw_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_rw_community = self.cleaned_data['snmp_rw_community']
        if snmp_rw_community:
            if snmp_enable == 'True' and snmp_rw_community:
                return snmp_rw_community
            else:
                raise forms.ValidationError("设置读写Community之前请激活SNMP")
        else:
            return snmp_rw_community


# 修改设备表单
class EditDevice(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'

    id = forms.IntegerField(label='设备ID',
                            required=True,
                            widget=forms.TextInput(attrs={"class": "form-control", 'readonly': True}))

    name = forms.CharField(max_length=100,
                           min_length=2,
                           label='设备名称',
                           required=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    # 类型为GenericIPAddressField,可以对输入的IP地址进行校验
    ip = forms.GenericIPAddressField(required=True,
                                     label='IP地址',
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="设备描述",
                                  required=False,
                                  # 输入为Textarea,支持多行输入,"rows": 3 控制展示的行数
                                  widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    # 选择的设备类型
    type_choices = []
    devicetype = Devicetype.objects.all()
    for x in devicetype:
        type_choices.append([x.id, x.type_name])
    type = forms.CharField(label='设备类型',
                           required=True,
                           widget=forms.Select(choices=type_choices,
                                               attrs={"class": "form-control"}))
    TRUE_FALSE_CHOICES = ((True, 'Yes'), (False, 'No'))
    snmp_enable = forms.ChoiceField(label='是否激活SNMP',
                                    required=True,
                                    choices=TRUE_FALSE_CHOICES,
                                    initial=False,
                                    widget=forms.Select(attrs={"class": "required checkbox form-control"}))
    community_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                     message="SNMP community 只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    snmp_ro_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP只读',
                                        required=True,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    snmp_rw_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP读写',
                                        required=False,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    username_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="用户名只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_username = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH用户名',
                                   required=True,
                                   validators=[username_regex],
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_password = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH密码',
                                   required=True,
                                   validators=[password_regex],
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    enable_password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                           message="特权密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    enable_password = forms.CharField(max_length=100,
                                      min_length=2,
                                      label='特权密码',
                                      required=False,
                                      validators=[enable_password_regex],
                                      widget=forms.PasswordInput(attrs={"class": "form-control"}))

    # # 校验设备名称不能重复, 在此系统中,设备并没有指定唯一ID,设备名就是唯一ID,不能重复
    # def clean_name(self):
    #     name = self.cleaned_data['name']  # 提取客户输入的设备名
    #     # 在数据库中查找是否存在这个设备名，exists()：判断查询集中是否有数据，如果有就返回true，没有返回false
    #     existing = Devicedb.objects.filter(name=name).exists()
    #     # 如果存在就显示校验错误信息
    #     if existing:
    #         raise forms.ValidationError("设备名不能重复")
    #     # 如果校验成功就返回设备名
    #     return name

    # 确认激活SNMP,才能设置只读Community
    def clean_snmp_ro_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_ro_community = self.cleaned_data['snmp_ro_community']
        if snmp_enable == 'True' and snmp_ro_community:
            return snmp_ro_community
        else:
            raise forms.ValidationError("设置只读Community之前请激活SNMP")

    # 确认激活SNMP,才能设置读写Community
    def clean_snmp_rw_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_rw_community = self.cleaned_data['snmp_rw_community']
        if snmp_rw_community:
            if snmp_enable == 'True' and snmp_rw_community:
                return snmp_rw_community
            else:
                raise forms.ValidationError("设置读写Community之前请激活SNMP")
        else:
            return snmp_rw_community


# 系统设置, 监控周期表单
class SysconfigmonitorintervalForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    interval_regex = RegexValidator(regex=r'^\d{1,2}$',
                                    message="监控周期只能支持最多2位整数")
    # CPU监控周期
    cpu_interval = forms.CharField(validators=[interval_regex],
                                   min_length=1,
                                   max_length=2,
                                   label='CPU监控周期（单位小时，默认1小时）',
                                   required=True,
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))

    # CPU最大值计算周期
    cpu_max_interval = forms.CharField(validators=[interval_regex],
                                       min_length=1,
                                       max_length=2,
                                       label='CPU最大值计算周期（单位小时，默认1小时）',
                                       required=True,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))

    # 内存监控周期
    mem_interval = forms.CharField(validators=[interval_regex],
                                   min_length=1,
                                   max_length=2,
                                   label='内存监控周期（单位小时，默认1小时）',
                                   required=True,
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))

    # 内存最大值计算周期
    mem_max_interval = forms.CharField(validators=[interval_regex],
                                       min_length=1,
                                       max_length=2,
                                       label='内存最大值计算周期（单位小时，默认1小时）',
                                       required=True,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 速率监控周期
    speed_interval = forms.CharField(validators=[interval_regex],
                                     min_length=1,
                                     max_length=2,
                                     label='接口速率监控周期（单位小时，默认1小时）',
                                     required=True,
                                     widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 利用率监控周期
    utilization_interval = forms.CharField(validators=[interval_regex],
                                           min_length=1,
                                           max_length=2,
                                           label='接口利用率监控周期（单位小时，默认1小时）',
                                           required=True,
                                           widget=forms.NumberInput(attrs={"class": "form-control"}))


# 系统设置, 数据库监控周期表单
class SysconfigdatabaselifetimeForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    interval_regex = RegexValidator(regex=r'^\d{1,3}$',
                                    message="数据老化时间只能支持最多3位整数")

    # 可达性数据老化时间
    reachable_lifetime = forms.CharField(validators=[interval_regex],
                                         min_length=1,
                                         max_length=3,
                                         label='可达性数据老化时间（单位小时，默认24小时）',
                                         required=True,
                                         widget=forms.NumberInput(attrs={"class": "form-control"}))

    # CPU数据老化时间
    cpu_lifetime = forms.CharField(validators=[interval_regex],
                                   min_length=1,
                                   max_length=3,
                                   label='CPU数据老化时间（单位小时，默认24小时）',
                                   required=True,
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))

    # 内存数据老化时间
    mem_lifetime = forms.CharField(validators=[interval_regex],
                                   min_length=1,
                                   max_length=3,
                                   label='内存数据老化时间（单位小时，默认24小时）',
                                   required=True,
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))

    # 接口数据老化时间
    interface_lifetime = forms.CharField(validators=[interval_regex],
                                         min_length=1,
                                         max_length=3,
                                         label='接口数据老化时间（单位小时，默认24小时）',
                                         required=True,
                                         widget=forms.NumberInput(attrs={"class": "form-control"}))

    # Netflow数据老化时间
    netflow_lifetime = forms.CharField(validators=[interval_regex],
                                       min_length=1,
                                       max_length=3,
                                       label='Netflow数据老化时间（单位小时，默认24小时）',
                                       required=True,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))


# 系统设置, 告警阈值,周期与SMTP相关表单
class Sysconfigthreshold(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    threshold_regex = RegexValidator(regex=r'^1?\d{1,2}$',
                                     message="阈值取值范围为1-100的整数")
    interval_regex = RegexValidator(regex=r'^\d{1,2}$',
                                    message="监控周期只能支持最多2位整数")
    # CPU告警阈值
    cpu_threshold = forms.CharField(validators=[threshold_regex],
                                    min_length=1,
                                    max_length=3,
                                    label='CPU告警阈值（单位%）设置为0表示取消',
                                    required=True,
                                    widget=forms.NumberInput(attrs={"class": "form-control"}))
    # CPU告警周期
    cpu_alarm_interval = forms.CharField(validators=[interval_regex],
                                         min_length=1,
                                         max_length=5,
                                         label='CPU告警周期（单位分钟）',
                                         required=True,
                                         widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 内存告警阈值
    mem_threshold = forms.CharField(validators=[threshold_regex],
                                    min_length=1,
                                    max_length=3,
                                    label='内存告警阈值（单位%）设置为0表示取消',
                                    required=True,
                                    widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 内存告警周期
    mem_alarm_interval = forms.CharField(validators=[interval_regex],
                                         min_length=1,
                                         max_length=5,
                                         label='内存告警周期（单位分钟）',
                                         required=True,
                                         widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 接口利用率告警阈值
    utilization_threshold = forms.CharField(validators=[threshold_regex],
                                            min_length=1,
                                            max_length=3,
                                            label='接口利用率告警阈值（单位%）设置为0表示取消',
                                            required=True,
                                            widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 接口利用率告警周期
    utilization_alarm_interval = forms.CharField(validators=[interval_regex],
                                                 min_length=1,
                                                 max_length=5,
                                                 label='接口利用率告警周期（单位分钟）',
                                                 required=True,
                                                 widget=forms.NumberInput(attrs={"class": "form-control"}))
    # SNMP告警周期
    snmp_alarm_interval = forms.CharField(validators=[interval_regex],
                                          min_length=1,
                                          max_length=5,
                                          label='SNMP告警周期（单位分钟）',
                                          required=True,
                                          widget=forms.NumberInput(attrs={"class": "form-control"}))
    # SMTP邮件服务器
    mailserver = forms.CharField(min_length=1,
                                 max_length=50,
                                 label='邮件服务器',
                                 required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    # SMTP认证用用户名
    mailusername = forms.CharField(min_length=1,
                                   max_length=50,
                                   label='用户名',
                                   required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    # SMTP认证用密码
    mailpassword = forms.CharField(min_length=1,
                                   max_length=50,
                                   label='密码',
                                   required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    # 发件人
    mailfrom = forms.CharField(min_length=1,
                               max_length=50,
                               label='发件人FROM',
                               required=False,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    # 收件人
    mailto = forms.CharField(min_length=1,
                             max_length=50,
                             label='收件人TO',
                             required=False,
                             widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_cpu_alarm_interval(self):
        cpu_threshold = int(self.cleaned_data['cpu_threshold'])
        cpu_alarm_interval = int(self.cleaned_data['cpu_alarm_interval'])

        if (cpu_threshold and cpu_alarm_interval) >= 1:
            pass
        elif cpu_threshold == 0 and cpu_alarm_interval == 0:
            pass
        else:
            raise forms.ValidationError("CPU阈值与告警周期,要么都设置,要么都保持默认的0!不能只设置其中一个!")

    def clean_mem_alarm_interval(self):
        mem_threshold = int(self.cleaned_data['mem_threshold'])
        mem_alarm_interval = int(self.cleaned_data['mem_alarm_interval'])

        if (mem_threshold and mem_alarm_interval) >= 1:
            pass
        elif mem_threshold == 0 and mem_alarm_interval == 0:
            pass
        else:
            raise forms.ValidationError("内存阈值与告警周期,要么都设置,要么都保持默认的0!不能只设置其中一个!")

    def clean_utilization_alarm_interval(self):
        utilization_threshold = int(self.cleaned_data['utilization_threshold'])
        utilization_alarm_interval = int(self.cleaned_data['utilization_alarm_interval'])

        if (utilization_threshold and utilization_alarm_interval) >= 1:
            pass
        elif utilization_threshold == 0 and utilization_alarm_interval == 0:
            pass
        else:
            raise forms.ValidationError("利用率阈值与告警周期,要么都设置,要么都保持默认的0!不能只设置其中一个!")

    def clean_mailto(self):
        mailserver = self.cleaned_data['mailserver']
        mailusername = self.cleaned_data['mailusername']
        mailpassword = self.cleaned_data['mailpassword']
        mailfrom = self.cleaned_data['mailfrom']
        mailto = self.cleaned_data['mailto']

        if mailserver and mailusername and mailpassword and mailfrom and mailto:
            pass
        elif not mailserver and not mailusername and not mailpassword and not mailfrom and not mailto:
            pass
        else:
            raise forms.ValidationError("邮件信息要么全部设置!要么全部保持空!不能只设置其中的一部分!")


class NetFlowProtocol(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    protocol_regex = RegexValidator(regex=r'^\d.*',
                                    message="协议号直接填写数字")
    protocol_type_regex = RegexValidator(regex=r'[A-Z0-9_]+',
                                         message="协议类型格式：IPV4_SRC_ADDR ")

    protocol_number = forms.CharField(validators=[protocol_regex],
                                      min_length=1,
                                      max_length=6,
                                      label='协议号',
                                      required=True,
                                      widget=forms.NumberInput(attrs={"class": "form-control"}))
    field_types = forms.CharField(validators=[protocol_type_regex],
                                  min_length=1,
                                  max_length=100,
                                  label='协议类型',
                                  required=True,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_protocol_number(self):
        protocol_number = self.cleaned_data['protocol_number']
        # 在数据库中查找是否存在这个协议号，exists()：判断查询集中是否有数据，如果有就返回true，没有返回false
        existing = FieldTypeMap.objects.filter(field_id=protocol_number).exists()
        # 如果存在就显示校验错误信息
        if existing:
            raise forms.ValidationError("协议号不能重复")
        # 如果校验成功就返回协议号
        return protocol_number

    def clean_field_types(self):
        field_types = self.cleaned_data['field_types']
        # 在数据库中查找是否存在这个协议类型，exists()：判断查询集中是否有数据，如果有就返回true，没有返回false
        existing = FieldTypeMap.objects.filter(field_name=field_types).exists()
        # 如果存在就显示校验错误信息
        if existing:
            raise forms.ValidationError("协议类型不能重复")
        # 如果校验成功就返回协议类型
        return field_types


class NetFlowApplication(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    pro_dst_post_regex = RegexValidator(regex=r'\d\/\d',
                                        message="格式：17/443 ")
    application_regex = RegexValidator(regex=r'[A-Za-z]+',
                                       message="格式：HTTPS ")
    pro_dst_post = forms.CharField(validators=[pro_dst_post_regex],
                                   min_length=1,
                                   max_length=100,
                                   label='协议/目的端口',
                                   required=True,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    application_name = forms.CharField(validators=[application_regex],
                                       min_length=1,
                                       max_length=100,
                                       label='应用名',
                                       required=True,
                                       widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_pro_dst_post(self):
        pro_dst_post = self.cleaned_data['pro_dst_post']
        # 在数据库中查找是否存在这个协议端口号，exists()：判断查询集中是否有数据，如果有就返回true，没有返回false
        existing = ApplicationMap.objects.filter(pro_dst_port=pro_dst_post).exists()
        # 如果存在就显示校验错误信息
        if existing:
            raise forms.ValidationError("协议和端口号不能重复")
        # 如果校验成功就返回协议端口号
        return pro_dst_post

    # 由于采用的是协议/目的端口号组合，可能一个应用使用不同端口号，所以这里暂时注释！
    # def clean_application_name(self):
    #     application_name = self.cleaned_data['application_name']
    #     # 在数据库中查找是否存在这个应用类型，exists()：判断查询集中是否有数据，如果有就返回true，没有返回false
    #     existing = ApplicationMap.objects.filter(application_name=application_name).exists()
    #     # 如果存在就显示校验错误信息
    #     if existing:
    #         raise forms.ValidationError("应用类型不能重复")
    #     # 如果校验成功就返回应用类型
    #     return application_name


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)


class loginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)

