from django.contrib import admin
from .models import ApiInfo

@admin.register(ApiInfo)
class ApiInfoAdmin(admin.ModelAdmin):
    list_display = ['api_name', 'env', 'of_business', 'host', 'api_path', 
                   'req_method', 'body_type', 'is_deleted']
    list_filter = ['env', 'of_business', 'req_method', 'body_type', 'is_deleted']
    search_fields = ['api_name', 'api_path', 'host', 'of_business']
    
    # 排除自动生成的时间字段
    exclude = ['create_time', 'update_time']
    
    # 列表页面每页显示的记录数
    list_per_page = 20
    
    # 按照更新时间降序排序
    ordering = ['-update_time']
