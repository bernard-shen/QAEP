import pymysql
import threading
from dbutils.pooled_db import PooledDB
from .singleton import singleton
from .get_config import get_configs

'''
storage = {
    1111:{stack:[(conn,cursor)]}
},

dictionary 为配置文件，存放以下数据：
dictionary = {sql_type:'',host:"",port:"",...}pip 
'''
sql_info = get_configs("web_env", 'database')


@singleton
class SqlHelper(object):

    # 因目前本地就一个固定mysql环境，sql连接引擎暂只指定pymysql
    def __init__(self, dictionary=sql_info):
        self.local = threading.local()
        self.dict = dictionary
        self.pool = PooledDB(pymysql,
            maxconnections=12,
            mincached=1,
            blocking=True,
            host=self.dict['host'],
            port=self.dict['port'],
            user=self.dict['user'],
            password=self.dict['password'],
            database=self.dict['database'],
            charset='utf8',
            autocommit=True
        )

    def open(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur

    def close(self, cur, conn):
        cur.close()
        conn.close()

    def fetchone(self, sql, *args):
        conn, cur = self.open()
        cur.execute(sql, args)
        result = cur.fetchone()
        self.close(conn, cur)
        return result

    def fetchall(self, sql, *args):
        conn, cur = self.open()
        cur.execute(sql, args)
        result = cur.fetchall()
        self.close(conn, cur)
        return result

    def __enter__(self):
        conn, cursor = self.open()
        rv = getattr(self.local, 'stack', None)
        if not rv:
            self.local.stack = [(conn, cursor)]
        else:
            rv.append((conn, cursor))
            self.local.stack = rv
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = getattr(self.local, 'stack', None)
        if not rv:
            # del self.local.stack
            return  # 什么都不干
        conn, cursor = self.local.stack.pop()
        cursor.close()
        conn.close()

# 在结尾实例化一次，导入实例化对象，也能实现单例模式；


if __name__ == '__main__':
    # 此处实例化，其他模块导入时成为单例；
    pd1 = SqlHelper(dictionary={})
    print(pd1)
    pd2 = SqlHelper(dictionary={})
    print(pd2)

    res = pd1.fetchone('select * from sys_users;')
    print(res)

    # 支持上下文嵌套调用; with时，只能单独使用cur.execute, 和 cur.fetch, cur.fetch不传入参;
    with pd2 as cur:
        cur.execute('select * from sys_users;')
        res = cur.fetchone()
        print(res)
