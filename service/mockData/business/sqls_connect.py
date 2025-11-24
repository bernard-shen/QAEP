# import cx_Oracle
# from pyhive import hive
# import psycopg2
# from psycopg2 import Error,DatabaseError
import pymysql
import time
from pymysql import err as error
from loguru import logger
# from pyhive import presto


class MySql:
    def __init__(self, host, sql_type, port=None, user=None, passwd=None, dbname=None, sample=None, catalog=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.sample = sample
        self.nowTime = time.strftime('%Y-%m-%d', time.localtime())
        self.sql_type = sql_type
        self.catalog = catalog
        # 连接mysql
        if self.sql_type == 'mysql' or self.sql_type == "Mysql" or self.sql_type == "MYSQL":
            self.connect = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, db=self.dbname, charset='utf8', autocommit=True)
            self.cursor = self.connect.cursor()
        # 连接oracle
        # elif self.sql_type == 'oracle':
        #     self.connect = cx_Oracle.connect('{user}/{passwd}@{host}:{port}/{sample}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, sample=self.sample))
        #     self.cursor = self.connect.cursor()
        # 连接hive
        # elif self.sql_type == 'hive':
        #     self.connect = hive.Connection(host=self.host, port=self.port, username=self.user, database=self.dbname)
        #     self.cursor = self.connect.cursor()
        # 连接pg
        # elif self.sql_type == 'pg':
        #     self.connect = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.dbname)
        #     self.cursor = self.connect.cursor()

        # elif self.sql_type == 'presto':
        #     self.engine = create_engine('presto://{}:{}/{}/{}'.format(self.host,self.port,self.catalog,self.sample))
        #     self.cursor = self.engine.connect()

        # 预留其他sql连接
        else:
            pass
        logger.add('../logs/db_connect/file_{}.log'.format(self.nowTime))

    def get_data(self, sql):
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

    def get_data_pg(self, sql):
        try:
            list_data = []
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for i in data:
                list_data.append(i)
            return list_data
        except error as err:
            print("db error: {}".format(err.pgcode))
            return err.pgerror

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
        except error.DatabaseError as err:
            logger.error("执行sql出错...")
            logger.error("sql: {}".format(sql))
            logger.error("db error:{}".format(err.args))

    def commit(self):
        try:
            if self.sql_type == "oracle":
                self.cursor.execute("COMMIT")
        except error.DatabaseError as err:
            logger.error("db error:{}".format(err.args))

    def close(self):
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    new_conn = MySql(sql_type="oracle", host='192.168.9.193', port=2003, user='testor', passwd='123456', sample='XE')
    res = new_conn.execute_sql('login -ushenpengfei -p!Qaz2wsx;')
    time.sleep(1)
    res1 = new_conn.execute_sql('CREATE TABLE TESTOR.CUS_062302 ( id NUMBER(11) NOT NULL, name VARCHAR2(50) NOT NULL, password VARCHAR2(50) NOT NULL)')
    print(res1)
