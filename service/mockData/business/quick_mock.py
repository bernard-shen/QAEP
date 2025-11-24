#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

from .get_db_connect import new_connect
from .sql_helper import SqlHelper
from .catch_error import CatchError
from .mock_data import MockMysqlData, MockOracleData, MockMyhiveData
from loguru import logger
import datetime
import time
import threading

"""
此方法使用数据库连接池 上下文 + 多线程， 经验证，造数效率明显高于quick_mock02
"""

def insert_data(sql_connect, data_lines, table_name):
    new_mock = MockMysqlData()
    column_list_new = ['uid', 'name', 'phone_number', 'id_no', 'address', 'bank_card', 'company_name', 'job',
                       'email', 'post_code', 'car_no', 'social_credit_code', 'car_code', 'passport', 'tax_code',
                       'organization', 'enterprise_code', 'individual_business', 'officer_card']
    for i in range(int(data_lines)):
        sql_command = new_mock.single_sql(table_name=table_name, column_list=column_list_new)
        sql_connect.execute_sql(sql_command)


def insert_data_by_pool(data_lines, table_name):
    new_mock = MockMysqlData()
    column_list_new = ['uid', 'name', 'phone_number', 'id_no', 'address', 'bank_card', 'company_name', 'job',
                       'email', 'post_code', 'car_no', 'social_credit_code', 'car_code', 'passport', 'tax_code',
                       'organization', 'enterprise_code', 'individual_business', 'officer_card']
    with new_connect as cur:
        for i in range(int(data_lines)):
            sql_command = new_mock.single_sql(table_name=table_name, column_list=column_list_new)
            cur.execute(sql_command)


def get_table_name():
    today = datetime.datetime.today().strftime('%Y%m%d') + '_' + str(time.time())[:10]
    table_name = "table_" + today
    return table_name


def get_column_list():
    list1 = ['uid', 'name', 'phone_number', 'id_no', 'address', 'bank_card', 'company_name', 'job',
                   'email', 'post_code', 'car_no', 'social_credit_code', 'car_code', 'passport', 'tax_code',
                   'organization', 'enterprise_code', 'individual_business', 'officer_card']
    return list1


# 业务内置
def get_secret_list():
    list2 = ["中文地址","银行卡号","电子邮件","企业名称","中文姓名","身份证号","电话号码","邮政编码","车牌号码","社会信用账号","汽车车架号","护照号","税务登记证号","组织机构代码","营业执照代码","单体商户名称","军官警官证编号"]
    return list2

# 此处设置少于100行走单线程，大于100行取连接池 走多线程，返回多线程时的每个线程的行数；
def get_data_group(data_lines):
    if int(data_lines) <= 100:
        return [int(data_lines)]
    else:
        per_group = int(data_lines) // 10
        if int(data_lines) % 10 == 0:
            last = per_group
        else:
            last = int(data_lines) - per_group * 10 + per_group
        return [per_group, last]


def quick_mock(sql_type, connection_info, data_lines=None):
    try:
        if sql_type in ['MYSQL', 'mysql', 'Mysql']:
            new_connect1 = SqlHelper(dictionary=connection_info)
            table_name = get_table_name()
            with new_connect as cur:
                cur.execute("SHOW DATABASES")
                dbs = cur.fetchall()
                db_list = [i[0] for i in dbs]
                if 'autotest001' not in db_list:
                    cur.execute("create database autotest001")
                    cur.execute("use autotest001")

                create_table_tmp = f"""
                    CREATE TABLE `{table_name}` (
                      `uid` bigint(20) DEFAULT NULL COMMENT 'uid',
                      `name` varchar(100) DEFAULT NULL COMMENT '名字',
                      `phone_number` varchar(100) DEFAULT NULL COMMENT '手机号',
                      `id_no` varchar(100) DEFAULT NULL COMMENT '身份证号码',
                      `address` varchar(100) DEFAULT NULL COMMENT '地址',
                      `bank_card` varchar(100) DEFAULT NULL COMMENT '银行卡',
                      `company_name` varchar(100) DEFAULT NULL COMMENT '企业名称',
                      `job` varchar(100) DEFAULT NULL COMMENT '职位',
                      `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
                      `post_code` varchar(20) DEFAULT NULL COMMENT '邮政编码',
                      `car_no` varchar(100) DEFAULT NULL COMMENT '车牌号',
                      `social_credit_code` varchar(100) DEFAULT NULL COMMENT '社会信用账号',
                      `car_code` varchar(100) DEFAULT NULL COMMENT '汽车车架号',
                      `passport` varchar(100) DEFAULT NULL COMMENT '护照',
                      `tax_code` varchar(100) DEFAULT NULL COMMENT '税务登记证号',
                      `organization` varchar(100) DEFAULT NULL COMMENT '组织机构代码',
                      `enterprise_code` varchar(100) DEFAULT NULL COMMENT '营业执照',
                      `individual_business` varchar(100) DEFAULT NULL COMMENT '单体商户名称',
                      `officer_card` varchar(100) DEFAULT NULL COMMENT '军官警官证编号'
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
                cur.execute(create_table_tmp)
                time.sleep(2)

            if int(data_lines) <= 100:
                time1 = time.time()
                insert_data_by_pool(data_lines=int(data_lines), table_name=table_name)
                print("用时：{}".format(time.time()-time1))
            else:
                data_group = get_data_group(int(data_lines))
                time1 = time.time()
                for i in range(10):
                    if i != 9:
                        thread = threading.Thread(target=insert_data_by_pool(data_lines=data_group[0], table_name=table_name))
                    else:
                        thread = threading.Thread(target=insert_data_by_pool(data_lines=data_group[1], table_name=table_name))
                    thread.start()
                    thread.join()
                print("用时：{}".format(time.time()-time1))

        elif sql_type in ['ORACLE', 'oracle', 'Oracle']:
            table_name = get_table_name()
            with new_connect as cur:
                cur.execute("SHOW DATABASES")
                ...
        else:
            # 其他类的
            sql_object = ""

    except Exception as e:
        logger.error("程序错误，错误原因：{}".format(e.args))
        pass


if __name__ == '__main__':
    print(quick_mock(sql_type='mysql', data_lines=666, connection_info={"host": "127.0.0.1", "port": 3306, "username": "root", "password": "qwert789456", "dbname": "autotest001"}))