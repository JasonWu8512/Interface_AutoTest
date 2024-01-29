# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/24 5:02 下午
@Author  : Demon
@File    : ApiRevenueTrafficInfo.py
"""



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse



class ApiRevenueTrafficInfo(object):

    def __init__(self, token):
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_visual/revenueTrafficInfo'

    def api_get_revenue_traffic_info(self):
        """查询实时营收
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/getRevenueTrafficInfo')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_get_revenue_hour(self):
        """查询实时营收 按小时刷新
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/getRevenueHour')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_get_complete_revenue(self):
        """查询实时营收 已完成目标营收
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/getCompleteRevenue')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)
