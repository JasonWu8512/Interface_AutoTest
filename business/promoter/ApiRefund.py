# coding=utf-8
# @Time    : 2020/12/3 11:29 上午
# @Author  : jerry
# @File    : ApiRefund.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiRefund:
    """
    退款脚本
    本脚本里面使用的token暂时无时效性
    """

    def __init__(self):
        self.headers = {"version": "1", "control": "no-cache", "Content-Type": "application/json",
                        "authorization": "Basic ZGY4YzkwMTViY2UyNGI3ZDgyMzBmMzM0NWIwMjg0MTY6OGE1MzBmYjU2YjAyNGQ0Y2JlODU2ZDI3N2FmNDE1MWU="}
        self.host = Domains.domain

    def api_refund(self, id):
        """
        订单退款
        param:id pingxxorder里的订单id
        """
        api_url = f'{self.host}/api/trade-order/refund'
        body = {
            "orderNo": id
        }
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    refund = ApiRefund()
    res = refund.api_refund("C94699")
    print(res)