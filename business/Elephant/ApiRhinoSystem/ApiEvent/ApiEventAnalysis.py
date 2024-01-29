# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 11:59 上午
@Author  : Demon
@File    : ApiEventAnalysis.py
"""

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiEventAnalysis(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/eventAnalysis'

    def api_check_name(self, event_name):
        """
        检查事件分析名称是否重复
        :param event_name :名称
        """
        api_url = self.host + f'{self.root}/checkName'
        body = {
            'event_name': event_name
        }
        return send_api_request(method='post', paramData=body, paramType='json', headers=self.headers, url=api_url)