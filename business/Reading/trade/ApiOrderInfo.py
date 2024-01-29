# coding=utf-8
# @Time    : 2021/5/25 1:38 下午
# @Author  : Karen
# @File    : ApiOrderInfo.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiOrderInfo(object):
    ''' 订单信息相关 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_order_list(self):
        """ 01）获取订单列表页 """
        api_url = "/api/order/list"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, method="get", headers=self.headers)
        return resp


    def api_order_detail(self,oid):
        """ 02）获取订单详情页 """
        api_url = "/api/order/detail"
        body = {'oid': oid}
        resp = send_api_request(url=self.host + api_url, paramType='params',paramData=body, method="get", headers=self.headers)
        return resp


    def api_order_gifts(self,oid):
        """ 03）获取订单的赠品 """
        api_url = "/api/order/gifts"
        body = {'oid': oid}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='params', method="get", headers=self.headers)
        return resp


    def api_order_logistics_detail(self,oid):
        """ 04）获取订单物流信息 """
        api_url = "/api/order/logistics/detail"
        body = {"oid":oid}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='params', method="get", headers=self.headers)
        return resp


    def api_order_address(self, oid, name, phone, province, city, district, detail):
        """ 05）填写地址 """
        api_url = "/api/order/address"
        body ={
            'oid': oid,
            'name': name,
            'phone': phone,
            'province': province,
            'city': city,
            'district': district,
            'detail': detail
        }
        resp = send_api_request(url=self.host + api_url, paramType='json',paramData=body, method="put", headers=self.headers)
        return resp


    def api_order_notice(self, pos):
        """ 06）获取当前物流公告 """
        api_url = "/api/order/notice"
        body = {'pos': pos}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='params', method="get",
                                headers=self.headers)
        return resp
