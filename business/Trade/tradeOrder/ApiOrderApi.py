# -*- coding: utf-8 -*-
# @Time: 2021/5/5 2:05 下午
# @Author: ian.zhou
# @File: ApiOrderApi.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiOrderApi:
    """
    订单
    """
    root = '/api/trade-order/order'

    def __init__(self, token):
        self.headers = {'Authorization': token, "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_order_address_prepare(self, orderNo):
        """
        修改订单地址-获取订单当前收货信息，判断订单是否能够修改地址
        :param orderNo: 订单号
        :return:
        """

        api_url = f'{self.host}{self.root}/address/prepare'
        body = {
            'orderNo': orderNo
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_order_address_commit(self, orderNo, recipient='测试订单', mobile='12345678901',
                       addressProvince='黑龙江省', addressCity='双鸭山市', addressDistrict='宝山区',
                       addressStreet='测试地址'):
        """
        修改订单地址
        :param orderNo: 订单号
        :param recipient: 收货地址: 收件人
        :param mobile: 收货地址: 收件人手机号
        :param addressProvince: 收货地址: 省份/自治区/直辖市
        :param addressCity: 收货地址: 市
        :param addressDistrict: 收货地址: 区/县
        :param addressStreet: 收货地址: 详细地址
        :return:
        """

        api_url = f'{self.host}{self.root}/address/commit'
        body = {
            'orderNo': orderNo,
            'recipientAddress': {
                'recipient': recipient,
                'mobile': mobile,
                'addressProvince': addressProvince,
                'addressCity': addressCity,
                'addressDistrict': addressDistrict,
                'addressStreet': addressStreet
            }
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_order_myorder(self, page=0, pageSize=10):
        """
        查询我的订单
        :param page:页码
        :param pageSize:页面大小
        """
        api_url = f'{self.host}{self.root}/myorder'
        body = {
            'page': page,
            'pageSize': pageSize
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_order_detail(self, orderNo):
        """
        查询订单详情
        :param orderNo:订单号
        """
        api_url = f'{self.host}{self.root}/myorder/{orderNo}'
        body = {

        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    user = UserProperty(mobile='17521157699')
    print("user:", user.basic_auth)
    order = ApiOrderApi(token=user.basic_auth)
    # print(order.api_order_address_commit(orderNo='O53677602862534656'))
    # print(order.api_order_myorder())
    print(order.api_order_detail(orderNo='O61600184948469760'))