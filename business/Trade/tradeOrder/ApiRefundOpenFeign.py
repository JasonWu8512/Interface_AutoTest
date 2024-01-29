# -*- coding: utf-8 -*-
# @Time: 2021/6/16 9:54 下午
# @Author: ian.zhou
# @File: ApiRefundOpenFeign
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiRefund:
    """
    订单退款
    """
    root = '/api/trade-order/refund'

    def __init__(self):
        self.headers = {'authorization': 'Basic ZGY4YzkwMTViY2UyNGI3ZDgyMzBmMzM0NWIwMjg0MTY6OGE1MzBmYjU2YjAyNGQ0Y2JlODU2ZDI3N2FmNDE1MWU=',
                        'Content-Type': 'application/json'}
        self.host = Domains.domain

    def api_order_refund(self, orderNo, desc=None, amount=None, refundNo=None, isOffline=False):
        """
        修改订单地址-获取订单当前收货信息，判断订单是否能够修改地址
        :param orderNo: 订单号
        :param amount: 退款金额
        :param refundNo: 退款工单单号
        :param isOffline: 是否线下退款
        :param desc: 退款原因
        :return:
        """

        api_url = f'{self.host}{self.root}'
        body = {
            'orderNo': orderNo,
            'amount': amount,
            'refundNo': refundNo,
            'isOffline': isOffline,
            'desc': desc
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    dm.set_domain("https://fat.jiliguala.com")
    refund = ApiRefund()
    res = refund.api_order_refund(orderNo='O71400736428605440')
    print(res)