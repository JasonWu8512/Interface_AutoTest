# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty
from business.Reading.user.ApiUser import ApiUser


class ApiOrder(object):
    """
    订单
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def api_order_list(self, page):
        """
        订单列表
        """
        api_url = "/api/order/list"
        body = {"page": page}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_order_detail(self, oid):
        """
        订单详情
        """
        api_url = "/api/order/detail"
        body = {"oid": oid}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_order_add_address(self, oid, addr, name, region, tel):
        """
        订单详情添加地址
        """
        api_url = "/api/order/addAddress"
        body = {"oid": oid,
                "addr": addr,
                "name": name,
                "region": region,
                "tel": tel
                }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    def api_order_logistics(self, oid, logisticscode):
        """
        获取物流
        """
        api_url = "/api/order/logistics"
        body = {"oid": oid,
                "logisticscode": logisticscode
                }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_env_path('fat')
    dm.set_domain("https://fat.jiliguala.com")
    mobile = '14021736031'
    user = UserProperty(mobile)
    token = user.basic_auth
    order = ApiOrder(token=token)
    # page = 0
    # res = order.api_order_list(page)
    # oid = 'O57266210068500480'
    # res = order.api_order_detail(oid)
    oid = 'O62025948675481600'
    # addr = '2号402'
    # name = 'Dododo'
    # region = '北京市 北京市 东城区'
    # tel = '18521736264'
    # res = order.api_order_add_address(oid, addr, name, region, tel)

    logistic_scode = '75438108066724'
    res = order.api_order_logistics(oid, logistic_scode)
    print(res)