# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 10:47 上午
@Author  : Demon
@File    : ApiMetaEnum.py
"""

from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request
from urllib import parse

class ApiMetaEnum(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_meta/metaEnum'

    def api_fetch_all(self):
        """
        查询元数据枚举值信息
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchAll')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')

    def api_add(self):
        """
        新增元数据枚举值信息
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/add')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')

    def api_delete(self):
        """
        删除元数据枚举值信息
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/delete')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')

    def api_update(self):
        """
        删除元数据枚举值信息
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/delete')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')
