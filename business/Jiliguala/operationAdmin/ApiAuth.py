# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 3:50 下午
# @Author  : zoey
# @File    : ApiAuth.py
# @Software: PyCharm


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.sso.ApiSso import ApiSso


class ApiAdminAuth:
    """
    eshop商城后台登录
    """
    root = '/api/admin/eshop/sso'

    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.host = Domains.domain
        self.host = Domains.config.get('url')

    def api_login(self, username, password):
        """
        获取token
        :param username: 用户
        :param password: 密码
        :return:
        """
        api_url = f"{self.host}{self.root}/login"
        code = ApiSso(email_address=username, pwd=password).sso_code
        body = {
            'code': code
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp
