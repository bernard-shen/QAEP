from django.db import models
import json

# Create your models here.

class TestEnvironment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    business = models.CharField(max_length=50, verbose_name="业务")
    env = models.CharField(max_length=20, verbose_name="环境")
    name = models.CharField(max_length=50, verbose_name="名称")
    domain = models.CharField(max_length=200, verbose_name="域名地址")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.business}-{self.env}-{self.name}"

    class Meta:
        db_table = 't_env'
        verbose_name = "环境"
        verbose_name_plural = "环境管理"
        ordering = ['-create_time']

class TestAccount(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    business = models.CharField(max_length=50, verbose_name="业务")
    env = models.CharField(max_length=20, verbose_name="环境")
    username = models.CharField(max_length=50, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.business}-{self.env}-{self.username}"

    class Meta:
        db_table = 't_account'
        verbose_name = "账户"
        verbose_name_plural = "账户管理"
        ordering = ['-create_time']

class TestCase(models.Model):
    STATUS_CHOICES = (
        ('normal', '正常'),
        ('abnormal', '异常'),
    )

    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="用例名称")
    business = models.CharField(max_length=50, verbose_name="业务")
    env = models.CharField(max_length=20, verbose_name="环境")
    account = models.CharField(max_length=20, null=True, verbose_name="账户")
    api_list = models.JSONField(default=list, verbose_name="接口列表")
    execution_body = models.JSONField(default=dict, verbose_name="执行体")
    extract_body = models.JSONField(default=dict, verbose_name="提取体")
    assert_body = models.JSONField(default=dict, verbose_name="断言体")
    run_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name="运行状态")
    last_result = models.TextField(null=True, blank=True, verbose_name="上次执行结果")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_testcases'
        verbose_name = "测试用例"
        verbose_name_plural = "用例管理"
        ordering = ['-create_time']

class TestScene(models.Model):
    STATUS_CHOICES = (
        ('normal', '正常'),
        ('abnormal', '异常'),
    )

    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="场景名称")
    business = models.CharField(max_length=50, verbose_name="业务")
    env = models.CharField(max_length=20, verbose_name="环境")
    account = models.CharField(max_length=20, null=True, verbose_name="账户")
    case_list = models.JSONField(default=list, verbose_name="用例列表")
    run_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name="运行状态")
    last_result = models.TextField(null=True, blank=True, verbose_name="上次执行结果")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_scenes'
        verbose_name = "测试场景"
        verbose_name_plural = "场景管理"
        ordering = ['-create_time']
