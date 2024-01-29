# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/30 7:13 下午
@Author  : Demon
@File    : CrmQuery.py
"""


from utils.middleware.dbLib import MySQL
from config.env.domains import Domains
from utils.middleware.mongoLib import MongoClient
from utils.decorators import switch_db


def generate_table_configs(table, **kwargs):
    # 生成简单sql
    # self.mysql.query('SELECT * FROM students WHERE gua_id IN ()')
    base = 'SELECT * FROM %s %s LIMIT 1000'
    rules = list()
    for arg, kw in kwargs.items():
        if isinstance(kw, str):
            rul = ' %s = "%s"' % (arg, kw)
        elif isinstance(kw, int):
            rul = ' %s = %d' % (arg, kw)
        elif iter(kw):
            rul = ' %s IN (%s) ' % (arg, ','.join(['"%s"' % item for item in kw]))
        rules.append(rul)
    is_where = ' WHERE %s' % ' AND '.join(rules) if rules else ''
    return base % (table, is_where)


class CrmJainaQuery(object):
    def __init__(self, ):
        # 规划师库操作
           self.mysql = MySQL(pre_db='crm_jaina', db_name='jaina')

    def query_jaina_info(self, table, **kwargs):
        # 根据条件查询学生信息 限制返回1000条数据
        sql_conditions = generate_table_configs(table=table, **kwargs)
        print(sql_conditions)
        return self.mysql.query(sql_conditions)


class CrmAllianceQuery(object):
    def __init__(self):
        # 规划师-公共库操作
        self.mysql = MySQL(pre_db='crm_alliance', db_name='alliance')

    def query_alliance_info(self, table, **kwargs):
        # 根据筛选条件查询表格中的数据
        sql_conditions = generate_table_configs(table=table, **kwargs)
        return self.mysql.query(sql_conditions)


class CrmThrallQuery(object):
    def __init__(self):
        # 班主任库操作
        self.mysql = MySQL(pre_db='crm_thrall', db_name='thrall')

    def query_table_info(self, table='class_students', **kwargs):
        # 根据筛选条件查询表格中的数据,默认查询英语学员信息表
        sql_conditions = generate_table_configs(table, **kwargs)
        return self.mysql.query(sql_conditions)

    def delete_leadsbind(self, uid):
        # 根据uid删除crm分配的班主任（转介绍业务自动化case使用）
        sql = "DELETE FROM crleadsbindv2 WHERE user_id='%s'" % uid
        return self.mysql.execute(sql)

class CrmZaryaQuery(object):
    def __init__(self):
        #推广人操作
        self.mysql =MySQL(pre_db='crm_zarya',db_name='zarya')
    def query_zarya_info(self,table,**kwargs):
        #根据筛选条件查询表格中的数据
        sql_conditions = generate_table_configs(table=table,**kwargs)
        print(sql_conditions)
        return self.mysql.query(sql_conditions)

class CrmLeadsAssignQuery(object):
    def __init__(self):
        # 班主任库操作
        self.mysql = MySQL(pre_db='crm_leads_assign', db_name='crm_leads_assign')

    def query_table_info(self, table='crleadsbindv2', **kwargs):
        # 根据筛选条件查询表格中的数据,默认查询英语学员信息表
        sql_conditions = generate_table_configs(table, **kwargs)
        return self.mysql.query(sql_conditions)

    def delete_leadsbind(self, uid):
        # 根据uid删除crm分配的班主任（转介绍业务自动化case使用）
        sql = "DELETE FROM crleadsbindv2 WHERE user_id='%s'" % uid
        return self.mysql.execute(sql)


if __name__ == '__main__':
    dm = Domains()
    dm.set_env_path('fat')
    cjq = CrmJainaQuery()
    # print(cjq.query_student_info(name=92, ids=[9, 87]))
    caq = CrmAllianceQuery()
    caq.query_alliance_info(table='name', gua_id=0)
