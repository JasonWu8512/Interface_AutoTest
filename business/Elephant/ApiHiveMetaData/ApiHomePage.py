# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 10:45 上午
@Author  : Demon
@File    : ApiHomePage.py
"""


from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request
from urllib import parse

class ApiHomePage(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_meta/homepage'

    def api_select(self):
        """
        查询元数据管理页面初始化信息
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/select')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')

    def api_fetch_7day_data(self):
        """
        查询元数据管理页面7天内信息初始化
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/fetch7DayData')
        return send_api_request(url=url, headers=self.headers, paramType='json', method='post')