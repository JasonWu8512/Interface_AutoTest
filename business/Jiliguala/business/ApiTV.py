# -*- coding: utf-8 -*-
# @Time    : 2021/6/24 15:26 下午
# @Author  : 万军
# @File    : ApiDbInner.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTV:
    """
    通用业务服务
    """
    root = '/api/tvlogin'

    def __init__(self, token):
        self.headers = {'Authorization': token}
        self.host = Domains.domain

    def api_tv_login_code(self):
        """
        安卓电视 - tvlogin code
        :return:
        """

        api_url = f'{self.host}{self.root}/code'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_tv_login_mobile(self, uid, code):
        """
        :param code: code
        :param uid: uid
        :return:
        """

        api_url = f'{self.host}{self.root}/mobile'
        body = {
            'code': code,
            'uid': uid

        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_tv_login_refresh(self, code):
        """
        安卓电视 - tvlogin refresh
        :param code: code
        :return:
        """

        api_url = f'{self.host}{self.root}/refresh'
        body = {
            'code': code

        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    TV = ApiTV('Basic YTU2YjA2YTg3NmYzNDEyOWE2MjgxZjczNTY0ZjNlZWQ6MmM4NDc1YjZkMjNmNGFlM2E5YjhlNTFhNTc0YjEzOWU=')
    print(TV.api_tv_login_code())
    print(TV.api_tv_login_mobile(uid='cde1e1c126d5490ca9072fef8bf0a874', code='j3oO'))
    print(TV.api_tv_login_refresh(code='1'))





