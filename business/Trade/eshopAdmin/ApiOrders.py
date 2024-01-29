# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 2:10 下午
# @Author  : zoey
# @File    : ApiOrders.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiOrders:
    """
    eshop 商城管理后台-订单管理-订单列表
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_orders(self, pageSize=20, pageNo=0, orderNo=None, user=None, orderState=None, payChannel=None,
                       createAtAfter=None, createAtBefore=None):
        """
        获取订单列表
        :param pageNo: 页面编号
        :param pageSize: 一页展示的商品数量
        :param createAtAfter: 订单创建开始时间
        :param createAtBefore: 订单创建结束时间
        :param orderNo: 订单号
        :param user: 用户手机号或呱号
        :param orderState: 订单状态（1：未付款，2：已付款，5：已退款，6：已取消）
        :param payChannel: 支付方式
        """
        api_url = f'{self.host}{self.root}/orders'
        body = {
            "pageSize": pageSize,
            "pageNo": pageNo,
            "orderNo": orderNo,
            "user": user,
            "orderState": orderState,
            "payChannel": payChannel,
            "createAtAfter": createAtAfter,
            "createAtBefore": createAtBefore
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_get_orders_detail(self, orderNo=None):
        """
        订单详情
        :param orderNo：订单号
        """
        api_url = f'{self.host}{self.root}/orders/detail'
        body = {
            "orderNo": orderNo
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_get_orders_platform(self):
        """
        获取售卖平台
        """
        api_url = f'{self.host}{self.root}/orders/platform'
        body = {
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_again_orders_semester(self, orderNo=None):
        """
        重新开课
        :param orderNo：订单号
        """
        api_url = f'{self.host}{self.root}/orders/semester-begin'
        body = {
            "orderNo": orderNo
        }
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp

    def api_again_orders_jst(self, orderNo=None):
        """
        重推订单
        :param orderNo：订单号
        """
        api_url = f'{self.host}{self.root}/orders/jst-upload'
        body = {
            "orderNo": orderNo
        }
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp