from django.contrib import admin
from .models import Role, User, Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['menu_id', 'label', 'is_base_menu', 'sub_menu', 'path', 'name', 'icon']
    list_filter = ['is_deleted']
    search_fields = ['label', 'path']

    # 排除自动生成的时间字段
    exclude = ['create_time', 'update_time']

    # 列表页面每页显示的记录数
    list_per_page = 20

    # 按照角色ID排序
    ordering = ['menu_id']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_id', 'role_name', 'role_permissions', 'tips', 'is_deleted']
    list_filter = ['is_deleted']
    search_fields = ['role_name', 'tips']
    
    # 排除自动生成的时间字段
    exclude = ['create_time', 'update_time']
    
    # 列表页面每页显示的记录数
    list_per_page = 20
    
    # 按照角色ID排序
    ordering = ['role_id']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['uid', 'username', 'password', 'roles', 'phone', 'email', 'is_deleted']
    list_filter = ['roles', 'is_deleted']
    search_fields = ['uid', 'username', 'phone', 'email']
    
    # 排除自动生成的时间字段和密码字段
    exclude = ['create_time', 'update_time']
    
    # 列表页面每页显示的记录数
    list_per_page = 20

    # 按照创建时间降序排序
    ordering = ['-create_time']
