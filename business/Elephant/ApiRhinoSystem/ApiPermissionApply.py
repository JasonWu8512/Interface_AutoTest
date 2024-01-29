# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 11:11 上午
@Author  : Demon
@File    : ApiPermissionApply.py
"""

from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request
from urllib import parse

class ApiPermissionApply(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/permission'

    def api_apply(self, orders, filter=None, currentPage: int = 1, page: int = 20):
        """
        申请爆表权限
        :param page : 每页显示条数 默认 20
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/apply")
        body = {
            "filter": filter
        }

        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_approve(self, orders, filter=None, currentPage: int = 1, page: int = 20):
        """
        报表审批
        :param page : 每页显示条数 默认 20
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/approve")
        body = {
            "filter": filter
        }

        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_fetch_by_user(self, orders, filter=None, currentPage: int = 1, page: int = 20):
        """
        查询报表集市中我的申请记录
        :param orders : 条件 [{"column": "applyTime", "orderBy": "desc"}]
        :param filter : 过滤条件
        :param currentPage : 当前页码 默认 1
        :param page : 每页显示条数 默认 20
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchByUser")
        body = {
            "filter": filter,
            "pageSize": page,
            "currentPage": currentPage,
            "orders": orders,
        }

        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_fetch_approve_by_user(self, orders=None, filters=None, cpage=1, pages=20):
        """
        查询报表集市中我的审批记录
        :param orders : 条件 [{"column": "applyTime", "orderBy": "desc"}]
        :param filter : 过滤条件
        :param currentPage : 当前页码 默认 1
        :param page : 每页显示条数 默认 20
        :return
        """
        api_url = parse.urljoin(self.host, "/api_bi/permission/fetchApproveByUser")
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyTime", "orderBy": "desc"}],
        }

        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_fetch_approve_user(self, orders=None, filters=None, cpage=1, pages=20):
        """
        审批报表操作
        :return
        """
        api_url = parse.urljoin(self.host, "/api_bi/permission/fetchApproveUser")
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyTime", "orderBy": "desc"}],
        }

        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)