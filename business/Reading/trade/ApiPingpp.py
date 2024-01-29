# coding=utf-8
# @Time    : 2021/5/25 1:39 下午
# @Author  : Karen
# @File    : ApiPingpp.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiPingpp(object):
    """ Ping++ """
    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def api_pingpp_charge_callback(self,oid):
        """ 01）ping++支付回调 """
        api_url = "/api/pingpp/charge/callback"
        headers = {"x-pingplusplus-signature": 'mock'}
        body = {
                "type": "charge.succeeded",
                "data": {
                    "object": {
                        "channel": "wx",
                        "order_no": oid,
                        "time_paid": 1622453619
                    }
                }
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=headers)
        return resp


    def api_pingpp_refund_callback(self,oid):
        """ 02）ping++退款回调 """
        api_url = "/api/pingpp/refund/callback"
        headers = {"x-pingplusplus-signature": 'mock'}
        body = {
                "type": "refund.succeeded",
                "data": {
                    "object": {
                        "charge_order_no": oid
                    }
                }
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=headers)
        return resp