# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 10:42 上午
@Author  : Demon
@File    : ApiColumnInfo.py
"""



from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request
from urllib import parse

class ApiColumnInfo(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_meta/columnInfo'

    def api_fetch_all_column(self, dbid, tbid, filt=None, pagesize=20, cpage=1, ordes=[]):
        """
        根据数据库id，表id 获取表的所有column信息
        :param dbid ,数据库id
        :param tbid ,表id
        :param filt ,过滤规则
        :param pagesize ,每页大小
        :param cpage ,当前页码
        :param ordes ,排序规则 [{"column": "columnIdx", "orderBy": "asc"}]
        """
        body = {
            "filter": filt,
            "databaseId": dbid,
            "tableId": tbid,
            "pageSize": pagesize,
            "currentPage": cpage,
            "orders": ordes
        }
        api_url = parse.urljoin(self.host, f'{self.root}/fetchAllColumn')
        return send_api_request(url=api_url, headers=self.headers, paramType='json', paramData=body, method='post')