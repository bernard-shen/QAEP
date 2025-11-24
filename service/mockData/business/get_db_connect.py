#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--
import os
from django.conf import settings
from .get_config import get_configs
from .sql_helper import SqlHelper


# 使用 Django settings 中定义的路径
CONFIG_DIR = os.path.join(settings.BASE_DIR, 'config')
FILE_DIR = os.path.join(CONFIG_DIR, 'env.yaml')

# 确保配置目录存在
os.makedirs(CONFIG_DIR, exist_ok=True)

try:
    now_env = get_configs("web_env", 'database', locator_path=FILE_DIR)
    now_env['creator_type'] = 'pymysql'
    new_connect = SqlHelper(dictionary=now_env)
except FileNotFoundError:
    # 如果配置文件不存在，使用 Django 默认数据库配置
    now_env = settings.DATABASES['default']
    new_connect = SqlHelper(dictionary=now_env)


if __name__ == '__main__':
    with new_connect as cur:
        res = cur.execute('select * from sys_users;')
        print(cur.fetchall())