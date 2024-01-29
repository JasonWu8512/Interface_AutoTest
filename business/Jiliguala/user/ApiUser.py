# coding=utf-8
# @Time    : 2020/8/5 4:37 下午
# @Author  : keith
# @File    : ApiUser

import base64
import random

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.businessQuery import usersQuery


class ApiUser(object):
    """
    用户注册登录
    """

    def __init__(self):
        # 请求头文件
        self.header = {
            "version": "1",
        }
        self.host = Domains.domain
        self.wx_app_header = {
            "version": "1",
            "openapp": "sp99",
            "Content-Type": "application/json",
            "Authorization": "Token"
        }

        query = usersQuery()

    # 登录接口
    def api_app_login(self, typ, u, p):
        """
        :param u:  手机
        :param p:  验证码 or 密码
        :param typ:  mobilecode or mobile
        :return:
        """
        api_url = "/api/users/tokens"
        body = {
            "u": u,
            "p": p,
            "typ": typ
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.header)
        return resp

    # 获取token
    def get_token(self, typ, u, p):
        """
        :param typ:
        :param u:
        :param p:
        :return:
        """
        resp = self.api_app_login(typ, u, p)
        _id = resp['data']['_id']
        tok = resp['data']['tok']
        a = (_id + ":" + tok).encode("utf-8")
        token = "Basic" + " " + str(base64.b64encode(a), encoding="utf-8")
        return token

    def api_app_register_user(self, u, p, typ, nick, ava, desc, bg):
        """
        :param u:
        :param p:
        :param typ:
        :param nick:
        :param ava:
        :param desc:
        :param bg:
        :return:
        """
        api_url = "/api/users"
        body = {
            "u": u,
            "p": p,
            "typ": typ,
            "nick": nick,
            "ava": ava,
            "desc": desc,
            "bg": bg
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="put",
                                headers=self.header)
        return resp

    # https://dev.jiliguala.com/api/openapp/login?jlglOpenapp=wx18f8075163853984&opencode=061lPHFa1OANAz0UawHa1euHD84lPHFa
    def api_wechat_app_login(self, jlglOpenapp):
        """
        :param jlglOpenapp:
        :return:
        """
        api_url = "/api/openapp/login"
        body = {
            "jlglOpenapp": jlglOpenapp,
            "opencode": "011JdI0w3W0PVU2JvW0w3SUIWL3JdI0W"
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.wx_app_header)
        return resp

    def get_mobile(self):
        """"
        随机生成手机号并返回
        """
        pho_prefix = "1280000"  # 手机号前缀
        pho_postfix = ""  # 手机号后缀
        for i in range(0, 4):
            pho_postfix = pho_postfix + str(random.randint(0, 9))

        pho_num = pho_prefix + pho_postfix  # 最终手机号
        return pho_num

    def api_register(self, mobile):
        """
        生成新用户
        """
        api_url = "/api/web/sms"
        body = {
            "mobile": mobile,
            "source": "Test",
            "crm_source": "sampleH5"
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body,
                                headers=self.header)
        return resp

    def get_new_user(self):
        """"
        创建新用户手机号并返回
        """
        # 随机生成手机号
        phone_num = self.user.get_mobile()
        # 查询该手机号是否已经在数据库存在
        query_res = self.query.get_users(mobile=phone_num)
        # 如果该手机号已经存在，则继续创建，直到该手机号在数据库不存在
        while query_res is not None:
            phone_num = self.user.get_mobile()
            query_res = self.query.get_users(mobile=phone_num)

        # 注册新用户
        self.user.api_register(phone_num)
        return phone_num


if __name__ == '__main__':
    dm = Domains()
    # dm.set_domain("https://fat.jiliguala.com")
    # dm.set_domain("https://jiliguala.com")
    user = ApiUser()
    print(user)
    mobile = user.get_mobile()
    userinfo = user.api_register(mobile)
    print(userinfo)
    # user.get_token(typ='mobile', u=18818207214, p=123456)
    # user.api_wechat_app_login("wx18f8075163853984")
    # print(user.get_open_user_token('13818207214'))
