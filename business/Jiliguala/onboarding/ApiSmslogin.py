# -*- coding: utf-8 -*-
# @Time    : 2021/6/2 2:30 下午
# @Author  : jacky_yuan
# @File    : ApiSmslogin.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiSmslogin():
    """
    onboarding  C端：验证码登录
    smslogin
    """

    def __init__(self):
        self.host = Domains.config.get('url')
        self.headers = {
            "Content-Type": "application/json",
            "Version": "1"
        }

    def api_sms_login(self, code, target, uid):
        """
        通过验证码登录
        :param code: 验证码
        :param target: 电话号码
        :param uid: 用户id
        :return:
        """
        api_url = "/api/user/sms/login/v2"
        body = {
            "code": code,
            "target": target,
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, method="post", headers=self.headers, paramType="json",
                                paramData=body)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    resp = ApiSmslogin().api_sms_login(code="4068", target="17621160716", uid="ca8b74f8f05e4dc7bcfac757867ee700")
    print(resp)