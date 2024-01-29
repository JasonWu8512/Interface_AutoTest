# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 11:18 上午
@Author  : Demon
@File    : ApiCollection.py
"""

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiCollection(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/collection'

    def api_fetch_list(self, keyword=None):
        """
        查询报表集市中我的收藏
        :param :keyword : 模糊筛选报告id或者name
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchList")
        body = {
            "param": keyword
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_operation(self, report_id):
        """
        操作报表：收藏/取消
        :param :report_id : 报表ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/operation")
        body = {
            "report_id": report_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)


