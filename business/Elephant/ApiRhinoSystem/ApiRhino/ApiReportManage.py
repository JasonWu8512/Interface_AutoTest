# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/6 1:57 下午
@Author  : Demon
@File    : ApiReport.py
"""

# 数据源表管理

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiReport(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/report'

    def api_report_fetch_all(self, keyword=None):
        """
        获取报告信息
        :param :keyword : 模糊筛选报告id或者name
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAll")
        body = {
            "param": keyword
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_delete(self, ids):
        """
        删除报告
        :param : ids
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/delete")
        body = {"id": ids}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_fetch_list(self, orders, filter=None, currentPage: int = 1, page: int = 20,
                               isBiManager: bool = None):
        """
        查询报表管理中所有的报表
        :param orders : 条件 [{"column": "updateTime", "orderBy": "desc"}]
        :param filter : 过滤条件
        :param currentPage : 当前页码 默认 1
        :param page : 每页显示条数 默认 20
        :param isBiManager : 是否是管理员账户，none 不传该参数，true 是
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchList")
        body = {
            "filter": filter,
            "pageSize": page,
            "currentPage": currentPage,
            "orders": orders,
            # "isBiManager": None
        }
        if isBiManager is not None:
            body.update(dict(isBiManager=isBiManager))

        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_off_line(self, ids):
        """
        下线报告，
        :param ids : 报告ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/offline")
        body = {
            "id": ids,
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)


