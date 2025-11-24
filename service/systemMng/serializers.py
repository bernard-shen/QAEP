from rest_framework import serializers
from .models import User, Role, Menu

class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = ['id', 'uid', 'username', 'roles', 'phone', 'email', 
                 'create_time', 'update_time', 'comment']
        # 排除密码字段

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name', 'role_permissions', 'tips']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['menu_id', 'label', 'is_base_menu', 'sub_menu', 'path', 
                 'name', 'icon', 'url'] 