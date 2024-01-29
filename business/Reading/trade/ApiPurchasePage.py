# coding=utf-8
# @Time    : 2021/5/12 5:34 下午
# @Author  : Karen
# @File    : ApiPurchasePage.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiPurchasePage(object):
    ''' 购买页 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_v2_vip_purchase(self):
        """
        01）v1.4.0之后的购买页（年卡+终身卡sku）
        """
        api_url = "/api/v2/vip/purchase"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp


    def api_vip_iap(self):
        """
        02）iOS reviewmode下的购买页
        """
        api_url = "/api/vip/iap"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, method="get", headers=self.headers)
        return resp

