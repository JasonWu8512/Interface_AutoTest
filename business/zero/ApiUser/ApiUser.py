# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/22 6:01 下午
@Author  : Demon
@File    : ApiLessonCentral.py
"""
import jwt
from utils.middleware.dbLib import MySQL
from config.env.domains import Domains
from lazy_property import LazyProperty



class ApiLoginUser(object):

    def __init__(self, email):
        self.email = email

    # 登录接口
    @LazyProperty
    def get_zero_token(self):
        """
        :param email:  邮箱
        :return:
        """
        user_info = {'exp': 12 * 3600 * 1000}
        user = MySQL('zero', 'zero').query(sql=f'select id, username from auth_user where email = "{self.email}"')
        user_info['username'] = user[0]['username']
        user_info['user_id'] = user[0]['id']
        token = jwt.encode(payload=user_info, key='slg')
        return token

if __name__ == '__main__':

    Domains.set_env_path('dev')
    alu = ApiLoginUser()
    pl = alu.get_zero_token(email='zoey_zhang@jiliguala.com')

    print(pl)