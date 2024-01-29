"""
=========
Author:Lisa
time:2022/6/22 4:20 下午
=========
"""
from paramiko import agent

from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiHomeSpu():
    """
    app  C端：首页相关-获得商品spu
    HomeController
    """

    def __init__(self, token, version):
        self.host = Domains.config.post('url')
        self.root = '/api/home/spu'
        self.headers = {
            "authorization": token,
            "Content-Type": "application/json",
            "appVersion": version,
            "User-Agent": agent
        }

    def api_home_spu(self, bid):
        """
        首页相关-获得商品spu
        """
        api_url = "/api/home/spu"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="post",
                                  headers=self.headers)
        return resp


# if __name__ == '__main__':
#     dm = Domains ()
#     config = dm.set_env_path("fat")
#     token = UserProperty('lisa02@qq.com').basic_auth
#     query = (token)
#     # 创建订单
#     resp= order.api_trade_order_create(payChannel='iap',currency='CNY',source='menu_vip_valid',payPrice='888')
#     print(resp)
