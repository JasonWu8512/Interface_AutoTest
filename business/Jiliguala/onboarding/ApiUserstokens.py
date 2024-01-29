# -*- coding: utf-8 -*-
# @Time    : 2021/6/3 9:52 上午
# @Author  : jacky_yuan
# @File    : ApiUserstokens.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUserstokens(object):
    """
    onboarding  C端： 密码登录获取token
    Tokensv2
    """

    def __init__(self):
        self.host = Domains.config.get('url')
        self.headers = {
            "Content-Type": "application/json",
            "version": "1"
        }
    def api_users_tokens(self,u, p, typ):
        """
        :param u:  手机号 or 邮箱
        :param p:  密码
        :param typ:  mobile or email
        :return:
        """
        api_url = "/api/users/tokens"
        body = {
            "u": u,
            "p": p,
            "typ": typ
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    resp = ApiUserstokens().api_users_tokens(u="19811011212", p="123456", typ="mobile")
    print(resp)