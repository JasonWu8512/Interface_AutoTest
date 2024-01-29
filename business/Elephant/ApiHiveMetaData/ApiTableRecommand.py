# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 10:55 上午
@Author  : Demon
@File    : ApiTableRecommand.py
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
        self.root = '/api_meta/tableRecommand'

    def api_add(self):
        """
        添加表为推荐
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/add')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')

    def api_delete(self):
        """
        删除表的推荐
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/delete')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')

    def api_select(self):
        """
        查询表的推荐信息
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/select')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')