# -*- coding: utf-8 -*-
# @Time: 2021/3/12 8:43 下午
# @Author: ian.zhou
# @File: ApiSso
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAdminAuth:
    """
    eshop商城后台用户权限
    """
    root = '/api/admin/eshop/sso'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_login(self, code):
        """
        登录获取token
        :param code: SSO auth code
        :return:
        """
        api_url = f"{self.host}{self.root}/login"
        body = {
            'code': code
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_roles(self):
        """
        获取用户权限
        :return:
        """
        api_url = f"{self.host}{self.root}/roles"
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_logout(self):
        """
        退出登录
        :return:
        """
        api_url = f"{self.host}{self.root}/logout"
        resp = send_api_request(method='post', url=api_url, headers=self.headers)
        return resp


