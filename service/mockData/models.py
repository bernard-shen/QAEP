from django.db import models
from django.utils import timezone

class ConnectionInfo(models.Model):
    SQL_TYPE_CHOICES = [
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL'),
        ('oracle', 'Oracle'),
        ('sqlserver', 'SQL Server'),
    ]
    
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('abnormal', '异常'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="ID")
    connect_id = models.CharField(max_length=145, blank=True, null=True, verbose_name="连接ID")
    connect_name = models.CharField(max_length=145, blank=True, null=True, verbose_name="连接名称")
    sql_type = models.CharField(
        max_length=145, 
        choices=SQL_TYPE_CHOICES,
        blank=True, 
        null=True, 
        verbose_name="数据库类型"
    )
    host = models.CharField(max_length=145, blank=True, null=True, verbose_name="主机地址")
    port = models.CharField(max_length=145, blank=True, null=True, verbose_name="端口")
    db = models.CharField(max_length=145, blank=True, null=True, verbose_name="数据库名")
    username = models.CharField(max_length=145, blank=True, null=True, verbose_name="用户名")
    password = models.CharField(max_length=145, blank=True, null=True, verbose_name="密码")
    uri = models.CharField(max_length=145, blank=True, null=True, verbose_name="连接URI")
    connect_status = models.CharField(
        max_length=145, 
        choices=STATUS_CHOICES,
        blank=True, 
        null=True, 
        verbose_name="连接状态"
    )
    create_user = models.CharField(max_length=145, blank=True, null=True, verbose_name="创建人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return f"{self.connect_name} ({self.connect_id})"

    class Meta:
        db_table = 'dt_connection_info'
        verbose_name = "数据库连接信息"
        verbose_name_plural = "数据库连接信息管理"
        ordering = ['-update_time']

class MockHistory(models.Model):
    MOCK_TYPE_CHOICES = [
        ('sql', 'SQL'),
        ('api', 'API'),
        ('file', 'File')
    ]

    SQL_TYPE_CHOICES = [
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL'),
        ('oracle', 'Oracle'),
        ('sqlserver', 'SQL Server'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="ID")
    mock_type = models.CharField(
        max_length=50, 
        choices=MOCK_TYPE_CHOICES,
        verbose_name="造数类型"
    )
    sql_type = models.CharField(
        max_length=50, 
        choices=SQL_TYPE_CHOICES,
        verbose_name="数据库类型"
    )
    is_increment_schema = models.BooleanField(
        default=False,
        verbose_name="是否新建数据库"
    )
    is_increment_table = models.BooleanField(
        default=False,
        verbose_name="是否新建表"
    )
    schema_name = models.CharField(
        max_length=145, 
        verbose_name="数据库名"
    )
    table_name = models.CharField(
        max_length=145, 
        verbose_name="表名"
    )
    is_increment_data = models.BooleanField(
        default=True,
        verbose_name="是否插入数据"
    )
    increment_lines = models.IntegerField(
        verbose_name="插入行数"
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    def __str__(self):
        return f"{self.schema_name}.{self.table_name} ({self.create_time})"

    class Meta:
        db_table = 'dt_mock_history'
        verbose_name = "造数历史记录"
        verbose_name_plural = "造数历史记录管理"
        ordering = ['-create_time']
