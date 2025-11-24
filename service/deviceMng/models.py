from django.db import models
from django.utils import timezone
from datetime import datetime


class Device(models.Model):
    DEVICE_TYPE_CHOICES = [
        ('Android', 'Android'),
        ('IOS', 'IOS'),
        ('Mac', 'Mac'),
        ('Windows', 'Windows'),
        ('harmonyOS', 'HarmonyOS'),
        ('other', '其他')
    ]

    STATUS_CHOICES = [
        ('0', '空闲'),
        ('1', '占用'),
        ('2', '申请中')
    ]

    id = models.AutoField(primary_key=True, verbose_name="ID")
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE_CHOICES, verbose_name="设备大类")
    os_name = models.CharField(max_length=50, verbose_name="操作系统")
    os_version = models.CharField(max_length=20, verbose_name="操作系统版本")
    device_model = models.CharField(max_length=50, verbose_name="手机型号")
    asset_code = models.CharField(max_length=20, unique=True, verbose_name="资产编码")
    screen_lock_password = models.CharField(max_length=50, blank=True, null=True, verbose_name="锁屏密码")
    install_password = models.CharField(max_length=50, blank=True, null=True, verbose_name="安装密码")
    processor = models.CharField(max_length=50, verbose_name="芯片处理器")
    owner = models.CharField(max_length=50, verbose_name="所属人")
    current_user = models.CharField(max_length=50, blank=True, null=True, verbose_name="领用人")
    used_days = models.IntegerField(default=0, verbose_name="占用天数（天）")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='0',  # 设置默认值为空闲
        verbose_name="设备状态"
    )
    buy_time = models.DateField(null=True, blank=True, verbose_name="购入年份")
    notes = models.TextField(blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    holding_time = models.DateTimeField(blank=True, null=True, verbose_name="开始占用时间")

    def __str__(self):
        return f"{self.device_model} ({self.asset_code})"

    class Meta:
        db_table = 'devices'
        verbose_name = "设备"
        verbose_name_plural = "设备列表"



class DeviceApply(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('0', '待审批'),
        ('1', '审批通过'),
        ('2', '审批拒绝')
    ]

    id = models.AutoField(primary_key=True, verbose_name="ID")
    apply_user = models.CharField(max_length=50, verbose_name="申请人")
    apply_device = models.CharField(max_length=50, verbose_name="申请设备")
    device_asset_code = models.CharField(max_length=20, verbose_name="设备资产编码")
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    approval_status = models.CharField(
        max_length=10, 
        choices=APPROVAL_STATUS_CHOICES, 
        default='0',
        verbose_name="审批状态"
    )
    approval_time = models.DateTimeField(blank=True, null=True, verbose_name="审批时间")
    approval_user = models.CharField(max_length=50, blank=True, null=True, verbose_name="审批人")
    approval_comment = models.TextField(blank=True, null=True, verbose_name="审批意见")

    def __str__(self):
        return f"{self.apply_user} - {self.device_asset_code}"

    class Meta:
        db_table = 'device_apply'
        verbose_name = "设备申请"
        verbose_name_plural = "设备申请管理"
        ordering = ['-apply_time']


