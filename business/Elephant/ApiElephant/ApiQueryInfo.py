# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/22 1:58 下午
@Author  : Demon
@File    : ApiQueryInfo.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse
import os



class ApiQueryInfo(object):

    def __init__(self, token):
        # 请求头文件
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_adhoc/adhoc'

    def api_adhoc_adhoc_sql_history(self, page_size=20, filters=None, current_page=1, status=None, orders: list=[]):
        """该用户当前历史查询并保存sql脚本
        :filters 模糊搜索条件
        :status 历史搜索的结果，成功还是失败 {'0': 等待中， '1', '2' }
        :orders 数据排序规则 ，[{"column": "startTime", "orderBy": "desc"}]
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/sqlHistory')
        body = {
            "filter": filters,
            "tagFilter": {
                "status": status
            },
            "pageSize": page_size,
            "currentPage": current_page,
            "orders": orders if orders else [{"column": "startTime", "orderBy": "desc"}]
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_query_list(self, sql, user_name='demon_jiao', ):
        """生成数据查询的sql—log,单语句查询"""
        url = parse.urljoin(self.host, f'{self.root}/queryList')
        body = {
            "user": user_name,
            "queryList": [sql],
            "type": "Hive",
            "limit": "5001"
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_query(self, sql, user_name='demon_jiao', ):
        """暂不知道用处"""
        url = parse.urljoin(self.host, f'{self.root}/query')
        body = {
            "user": user_name,
            "queryList": [sql],
            "type": "Hive",
            "limit": "5001"
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_check_status(self, task_id: str):
        """日志状态轮询"""
        url = parse.urljoin(self.host, f'{self.root}/checkStatus')
        body = {"id": [task_id]}

        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_sql_result(self, task_id: str):
        """获取sql查询结果"""
        url = parse.urljoin(self.host, f'{self.root}/sqlResult')
        body = {"id": [task_id]}

        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_sql_log(self, sql, user_name='demon_jiao', ):
        """sql运行日志"""
        url = parse.urljoin(self.host, f'{self.root}/sqlLog')
        body = {

        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)
