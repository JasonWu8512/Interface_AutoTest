# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 10:34 上午
@Author  : Demon
@File    : ApiPermissionApprove.py
"""


from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request

class ApiPermissionApprove(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_meta/permissionApprove'

    def api_fetch_all_by_approve_status(self, filters, pages=20, cpage=1, orders=None, statu=0):
        """
        表权限审批记录查询
        :param filters :
        :param orders :
        :return
        """
        url = self.host + f'{self.root}/fetchAllByApproveStatus'
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyUpdateTime", "orderBy": "desc"}],
            "status": statu
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)

    def api_fetch_waiting_approve(self, filters, pages=20, cpage=1, orders=None, statu=0):
        """
        查询待审批记录
        :param filters :
        :param orders :
        :return
        """
        url = self.host + f'{self.root}/fetchWaitingApprove'
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyUpdateTime", "orderBy": "desc"}],
            "status": statu
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)

    def api_fetch_all(self, filters, pages=20, cpage=1, orders=None, statu=0):
        """
        查询全部权限审批记录
        :param filters :
        :param orders :
        :return
        """
        url = self.host + f'{self.root}/fetchAll'
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyUpdateTime", "orderBy": "desc"}],
            "status": statu
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)

    def api_update(self, filters, pages=20, cpage=1, orders=None, statu=0):
        """
        更新权限审批记录
        :param filters :
        :param orders :
        :return
        """
        url = self.host + f'{self.root}/update'
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyUpdateTime", "orderBy": "desc"}],
            "status": statu
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)