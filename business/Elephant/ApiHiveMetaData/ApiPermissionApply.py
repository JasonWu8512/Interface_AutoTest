# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 10:28 上午
@Author  : Demon
@File    : ApiPermissionApply.py
"""


from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request

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
        self.root = '/api_meta/permissionApply'

    def api_fetch_by_user(self, filters, pages=20, cpage=1, orders=None):
        """
        查询当前账户申请的表的记录
        :param filters :
        :orders filters :
        :return
        """
        url = self.host + f'{self.root}/fetchByUser'
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyUpdateTime", "orderBy": "desc"}]
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)

    def api_fetc_all_table(self, filters, pages=20, cpage=1, orders=None):
        """
        查询所有表信息
        :param filters :
        :orders filters :
        :return
        """
        url = self.host + f'{self.root}/fetchAllTable'
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyUpdateTime", "orderBy": "desc"}]
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)

    def api_fetc_one_table(self, filters, pages=20, cpage=1, orders=None):
        """
        查询一个表信息
        :param filters :
        :orders filters :
        :return
        """
        url = self.host + f'{self.root}/fetchOneTable'
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "applyUpdateTime", "orderBy": "desc"}]
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)

    def api_delete(self, filters, pages=20, cpage=1, orders=None):
        """
        删除对表的操作权限
        :param filters :
        :orders filters :
        :return
        """
        url = self.host + f'{self.root}/delete'
        body = {
            "filter": filters,
            "pageSize": pages,
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)

    def api_add(self, dbname, tbname, uid=None, operats=None, reason="测试", uname="demon_jiao"):
        """
        表权限申请
        :param dbname :
        :param tbname :
        :param operats : 权限列表 增删查/all  ['select']
        :return
        """
        url = self.host + '/api_meta/permissionApply/add'
        body = {
            "applyUser": uname,
            "databaseName": dbname,
            "tableName": tbname,
            "applyReason": reason,
            "userId": uid if uid else "c218b6effcdb4612a60cdcd900a1abac",
            "userOperationList": operats if operats else ["select"]
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=url)