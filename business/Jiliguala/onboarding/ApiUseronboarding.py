# -*- coding: utf-8 -*-
# @Time    : 2021/6/2 3:55 下午
# @Author  : jacky_yuan
# @File    : ApiUseronboarding.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUseronboarding():
    """
    onboarding  C端：登录创建baby
    Useronboardin
    """

    def __init__(self, version, agent):
        self.host = Domains.config.get('url')
        self.headers = {
            "Content-Type": "application/json",
            "X-APP-Version": version,
            "User-Agent": agent
        }

    def api_user_onboarding(self, nick, bd, auth):
        """
        onboarding创建baby
        :param nick: 宝贝昵称
        :param bd: 宝贝时间戳
        :param auth: 用户auth
        :return:
        """
        api_url = "/api/user/onboarding"
        body = {
            "nick": nick,
            "bd": bd,
            "auth": auth
        }
        resp = send_api_request(url=self.host + api_url, method="post", headers=self.headers, paramType="json",
                                paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    resp = ApiUseronboarding().api_user_onboarding(nick="宝贝", bd="1527897600000",
                                                   auth="Basic OWM5NjhiMzVhZDY1NDE2ZWE4MWI3YTIyNGE2M2M3Y2Y6MjYyNmQ2ZTliNTZiNGFiN2I0YTBiYTM0NzVjNTlmMDI=")
    print(resp)
