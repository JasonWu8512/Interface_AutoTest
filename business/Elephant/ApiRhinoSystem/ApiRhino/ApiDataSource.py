# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 11:51 上午
@Author  : Demon
@File    : ApiDataSource.py
"""



from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiDataSource(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/datasource'

    def api_fetch_list(self, ids):
        """
        根据ID查询
        :param :ids : 模糊筛选报告id或者name
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchById")
        body = {
            "param": ids
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)