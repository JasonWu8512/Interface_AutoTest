# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/22 6:23 下午
@Author  : Demon
@File    : GetUserProperty.py
"""

from business.zero.ApiUser.ApiUser import ApiLoginUser
from utils.requests.apiRequests import send_api_request
from urllib import parse
from config.env.domains import Domains


class GetUserProperty(object):

    def __init__(self, users='zero_demon'):
        # 请求头文件
        login = ApiLoginUser()
        self.infos = login.api_auth_login(
            user=Domains.config.get(users).get('user'),
            pwd=Domains.config.get(users).get('pwd'),
        )

    @property
    def get_token(self):
        return self.infos.get('token')

    @property
    def get_id(self):
        return self.infos.get('id')


if __name__ == '__main__':

    Domains.set_env_path('dev')
    alu = GetUserProperty()
    print(alu.get_id)