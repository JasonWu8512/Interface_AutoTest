# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:43 上午
# @Author  : zoey
# @File    : ApiCommodity.py
# @Software: PyCharm
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiCommodity:
    """
    eshop 商城微信C端
    """

    def __init__(self, token):
        self.host = Domains.domain
        self.root = '/api/eshop'
        self.headers = {'Authorization': token, "Content-Type": "application/json"}

    """--------------------------------商品相关CommodityController-------------------------------------"""
    def api_get_commodity_detail(self, itemid):
        """
        获取商品详情
        :param itemid:
        :return:
        """
        api_url = f'{self.host}{self.root}/commodity/{itemid}'
        resp = send_api_request(url=api_url,
                                method='get', headers=self.headers)
        return resp

    def api_get_commodity_rolling(self, itemid):
        """
        :param itemid:
        :return:
        """
        api_url = f'{self.host}{self.root}/commodity/{itemid}/rolling'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_get_commodity_groups(self, itemid, promotionId=''):
        """
        获取该商品的拼团活动
        :param itemid:
        :param promotionId:
        :return:
        """
        api_url = f'{self.host}{self.root}/commodity/{itemid}/groups'
        body = {
            'promotionId': promotionId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params',
                                headers=self.headers)
        return resp


