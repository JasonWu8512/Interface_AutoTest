# -*- coding: utf-8 -*-
# @Time    : 2021/6/2 3:28 下午
# @Author  : jacky_yuan
# @File    : ApiGetsmslogin.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGetSmsLogin():
    """
    onboarding  C端： 获取验证码
    smslogin
    """
    def __init__(self):
        self.host = Domains.config.get('url')
        self.headers = {
            "Content-Type": "application/json"
        }

    def api_get_sms(self, target):
        """
        获取验证码
        :param target:电话号码
        :return:
        """
        api_url = "/api/user/sms/login/v2"
        body = {
            "target": target,
        }
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers, paramType="params",
                                paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    resp = ApiGetSmsLogin().api_get_sms(target="217621160716")
    print(resp)