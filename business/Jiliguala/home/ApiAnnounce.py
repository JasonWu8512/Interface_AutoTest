# -*- coding: utf-8 -*-
# @Time : 2021/5/23 9:35 下午
# @Author : Cassie
# @File : ApiAnnounce.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAnnounce():
    """
    老呱美1.5获取首页弹窗
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/users/homeannounce'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_announce(self, bid):
        """
        老呱美1.5获取首页弹窗
        :param bid:宝贝id
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    version=config['version']['ver16.0']
    print(version)
    user = UserProperty("15958112857")
    token = user.basic_auth
    announce = ApiAnnounce(token,version)
    resp = announce.api_get_announce("0e5c5f66135641e881a9000fe60d2622")
    print(resp)
