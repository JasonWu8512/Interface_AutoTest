# coding=utf-8
# @Time    : 2021/5/25 1:38 下午
# @Author  : Karen
# @File    : ApiCreateOrder.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiCreateOrder(object):
    ''' 下单 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_get_order(self,id):
        """ 01）获取订单状态 """
        api_url = "/api/order"
        body = {"id": id}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_create_order(self,itemId):
        """ 02）仅创建订单，不涉及支付 """
        api_url = "/api/order"
        body = {
            "itemId": itemId
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post",
                                headers=self.headers)
        return resp



    def api_order_charge(self,itemId,channel,couponRecordId=None):
        """ 03）创建订单，并请求 ping++ ，返回 ping++ 的 charge 对象 """
        api_url = "/api/order/charge"
        body = {
            'itemId': itemId,
            'channel': channel
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=self.headers)
        return resp


    def api_order_pingpp_charge(self, oid, channel):
        """ 04）请求 pingpp ，创建 pingpp 的 charge 对象"""
        api_url = "/api/order/pingpp-charge"
        body = {
            'oid': oid,
            'channel': channel
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post",
                                headers=self.headers)
        return resp


    def api_order_iap(self,itemId,transactionId,receiptData):
        """ 05）iOS reviewmode下的iap上报 """
        api_url = "/api/order/iap"
        body = {
            'itemId': itemId,
            'transactionId': transactionId,
            'receiptData': receiptData
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=self.headers)
        return resp


    def api_order_ios_failed(self):
        """ 06）ios支付失败后发送短信 v1.9.1 """
        api_url = "/api/order/ios/failed"
        body ={}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=self.headers)
        return resp


    def api_user_iap_restore(self,itemId,receiptData):
        """ 07）ios iap恢复购买 """
        api_url = "/api/user/iap/restore"
        body ={
            'itemId': itemId,
            'receiptData': receiptData

        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=self.headers)
        return resp


    def api_order_charge_paying(self, oid):
        """ 08）支付完成后由客户端触发将订单变为 paying 状态 """
        api_url = "/api/order/charge/paying"
        body = {'oid': oid}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=self.headers)
        return resp

    def api_order_refund(self, id):
        """ 09）订单退款 """
        api_url = "/api/circulars/order/refund"
        body = {'id': id}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post", headers=self.headers)
        return resp