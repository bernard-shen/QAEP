#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

from .factory_method import MysqlFactory, OracleFactory
from loguru import logger
from .sql_helper import SqlHelper
from .get_config import get_configs


def test_connect(sql_type, connection_info):
    try:
        if sql_type in ['MYSQL', 'mysql', 'Mysql']:
            sql_object = MysqlFactory(host=connection_info["host"], port=int(connection_info["port"]),
                                        user=connection_info["username"], passwd=connection_info["password"], dbname=connection_info["db"])

        elif sql_type in ['ORACLE', 'oracle', 'Oracle']:
            sql_object = OracleFactory(host=connection_info["host"], port=int(connection_info["port"]),
                                        user=connection_info["username"], passwd=connection_info["password"], sample=connection_info["db"])
        else:
            # 其他类的， 没配置环境和插件，所以也没建对应的工厂子类类
            # sql_object = ""
            sql_object = MysqlFactory(host=connection_info["host"], port=int(connection_info["port"]),
                                        user=connection_info["username"], passwd=connection_info["password"], dbname=connection_info["db"])

        sql_connect = sql_object.create_connection()
        # 不能用execute_sql判断，因为这个方法我没设置返回值，成功失败都是None
        if sql_connect.get_data("select 1"):
            connect_flag = '1'
        else:
            connect_flag = '0'
        return connect_flag
    except Exception as e:
        logger.error('测试连接失败！失败原因：{}'.format(e.args))
        connect_flag = '0'
        return connect_flag


def get_db_list(sql_type, connection_info):
    try:
        if sql_type in ['MYSQL', 'mysql', 'Mysql']:
            sql_object = MysqlFactory(host=connection_info["host"], port=int(connection_info["port"]),
                                        user=connection_info["username"], passwd=connection_info["password"], dbname=connection_info["db"])

        elif sql_type in ['ORACLE', 'oracle', 'Oracle']:
            sql_object = OracleFactory(host=connection_info["host"], port=int(connection_info["port"]),
                                        user=connection_info["username"], passwd=connection_info["password"], sample=connection_info["db"])
        else:
            # 其他类的
            sql_object = ""

        sql_connect = sql_object.create_connection()
        # 不能用execute_sql判断，因为这个方法我没设置返回值，成功失败都是None
        db_list = sql_connect.get_data("show databases;")
        sys_db = ['information_schema','mysql','performance_schema','sys']
        list_temp = []
        list_new = [i[0] for i in db_list if i[0] not in sys_db]
        for item in list_new:
            list_temp.append({"name":item, "value":item})
        return list_temp
    except Exception as e:
        logger.error('获取dblist失败！失败原因：{}'.format(e.args))
        return []

def get_table_list(sql_type, connection_info, choice_db):
    try:
        if sql_type in ['MYSQL', 'mysql', 'Mysql']:
            sql_object = MysqlFactory(host=connection_info["host"], port=int(connection_info["port"]),
                                        user=connection_info["username"], passwd=connection_info["password"], dbname=connection_info["db"])

        elif sql_type in ['ORACLE', 'oracle', 'Oracle']:
            sql_object = OracleFactory(host=connection_info["host"], port=int(connection_info["port"]),
                                        user=connection_info["username"], passwd=connection_info["password"], sample=connection_info["db"])
        else:
            # 其他类的
            sql_object = ""

        sql_connect = sql_object.create_connection()
        # 不能用execute_sql判断，因为这个方法我没设置返回值，成功失败都是None
        sql_connect.execute_sql(f"use {choice_db};")
        table_list = sql_connect.get_data("show tables;")
        list_temp = []
        list_new = [i[0] for i in table_list]
        for item in list_new:
            list_temp.append({"name":item, "value":item})
        return list_temp
    except Exception as e:
        logger.error('获取dblist失败！失败原因：{}'.format(e.args))
        return []


if __name__ == '__main__':
    print(test_connect(sql_type='mysql', connection_info={"host": "127.0.0.1", "port": 3306, "username": "root", "password": "qwert789456", "dbname": "autotest1"}))


