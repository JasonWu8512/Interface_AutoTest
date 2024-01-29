# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2022/6/28 17:05 上午
@Author   : Anna
@File     : ApiSc.py
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiSc():
    def __init__(self, token, version=None):
        self.host = Domains.config.get('url')
        self.root = '/api/sc'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_sc(self, bid):
        """
        拓展页面
        :param bid:宝宝id
        :return:
        """
        api_url = f"{self.host}{self.root}/table"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("12345678001")
    token = user.basic_auth
    version = config["version"]['ver12.1']

    # 拓展tab页面
    sc = ApiSc(token, version)
    resp = sc.api_get_sc("467f0668aeec404382e504cd5731e994")
    print(resp)
