#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

"""
连接管理提供-数据连接的-增、删、改、查 -功能
连接管理提供-数据连接的-测试连接 -功能
连接管理提供-数据连接的-一键造数、自定义造数-功能：
（一键造数：在autotest1库下新增默认table和默认全内置隐私类型字段；仅需指定造数量；
自定义造数：可选创建schema、tabel、可指定表字段数量和类型、以及造数数据量）
"""

from .get_db_connect import new_connect
from .catch_error import CatchError
from loguru import logger
import datetime
import time


class MyConnect(object):
    def __init__(self):
        self.conn = new_connect

    # 获取时间
    def get_time(self):
        now = datetime.datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    # 获取列
    def execute_sql(self, sql):
        with self.conn as cur:
            cur.execute(sql)

    @CatchError
    def get_columns(self, table_name):
        if table_name:
            with self.conn as cur:
                cur.execute(F"describe {table_name};")
                column_list = [i[0] for i in cur.fetchall()]
            return column_list

    # 获取连接数量
    @CatchError
    def get_connections_count(self):
        with self.conn as cur:
            cur.execute("select count(*) from autotest1.dt_connection_info where is_delete != '1';")
            res = cur.fetchone()
        return int(res[0])

# ===================
    # 查询连接
    def get_connection_list(self, connect_id='', connect_name='', sql_type='', host='', connect_status= '', page=None, default_num=10):
        column_list = self.get_columns(table_name='autotest1.dt_connection_info')
        search_list = ["connect_id", "connect_name", "sql_type", "host", "connect_status"]
        value_list = [connect_id, connect_name, sql_type, host, connect_status]
        search_dict = dict(zip(search_list,value_list))
        base_sql = "SELECT * FROM autotest1.dt_connection_info where is_delete != '1' "
        for key, value in search_dict.items():
            if value != '' and key != 'connect_name':
                base_sql += f"and {key} = '{value}'"
            elif value != '' and key == 'connect_name':
                base_sql += f"and {key} like '%{value}%'"
            else:
                pass
        base_sql += ' order by id desc'

        with self.conn as cur:
            cur.execute(base_sql)
        res = cur.fetchall()

        if len(res) > 0:
            list_temp = [dict(zip(column_list, list(i))) for i in res]
            if page and int(page) > 0:
                return list_temp[((int(page) - 1) * default_num):((int(page)) * default_num)]
            else:
                return list_temp


    # 新增连接
    def addConnection(self, dictionary):
        connect_id = str(time.time()).replace('.', '')
        creat_time = self.get_time()
        sql_tmp = f'''INSERT INTO `autotest1`.`dt_connection_info` 
        (`connect_id`, `connect_name`, `sql_type`, `host`, `port`, `db`, `username`, `password`, `create_time`, `is_delete`) 
        VALUES ('{connect_id}', '{dictionary['connect_name']}', '{dictionary['sql_type']}', '{dictionary['host']}', '{dictionary['port']}', 
        '{dictionary['db']}', '{dictionary['username']}', '{dictionary['password']}', '{creat_time}', '0');'''

        if self.checkConnectName(connect_name=dictionary['connect_name']):
            with self.conn as cur:
                cur.execute(sql_tmp)
                if cur.rowcount >= 0:
                    return "新建连接成功。"
                else:
                    return "新建连接失败！"
        else:
            return "连接名称已存在！"

    # 删除连接
    @CatchError
    def delConnection(self, connect_id):
        id_list = [i['connect_id'] for i in self.get_connection_list()]
        if connect_id not in id_list:
            return '连接不存在...'
        with self.conn as cur:
            cur.execute(f"delete from autotest1.dt_connection_info where connect_id = {connect_id};")
            if cur.rowcount != -1:
                return '角色删除成功...'
            else:
                return '角色删除失败，请联系管理员！'

    # 编辑连接
    @CatchError
    def updateConnection(self, dictionary):
        update_time = self.get_time()
        sql_tmp = f'''UPDATE `autotest1`.`dt_connection_info` SET `connect_name` = '{dictionary['connect_name']}', 
        `host` = '{dictionary['host']}', `port` = '{dictionary['port']}', `db` = '{dictionary['db']}', `username` = '{dictionary['username']}', 
        `password` = '{dictionary['password']}', `update_time` = '{update_time}' WHERE (`connect_id` = '{dictionary['connect_id']}');'''

        with self.conn as cur:
            cur.execute(sql_tmp)
            if cur.rowcount >= 0:
                return "编辑连接成功。"
            else:
                return "编辑连接失败！"

    # 校验连接名是否存在
    @CatchError
    def checkConnectName(self, connect_name):
        if connect_name:
            name_list = self.get_connection_list(connect_name=connect_name)
            if not name_list:
                return True
        else:
            logger.error("请输入角色名！")
            return False



if __name__ == '__main__':
    new_cc = MyConnect()
    # print(new_cc.get_connection_list(connect_name='mysql连接-admin'))
    print(new_cc.delConnection(connect_id='169190029076220'))


