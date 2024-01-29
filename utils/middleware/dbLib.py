# coding=utf-8
# @Time    : 2020/8/3 4:20 下午
# @Author  : keith
# @File    : dbLib

import os
import time
from functools import wraps
from peewee import OperationalError, __exception_wrapper__
from utils.middleware.DBConfigs import CONFIG_MAP
from playhouse.pool import PooledMySQLDatabase
from uuid import uuid4
import pandas as pd
from dbutils.pooled_db import PooledDB
from config.env.domains import Domains


def time_elapse(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"开始执行: {func.__name__}")
        ret = func(*args, **kwargs)
        print(f"完成执行: {func.__name__}, 耗时: {(time.time() - start):.2f}秒")
        return ret

    return wrapper


class RetryOperationError:
    def execute_sql(self, sql, params=None, commit=True):
        try:
            cursor = super(RetryOperationError, self).execute_sql(sql, params, commit)
        except OperationalError:
            if not self.is_closed():
                self.close()
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        return cursor


class AutoConnectPooledDatabase(RetryOperationError, PooledMySQLDatabase):
    pass


connection_pools = {k: None for k, v in CONFIG_MAP.items()}


def get_db_key(pre_db):
    env = os.environ.get('env')
    if env:
        config = Domains.set_env_path(env)
    else:
        config = Domains.set_env_path('fat')
    return f'{pre_db}_{config["env"]}'


def get_connect_config(pre_db, db_name=None):
    """生成不同环境的db链接配置"""
    db_key = get_db_key(pre_db)
    if connection_pools[db_key] is None:
        connection_pools[db_key] = dict(CONFIG_MAP.get(db_key), database=db_name)
    return connection_pools[db_key]


def get_database(refresh=None, pre_db=None, db_name=None):
    connection_pool = get_connect_config(pre_db=pre_db, db_name=db_name)
    # connection_pool = connection_pools[db_config]
    # print('connection_pool', connection_pool, isinstance(connection_pool, AutoConnectPooledDatabase))
    # print(connection_pools)
    conn = connection_pools[get_db_key(pre_db)]
    if (refresh or isinstance(conn, dict)):
        connection_pool = AutoConnectPooledDatabase(**connection_pools[get_db_key(pre_db)])
        # print('connection_pool', connection_pool())
        connection_pools[get_db_key(pre_db)] = connection_pool
        print('*' * 10, connection_pools)
    if isinstance(conn, AutoConnectPooledDatabase) and conn.is_closed:
        connection_pool = connection_pools[get_db_key(pre_db)]
        print(isinstance(conn, AutoConnectPooledDatabase), conn.is_closed())
    try:
        cursor = connection_pool.execute_sql("SELECT 1")
        cursor.fetchall()
    except Exception as e:
        print(e)
        if refresh:
            return None
        connection_pool = get_database(True, pre_db=pre_db, db_name=db_name)
    return connection_pool


class MySQL:
    def __init__(self, pre_db, db_name, db_config="default"):
        self.db = get_database(pre_db=pre_db, db_name=db_name)
        # self.db = get_connect_config(pre_db=pre_db, db_name=db_name)
        # self.db = get_database(db_config=db_config)

    @time_elapse
    def query(self, sql, args=None):
        cursor = self.db.execute_sql(sql, args)
        columns = [head[0] for head in cursor.description]
        data = cursor.fetchall()
        return [dict(zip(columns, row)) for row in data]

    def query_data_frame(self, sql, args=None):
        """DataFrame: null --> NA"""
        cursor = self.db.execute_sql(sql, args)
        return pd.DataFrame(list(cursor.fetchall()), columns=[head[0] for head in cursor.description])

    def query_raw(self, sql, args=None):
        cursor = self.db.execute_sql(sql, args)
        return cursor.fetchall()

    @time_elapse
    def execute(self, sql, args=None):
        self.db.execute_sql(sql, args)

    def execute_many(self, sql, args=None):
        uid = str(uuid4())
        print(f"正在执行sql批处理, uuid: {uid}")
        with self.db.atomic():
            for arg in args:
                self.db.execute_sql(sql, arg)
        print(f"批处理完成, uuid: {uid}")


def check_file_is_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('file_path'):
            if not os.path.exists(kwargs.get('file_path')):
                raise Exception('文件不存在')
        ret = func(*args, **kwargs)
        return ret

    return wrapper


class DBLib(object):
    pass

# if __name__ == '__main__':
# sql = MySQL(db_config='default')
# print(sql.query('SHOW TABLES;'))
# print(MySQL(db_config='crm_prod_readonly').query('select * from Answer limit 2'))
# print(MySQL(db_config='crm_prod_readonly').query_data_frame('select * from Answer limit 2'))
# print(sql.query('select * from rpt_traffic_reading_new_user_add_d limit 1'))
# pass
# Domains.set_env_path('fat')
# mysql = MySQL(pre_db='eduplatform1', db_name='eduplatform1')
# print(mysql.query('SHOW TABLES;'))
#
# mysql1 = MySQL(pre_db='eduplatform2', db_name='eduplatform2')
# print(id(mysql), id(mysql1))
# print(mysql1.query('SHOW TABLES;'))
# # print(get_connect_config(pre_db='default',))
# mysql2 = MySQL(pre_db='eduplatform3', db_name='eduplatform3')
# print(id(mysql), id(mysql1))
# print(mysql2.query('select * from knowledge_record1 limit 2'))

# 海外数据库连接调试
# Domains.set_env_path('prod')
# mysql = MySQL(pre_db='jlgg', db_name='user')
# print(mysql.query('SELECT * FROM inter_user LIMIT 2;'))
