from django.db import models


class ApiInfo(models.Model):
    # 环境选项
    ENV_CHOICES = [
        ('TEST', '测试环境'),
        ('PROD', '生产环境'),
    ]

    # 请求方法选项
    REQ_METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    ]

    # 请求体类型选项
    BODY_TYPE_CHOICES = [
        ('JSON', 'JSON'),
        ('DATA', 'Form Data'),
        ('PARAMS', 'params'),
        ('RAW', 'Raw'),
    ]

    # 字段定义
    id = models.AutoField(primary_key=True, verbose_name="ID")
    env = models.CharField(max_length=10, choices=ENV_CHOICES, verbose_name="环境")
    of_business = models.CharField(max_length=50, verbose_name="所属业务")
    host = models.CharField(max_length=100, verbose_name="域名地址")
    api_name = models.CharField(max_length=100, verbose_name="API名称")
    api_path = models.CharField(max_length=200, verbose_name="API路径")
    req_method = models.CharField(max_length=10, choices=REQ_METHOD_CHOICES, verbose_name="请求方法")
    req_body = models.TextField(blank=True, null=True, verbose_name="请求体")
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, verbose_name="请求体类型")
    req_header = models.TextField(blank=True, null=True, verbose_name="请求头")
    req_params = models.TextField(blank=True, null=True, verbose_name="请求参数")
    resp_demo = models.TextField(blank=True, null=True, verbose_name="响应示例")
    extr_value = models.TextField(blank=True, null=True, verbose_name="提取值")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.env}-{self.of_business}-{self.api_name}- {self.api_path}"

    class Meta:
        db_table = 'api_info'
        verbose_name = "API信息"
        verbose_name_plural = "API信息列表"