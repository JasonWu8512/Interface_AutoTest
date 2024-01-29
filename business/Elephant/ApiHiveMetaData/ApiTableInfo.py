# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 10:51 上午
@Author  : Demon
@File    : ApiTableInfo.py
"""

from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request
from urllib import parse

class ApiTableInfo(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_meta/tableInfo'

    def api_get_search_list(self):
        """
        查询元数据管理页面初始化信息
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/getSearchList')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')


    def api_fetch_all_table(self, uid=None, tagfilt=None, filt=None, pagesize=20, cpage=1, orders=[]):
        """
        根据标签，仓库，安全等级 获取表的所有table信息
        :param filt ,过滤规则 表名｜描述｜创建人
        :param pagesize ,每页大小
        :param cpage ,当前页码
        :param ordes ,排序规则 [{"column": "columnIdx", "orderBy": "asc"}]
        :param uid ,用户id 4be2756f72e2473c871c38a830cb5943
        :param tagfilt 标签过滤规则
        """
        if not tagfilt:
            tagfilt = {
                "tableTopic": None,
                "databaseName": None,
                "tableSecurity": None
            }
        body = {
            "filter": filt,
            "tagFilter": tagfilt,
            "userId": uid,
            "pageSize": pagesize,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "databaseName", "orderBy": "asc"}]
        }
        url = parse.urljoin(self.host, f'{self.root}/fetchAllTable')
        return send_api_request(url=url, headers=self.headers, paramType='json', paramData=body, method='post')

    def api_fetch_table_info(self, uid=None, dbname=None, tbname=None):
        """
        根据标签，仓库，安全等级 获取表的所有table信息
        :param tableName ,表名
        :param databaseName ,库名
        :param userId ,用户uid
        :return
        """
        body = {
            "tableName": tbname,
            "databaseName": dbname,
            "userId": uid,
        }
        url = parse.urljoin(self.host, f'{self.root}/fetchTableInfo')
        return send_api_request(url=url, headers=self.headers, paramType='json', paramData=body, method='post')

    def api_get_database_list(self):
        """
        获取数据库列表
        :return
        """

        url = parse.urljoin(self.host, f'{self.root}/getDatabaseList')
        return send_api_request(url=url, headers=self.headers, method='post')

