# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 2:29 下午
@Author  : Demon
@File    : ApiLessonCentral.py
"""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiUser(object):
    def __init__(self, cookies=None):
        # 请求头文件
        self.headers = header
        self.host = Domains.config.get('crm_number_url')
        self.root = '/api/account'

    def api_oa_account_login(self, sso_code):
        # 新版sso-oa账号登录
        api_url = parse.urljoin(self.host, f"{self.root}/auth_oa_token")
        body = {
            "sso_auth_code": sso_code
        }
        return send_api_request(url=api_url, paramData=body, paramType='json', method="post",
                                headers=self.headers)

    def api_account_login(self, sso_code, app_name='crm'):
        """
        :param app_name:  默认crm
        :param sso_auth_code:  sso 登陆code
        :return:
        """

        api_url = parse.urljoin(self.host, f"{self.root}/auth_token")
        body = {
            "app_name": app_name,
            "sso_auth_code": sso_code
        }
        resp = send_api_request(url=api_url, paramData=body, paramType='json', method="post",
                                headers=self.headers)
        return resp

    def api_account_logout_sso(self, cookies):
        """退出登录"""
        api_url = parse.urljoin(self.host, f"{self.root}/logout_sso")
        return send_api_request(url=api_url, paramType='json', paramData={}, cookies=cookies, method='post')


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('dev')
    print(config)
    print(Domains.config)
