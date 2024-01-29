# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:43 上午
# @Author  : zoey
# @File    : ApiGroup.py
# @Software: PyCharm
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiGroup:
    """
    eshop 商城微信C端
    """

    def __init__(self, token):
        self.host = Domains.domain
        self.root = '/api/eshop'
        self.headers = {'Authorization': token, "Content-Type": "application/json"}

    """-------------------------------------------groups相关GroupController----------------------------------"""

    def api_get_my_groups(self, promotionId, itemId):
        """
        获取我的拼团
        :param promotionId: 活动id
        :param itemId: 商品id
        :return:
        """
        api_url = f'{self.host}{self.root}/groups'
        body = {
            "promotionId": promotionId,
            "itemId": itemId
        }
        resp = send_api_request(url=api_url, method="get", paramData=body, paramType="params", headers=self.headers)
        return resp

    def api_get_group_detail(self, groupId):
        """
        查看团单信息
        :param groupId: 团单id
        :return:
        """
        api_url = f"{self.host}{self.root}/group/{groupId}"
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp

    def api_get_group_detail_v2(self, groupId):
        """
        查看团单信息
        :param groupId: 团单id
        :return:
        """
        api_url = f"{self.host}{self.root}/v2/group/{groupId}"
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp
