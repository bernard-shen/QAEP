#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--
import pymysql
# import cx_Oracle
# from pyhive import hive
# import psycopg2
# from psycopg2 import Error,DatabaseError
import time
from pymysql import err as error
from loguru import logger


class Connection(object):
    def __init__(self, host, port=None, user=None, passwd=None, dbname=None, sample=None, catalog=None, sql_type=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.sample = sample
        self.sql_type = sql_type
        self.nowTime = time.strftime('%Y-%m-%d', time.localtime())
        self.catalog = catalog
        logger.add('../logs/db_connect/file_{}.log'.format(self.nowTime))

    def get_connect_cursor(self):
        cursor = []
        return cursor

    def get_data(self, sql):
        self.cursor = self.get_connect_cursor()[0]
        try:
            list_data = []
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for i in data:
                list_data.append(i)
            return list_data
        except error.DatabaseError as err:
            logger.error("sql: {}".format(sql))
            logger.error("db error: {}".format(err.args))

    def get_data_first_column(self, sql):
        self.cursor = self.get_connect_cursor()[0]
        try:
            list_data = []
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for i in data:
                list_data.append(i[0])
            return list_data
        except error.DatabaseError as err:
            logger.error("db error: {}".format(err.args))

    def execute_sql(self, sql):
        self.cursor = self.get_connect_cursor()[0]
        try:
            self.cursor.execute(sql)
        except error.DatabaseError as err:
            logger.error("执行sql出错...")
            logger.error("sql: {}".format(sql))
            logger.error("db error:{}".format(err.args))

    def commit(self):
        self.cursor = self.get_connect_cursor()[0]
        try:
            if self.sql_type == "oracle":
                self.cursor.execute("COMMIT")
        except error.DatabaseError as err:
            logger.error("db error:{}".format(err.args))

    def close(self):
        self.cursor = self.get_connect_cursor()[0]
        self.cursor.close()


class Mysql(Connection):
    def get_connect_cursor(self):
        print("这是子类方法")
        try:
            self.connect = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                           db=self.dbname, charset='utf8', autocommit=True)
            self.cursor = self.connect.cursor()
            return [self.cursor]
        except Exception as e:
            logger.error("获取Mysql连接失败, 失败原因：{}...".format(e.args))
            return "获取Mysql连接失败, 失败原因：{}...".format(e.args)


class Oracle(Connection):
    def get_connect_cursor(self):
        print("这是子类方法")
        try:
            # self.connect = cx_Oracle.connect(
            #     '{user}/{passwd}@{host}:{port}/{sample}'.format(user=self.user, passwd=self.passwd, host=self.host,
            #                                                     port=self.port, sample=self.sample))
            # self.cursor = self.connect.cursor()
            return [self.cursor]
        except Exception as e:
            logger.error("获取Mysql连接失败, 失败原因：{}...".format(e.args))
            return None


class ConnectionFactory(object):
    def __init__(self, host, port=None, user=None, passwd=None, dbname=None, sample=None, catalog=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.sample = sample
        self.nowTime = time.strftime('%Y-%m-%d', time.localtime())
        self.catalog = catalog

    def create_connection(self):
        pass


class MysqlFactory(ConnectionFactory):
    def create_connection(self):
        return Mysql(host=self.host, port=self.port, user=self.user, passwd=self.passwd, dbname=self.dbname)


class OracleFactory(ConnectionFactory):
    def create_connection(self):
        return Oracle(host=self.host, port=self.port, user=self.user, passwd=self.passwd, sample=self.sample)


class HiveFactory(ConnectionFactory):
    # Hive 连接工厂实现
    pass


if __name__ == '__main__':
    mysql_Object = MysqlFactory(host='127.0.0.1', port=3306, user='root', passwd='qwert789456', dbname='autotest1')
    mysql_connect = mysql_Object.create_connection()
    data = mysql_connect.get_data(sql="select * from dt_based_sqls;")
    print(data)


