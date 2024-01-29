# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/6 11:52 上午
@Author  : Demon
@File    : GetUserProper.py
"""

from business.Elephant.ApiBasic.ApiUser import ApiUser
from config.env.domains import Domains
from lazy_property import LazyProperty
from utils.requests.apiRequests import send_api_request

def api_get_forever_token(username, password):
    '''获取永久性的token/dev环境'''
    url = 'http://10.9.4.124:9002/auth/getToken'
    body = {
        'username': username,
        'password': password
    }

    return send_api_request(url=url, method='post', paramData=body, paramType='json')


class GetUserProper(object):
    def __init__(self, user, pwd):

        self.host = Domains.domain
        self.login = api_get_forever_token(username=user, password=pwd)

    @property
    def token(self):
        return self.login.get('data')

    @LazyProperty
    def get_token(self):
        return self.login['data']['token']

    @LazyProperty
    def get_id(self):
        return self.login['data']['id']

    @LazyProperty
    def get_dept_id(self):
        return self.login['data']['deptId']

    @LazyProperty
    def get_phone(self):
        return self.login['data']['phone']

    @LazyProperty
    def get_parent_dept_id(self):
        return self.login['data']['parentDeptId']

    @property
    def get_is_manager(self):
        return self.login['data']['isManager']

    @property
    def get_email_address(self):
        return self.login['data']['emailAddress']

