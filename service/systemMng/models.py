from django.db import models
import time

# Create your models here.

class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True, verbose_name="菜单ID")
    label = models.CharField(max_length=50, verbose_name="菜单名称")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_base_menu = models.BooleanField(default=False, verbose_name="是否为基础菜单")
    sub_menu = models.CharField(max_length=200, blank=True, null=True, verbose_name="子菜单")
    path = models.CharField(max_length=100, verbose_name="路由路径")
    name = models.CharField(max_length=50, verbose_name="路由名称")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="图标")
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name="外部链接")

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'menu'
        verbose_name = "菜单"
        verbose_name_plural = "菜单管理"
        ordering = ['menu_id']

class Role(models.Model):
    role_id = models.AutoField(primary_key=True, verbose_name="角色ID")
    role_name = models.CharField(max_length=50, unique=True, verbose_name="角色名称")
    role_permissions = models.TextField(blank=True, null=True, verbose_name="角色权限")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    tips = models.CharField(max_length=200, blank=True, null=True, verbose_name="备注说明")

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'role'
        verbose_name = "角色"
        verbose_name_plural = "角色管理"
        ordering = ['role_id']

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    uid = models.CharField(max_length=50, unique=True, verbose_name="用户标识")
    username = models.CharField(max_length=50, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    roles = models.CharField(max_length=200, blank=True, null=True, verbose_name="角色")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="手机号")
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")
    comment = models.TextField(blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    def save(self, *args, **kwargs):
        if not self.uid:
            # 生成 uid (格式：U + 时间戳后6位)
            timestamp = str(int(time.time()))[-6:]
            self.uid = f"U{timestamp}"
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.uid})"

    class Meta:
        db_table = 'user'
        verbose_name = "用户"
        verbose_name_plural = "用户管理"
        ordering = ['-create_time']
