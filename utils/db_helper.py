# -*- coding: utf-8 -*-
"""
@Time    : 2020/11/14 1:04 下午
@Author  : Demon
@File    : db_helper.py
"""
import os
import threading
from business.Elephant.commons.common import DEV
import pymysql



class DB_CLIENT(object):
    LOCAL = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "Test1234",
        "database": "db_name",

    }

    DB_CLICK_HOUSE_FAT = {
        "host": "10.18.2.19",
        "port": 8123,
        "user": "root",
        "password": "Test1234",
        "database": "db_name",

    }

    DB_XELEPHANT_DEV = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "Test1234",
        "database": "db_name",

    }

    DB_XELEPHANT_PRE = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "Test1234",
        "database": "db_name",

    }

    DB_XELEPHANT_PRO = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "Test1234",
        "database": "db_name",

    }

    GROUND_HOG = {
        "host": "jiliguala-bigdata41",
        "port": 3306,
        "user": "datacenter",
        "password": "JiligualaDataCenter",
        "database": "rhino_system",
    }

    _instance_lock = threading.Lock()
    def __init__(self, addrs: str=DEV.DEV.value):
        """
        @addrs :环境配置，默认dev
        """
        self.st = f"DB_XELEPHANT_{addrs.upper()}"
        if hasattr(DB_CLIENT, addrs.upper()):
            self.dbconfig = getattr(DB_CLIENT, addrs.upper())
        elif hasattr(DB_CLIENT, self.st):
            self.dbconfig = getattr(DB_CLIENT, self.st)
        else:
            self.dbconfig = DB_CLIENT.DB_XELEPHANT_DEV

    def get_connection(self):
        try:
            self.conn = pymysql.connect(
                host=self.dbconfig['host'],
                port=self.dbconfig['port'],
                user=self.dbconfig['user'],
                password=self.dbconfig['password'],
                database=self.dbconfig['database'],
                charset='utf8'
            )
            print(f"{self.st.upper()} Database connected success")
            return self.conn
        except pymysql.Error as e:
            print(f"{self.st.upper()} Database connected failed")
            return False

#
# class SQL:
#     # @classmethod
#     # def safe(cls, s):
#     #     return MySQLdb.escape_string(s)
#
#     @classmethod
#     def dict_2_str_and(cls, dictin):
#         '''
#         将字典变成，key='value' and key='value'的形式
#         '''
#         tmplist = []
#         for k, v in dictin.items():
#             if not isinstance(v, str):
#                 # v: ["between", ["", ""]]
#                 if v[0].upper() == "BETWEEN":
#                     tmp = "%s BETWEEN '%s' AND '%s'" % (str(k), str(v[1][0]), str(v[1][-1]))
#                 else:
#                     tmp = "%s IN %s" % (str(k), str(v))
#             else:
#                 tmp = "%s='%s'" % (str(k), str(v))
#             tmplist.append(' ' + tmp + ' ')
#
#         return ' AND '.join(tmplist)
#
#     @classmethod
#     def __get_join_func(self, dicts):
#         return " " + dicts.get("_rel_").upper() + " " if dicts.get("_rel_") else " AND "
#
#     @classmethod
#     def __create_con(self, col, data):
#         """
#         :param col:列名
#         :param data:条件 {'in': [1, 3], '_rel_': 'or'}
#         """
#         if not isinstance(data, dict):
#             return False
#         _rel_ = self.__get_join_func(data)
#         temp = []
#         for k, v in data.items():
#             if k == '_rel_': continue
#             if k.upper() == "BETWEEN":
#                 tmp = f"{col} {k.upper()} \"{v[0]}\" AND \"{v[-1]}\""
#             elif k.upper() == "IN":
#                 con = ["\"" + str(_) + "\"" for _ in v]
#                 tmp = f"{col} {k.upper()} ({','.join(con)})"
#             elif k.upper() == "LIKE":
#                 tmp = f"{col} {k.upper()} \"%{v}%\""
#             else:
#                 tmp = f"{col} {k.upper()} \"{v}\""
#             temp.append(tmp)
#         return _rel_.join(temp)
#
#     @classmethod
#     def __dict_2(self, dictin):
#         '''
#         将字典变成，key='value' and key='value'的形式
#         :param dictin:字典
#         '''
#         if not isinstance(dictin, dict): return False
#         ans = []
#
#         _rel_ = self.__get_join_func(dictin)
#         for key, value in dictin.items():
#             if key != '_rel_':
#                 ans.append(self.__create_con(key, value))
#         if len(ans) == 1:
#             return ans[0]
#         else:
#             return _rel_.join(map(lambda x: "(" + x + ")", ans))
#
#     @classmethod
#     def get_s_sql(cls, table, conditions=None, isdistinct=False, keys=None):
#         '''
#         生成select的sql语句
#         :param table:查询记录的表名
#         :param key:需要查询的字段
#         :param conditions:插入的数据，字典  # v: ["between", ["", ""]] ;  # v: ["in", ["", "", ""]]
#         :param isdistinct:查询的数据是否不重复
#         '''
#         keys = keys if keys else "*"
#         if isdistinct:
#             sql = 'SELECT DISTINCT %s ' % ",".join(keys)
#         else:
#             sql = 'SELECT  %s ' % ",".join(keys)
#         sql += ' FROM %s ' % table
#         if conditions:
#             # mock_data.py += ' WHERE %s ' % SQL.__dict_2(self=SQL, dictin=conditions)
#             sql += ' WHERE %s ' % cls.__dict_2(dictin=conditions)
#         return sql


class DB(object):
    def __init__(self, config='dev'):
        self.conn = DB_CLIENT(addrs=config).get_connection()

    def search(self, sql):
        try:
            print(sql)
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                columns = [_[0].lower() for _ in cursor.description]
                results = [dict(zip(columns, _)) for _ in cursor]
                return results

        except Exception as e:
            print(e)
        # finally:
        #     cls.CONNECT.close()

    def get(self, sql):
        results = self.search(sql)
        return results[0] if len(results) else None

    def insert(self, sql):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                self.conn.commit()

            except Exception as e:
                self.conn.rollback()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn:
                self.conn.close()
        except:
            pass




