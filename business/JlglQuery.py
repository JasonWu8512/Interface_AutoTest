# -*- coding: utf-8 -*-
# @Time : 2021/8/2 7:53 下午
# @Author : Cassie
# @File : JlglQuery.py.py
from config.env.domains import Domains
from utils.middleware.dbLib import MySQL


class JiglGuery:
    """JLGL业务相关的mysql操作"""

    def __init__(self):
        self.strategy = MySQL(pre_db='user_strategy', db_name='user_strategy')

    def query_user_strategty(self, sql):
        res = self.strategy.query(sql)
        return res

    def delete_user_strategry(self, bid):
        """删除bid对应的分流结果"""
        if not bid:
            raise ('必须指定删除条件')
        query = f'DELETE FROM user_strategy.user_strategy WHERE baby_id="{bid}"'
        self.strategy.execute(query)


if __name__ == '__main__':
    Domains.set_env_path('fat')
    strategy = JiglGuery()
    # res = strategy.query_user_strategty(
    #     'SELECT * FROM user_strategy.user_strategy where baby_id="316315f791e84bab87e59f0b7aac1f14" order by phase asc; ')
    res = strategy.delete_user_strategry("316315f791e84bab87e59f0b7aac1f14")
    print(res)
