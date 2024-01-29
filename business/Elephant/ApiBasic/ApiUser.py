# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/6 10:39 上午
@Author  : Demon
@File    : ApiLessonCentral.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from business.Elephant.commons.common import TOKEN
from urllib import parse



class ApiUser(object):

    def __init__(self):
        # 请求头文件
        self.headers = header
        self.host = Domains.domain

    # 登录接口
    def api_auth_login(self, user, pwd, uuid, code):
        """
        :param user:  账户
        :param pwd:  密码
        :param uuid:  UUID
        :param code: 验证码
        :return:
        """
        api_url = "/api_basic/auth/login"
        body = {
            "password": pwd,
            "username": user,
            "uuid": uuid,
            "vcode": code
        }
        resp = send_api_request(url=parse.urljoin(self.host, api_url), paramType="json", paramData=body, method="post",
                                headers=self.headers)
        return resp

    def get_token(self, uuid, code, user="demon_jiao@jiliguala.com", pwd="demon_jiao123"):
        """
        获取验证的token
        :param user : 用户名
        :param pwd : 密码
        :param uuid : 随机码
        :param code : 图片验证码
        :param return :token
        """
        t = self.api_auth_login(user, pwd, uuid, code)
        if t.get("data"):
            return t.get("data").get("token")
        return TOKEN

    def get_code(self):
        """
        从库里获取验证码
        :return : code
        """

        return

    def api_auth_vcode(self):
        """
        查询uuid数值
        :return: uuid
        """
        api_url = "/api_basic/auth/vcode"

        resp = send_api_request(url=self.host + api_url, method="post",
                                headers=self.headers)
        assert resp.get("data").get("uuid")
        return resp.get("data").get("uuid")

if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("http://10.9.4.124:8088")
    user = ApiUser()

    print(user.api_get_code())
    # print(user.api_get_token(uuid="Demon", code="ss"))

    print(user.api_auth_vcode())
