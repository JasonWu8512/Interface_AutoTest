# -*- coding: utf-8 -*-
# @Time    : 2021/6/3 10:22 上午
# @Author  : jacky_yuan
# @File    : ApiUsersguestv2.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUsersguestv2(object):
    """
    onboarding  C端： 创建游客
    Usersguestv2
    """

    def __init__(self, version, agent):
        self.host = Domains.config.get('url')
        self.headers = {
            "Content-Type": "application/json",
            "X-APP-Version": version,
            "User-Agent": agent
        }

    def api_users_guestv2(self):
        api_url = "/api/users/guest/v2"
        resp = send_api_request(url=self.host + api_url, paramType="params", method="put",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    resp = ApiUsersguestv2().api_users_guestv2()
    print(resp)
