# -*- coding: utf-8 -*-
# @Time : 2021/6/21 1:24 下午
# @Author : saber
# @File : ApiGlobe.py

from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGlobe():
    """
      全局使用的标志位
      GlobeController
    """

    def __init__(self, token):
        self.host = Domains.config.get('url')
        self.root = '/api/globe'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            # "X-APP-Version": version
        }

    def api_get_anonymous(self, bid):
        """
        全局使用的标志位
        :param
        :return:
        """
        api_url = f"{self.host}{self.root}/anonymous"
        body = {

        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_globe(self):
        """
        全局使用的标志位
        :param
        :return:
        """
        api_url = f"{self.host}{self.root}"
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("15958112857")
    token = user.basic_auth
    globe = ApiGlobe(token)
    resp = globe.api_get_anonymous("0e5c5f66135641e881a9000fe60d2622")
    print(resp)
    resp02 = globe.api_get_globe()
    print('-----')
    print(resp02)
