#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

from .get_db_connect import new_connect
from .mock_data import MockMysqlData, MockOracleData, MockMyhiveData
from loguru import logger
import datetime
import time
import threading
from .sql_helper import SqlHelper
from .get_config import get_configs
from ..models import MockHistory

"""
自定义造数：使用前端传入的参数，来确定：
1、是否新建库、表：库表在已有列表中，不再则新建；
2、字段映射：使用用户勾选字段来创建表；
"""


class MyManualMock(object):
    def __init__(self, connection_info):
        self.sql_type = connection_info["sql_type"]
        self.connection_info = connection_info

    def get_time(self):
        return str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    def get_table_name(self):
        today = datetime.datetime.today().strftime('%Y%m%d') + '_' + str(time.time())[:10]
        table_name = "table_" + today
        return table_name

    def get_column_list(self):
        list1 = ['uid', 'name', 'phone_number', 'id_no', 'address', 'bank_card', 'company_name', 'job',
                 'email', 'post_code', 'car_no', 'social_credit_code', 'car_code', 'passport', 'tax_code',
                 'organization', 'enterprise_code', 'individual_business', 'officer_card']
        return list1

    def insert_data_by_pool(self, data_lines):
        if self.sql_type in ['MYSQL', 'mysql', 'Mysql']:
            new_mock = MockMysqlData()
        elif self.sql_type in ['ORACLE', 'oracle', 'Oracle']:
            new_mock = MockOracleData()
        elif self.sql_type in ['HIVE', 'hive', 'Hive']:
            new_mock = MockMyhiveData()
        else:
            # 内网代码丢失，此处预留空位，本地环境有限，暂不赘述和扩展；
            new_mock = MockMysqlData()
            pass
        with new_connect as cur:
             for i in range(int(data_lines)):
                sql_command = new_mock.single_sql(dbname=self.connection_info["dbname"],
                                                  table_name=self.connection_info["table_name"],
                                                  column_list=self.connection_info["column_list"])
                cur.execute(sql_command)

    # 此处设置少于100行走单线程; 大于100行取连接池 走多线程; 返回多线程时的首尾两个线程的行数；
    def get_data_group(self, data_lines):
        if int(data_lines) <= 100:
            return [int(data_lines)]
        else:
            per_group = int(data_lines) // 10
            if int(data_lines) % 10 == 0:
                last = per_group
            else:
                last = int(data_lines) - per_group * 10 + per_group
            return [per_group, last]

    def get_create_tables_sql(self, column_list):
        start = f"""CREATE TABLE `{self.connection_info["dbname"]}`.`{self.connection_info["table_name"]}` (\n"""
        end = """\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        if len(column_list) == 0:
            between = ''
        elif len(column_list) == 1:
            between = f"\t`{column_list[0]}` varchar(100) DEFAULT NULL"
        else:
            between = ""
            for i in range(len(column_list)-1):
                between += f"\t`{column_list[i]}` varchar(100) DEFAULT NULL,\n"
            between += f"\t`{column_list[-1]}` varchar(100) DEFAULT NULL"
        return start + between + end

    def manual_mock(self, sql_type, data_lines=None):
        is_increment_schema = 0
        is_increment_table = 0
        try:
            if sql_type in ['MYSQL', 'mysql', 'Mysql']:
                with new_connect as cur:
                    cur.execute("SHOW DATABASES")
                    dbs = cur.fetchall()
                    db_list = [i[0] for i in dbs]
                    if self.connection_info["dbname"] == '':
                        self.connection_info["dbname"] = 'autotest1'
                    if self.connection_info["table_name"] == "":
                        self.connection_info["table_name"] = self.get_table_name()
                    if not self.connection_info["column_list"]:
                        self.connection_info["column_list"] = self.get_column_list()

                    if self.connection_info["dbname"] != '' and self.connection_info["dbname"] not in db_list:
                        is_increment_schema = 1
                        is_increment_table = 1
                        cur.execute(f"create database {self.connection_info['dbname']}")
                        cur.execute(f"use {self.connection_info['dbname']}")
                        table_sql = self.get_create_tables_sql(column_list=self.connection_info["column_list"])
                        cur.execute(table_sql)
                    else:
                        with new_connect as cur:
                            cur.execute(f"use {self.connection_info['dbname']}")
                            cur.execute("show tables;")
                            tbs = cur.fetchall()
                            tb_list = [i[0] for i in tbs]
                            if self.connection_info["table_name"] not in tb_list:
                                table_sql = self.get_create_tables_sql(column_list=self.connection_info["column_list"])
                                cur.execute(table_sql)
                                is_increment_table = 1
                            else:
                                cur.execute(f"describe {self.connection_info['table_name']};")
                                column_list = [i[0] for i in cur.fetchall()]
                                self.connection_info["column_list"] = column_list

                    if int(data_lines) <= 100:
                        time1 = time.time()
                        self.insert_data_by_pool(data_lines=int(data_lines))
                        print("用时：{}".format(time.time()-time1))
                    else:
                        data_group = self.get_data_group(int(data_lines))
                        time1 = time.time()
                        for i in range(10):
                            if i != 9:
                                thread = threading.Thread(target=self.insert_data_by_pool(data_lines=data_group[0]))
                            else:
                                thread = threading.Thread(target=self.insert_data_by_pool(data_lines=data_group[1]))
                            thread.start()
                            thread.join()
                        print("用时：{}".format(time.time()-time1))

                    # 此处同步造数历史记录数据
                    MockHistory.objects.create(
                        mock_type='sql',
                        sql_type=self.connection_info['sql_type'],
                        is_increment_schema=bool(is_increment_schema),
                        is_increment_table=bool(is_increment_table),
                        schema_name=self.connection_info['dbname'],
                        table_name=self.connection_info['table_name'],
                        is_increment_data=True,
                        increment_lines=int(self.connection_info['dataLines'])
                    )

            elif sql_type in ['ORACLE', 'oracle', 'Oracle']:
                with new_connect as cur:
                    cur.execute("SHOW DATABASES")
                    # ...
            else:
                pass
                # 其他类的
                sql_object = ""
            return "造数成功"
        except Exception as e:
            logger.error("程序错误，错误原因：{}".format(e.args))
            return "造数错误，错误原因：{}".format(e.args)


if __name__ == '__main__':
    new_mock = MyManualMock(connection_info={"sql_type": "mysql", "table_name":"shen004", "column_list":['uid','name','phone'], "host": "127.0.0.1", "port": 3306, "username": "root", "password": "qwert789456", "dbname": "autotest010"})
    new_mock.manual_mock(sql_type='mysql', data_lines=1000)


