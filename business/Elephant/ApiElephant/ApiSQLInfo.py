# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/22 1:45 下午
@Author  : Demon
@File    : ApiSQLInfo.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse
import os



class ApiSQLInfo(object):

    def __init__(self, token):
        # 请求头文件
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_adhoc/sqlInfo'

    def api_adhoc_sql_info_sql_list(self, user_name='demon_jiao', ):
        """该用户当前历史查询并保存sql脚本"""
        url = parse.urljoin(self.host, f'{self.root}/sqlList')
        body = {
            "user": user_name,
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_save_sql(self, sql, name):
        """保存sql为历史脚本
        :param name: 脚本名称
        """
        url = parse.urljoin(self.host, '/api_adhoc/sqlInfo/saveSql')
        body = {
            "user": "demon_jiao",
            "sqlCode": sql,
            "sqlName": name
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_del_sql(self, sql_id):
        """删除保存的sql历史脚本
        :param sql_id: 脚本ID
        """
        url = parse.urljoin(self.host, f'{self.root}/delSql')
        body = {
            "id": sql_id
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_update_sql(self, sql_id, sql_name, sqlcode, user):
        """更新保存的sql历史脚本
        :param sql_id: 脚本ID
        :param sql_name: 脚本ID
        :param sqlcode:  "select *\nfrom jlgl_rpt.rpt_traffic_reading_new_user_add_d as d \nwhere dt ='20201201'"
        :param user: 脚本ID
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/updateSql')
        body = {
            "id": sql_id,
            "sqlName": sql_name,
            "sqlCode": sqlcode,
            "user": user
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)