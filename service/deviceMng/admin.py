from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_model', 'asset_code', 'device_type', 'os_name', 'owner', 'status', 'current_user']
    list_filter = ['device_type', 'status', 'os_name']
    search_fields = ['device_model', 'asset_code', 'owner', 'current_user']
    
    # 排除自动生成的时间字段
    exclude = ['create_time', 'update_time']
    
    # 列表页面每页显示的记录数
    list_per_page = 20
    
    # 按照更新时间降序排序
    ordering = ['-update_time']
