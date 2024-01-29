# coding=utf-8

import base64

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from utils.decorators import switch_db
from utils.middleware.mongoLib import MongoClient


class ApiUser(object):
    """
    用户注册登录
    """

    def __init__(self):
        # 请求头文件
        self.header = {
            "version": "1",
            'Content-Type': 'application/json;charset=UTF-8',
        }
        self.host = Domains.domain

    # 登录接口
    def api_login(self, typ, u, p):
        """
        :param u:  手机
        :param p:  验证码 or 密码
        :param typ:  mobilecode or mobile
        :return:
        """
        api_url = "/api/user/auth"
        body = {
            "u": u,
            "p": p,
            "typ": typ
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
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
        resp = self.api_login(typ, u, p)
        _id = resp['data']['_id']
        tok = resp['data']['tok']
        a = (_id + ":" + tok).encode("utf-8")
        token = "Basic" + " " + str(base64.b64encode(a), encoding="utf-8")
        return token

    def api_get_user_sms(self, mobile, ggheader):
        """
        发送手机验证码
        """
        api_url = "/api/user/sms"
        body = {"mobile": mobile}
        header = {'Content-Type': 'application/json;charset=UTF-8', "GGHeader-V2": ggheader}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=header)
        return resp

    def api_get_user_sms_login(self, mobile, ggheader, type='text'):
        """
        发送手机验证码
        """
        api_url = "/api/user/sms"
        body = {"mobile": mobile, "type": type}
        header = {'Content-Type': 'application/json;charset=UTF-8', "GGHeader-V2": ggheader}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=header)
        return resp

    @switch_db('jlgl')
    def get_jlgl_user(self, mobile):
        with MongoClient("JLGL", "users") as client:
            return client.find_one({"mobile": mobile})

    def api_put_guest(self):
        '''创建游客'''
        api_url = "/api/user/guest"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.header)
        return resp



    def get_guest_token(self):
        """
        获取游客token
        """
        resp = self.api_put_guest()
        _id = resp['data']['_id']
        tok = resp['data']['tok']
        a = (_id + ":" + tok).encode("utf-8")
        token = "Basic" + " " + str(base64.b64encode(a), encoding="utf-8")
        print('游客token:',token)
        return token


class ApiBaby(object):
    """
    创建宝贝
    """

    def __init__(self, token):
        self.header = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_put_baby(self,birthday='2020-09-21T00:00:00.000+08'):
        '''创建宝贝'''
        api_url = "/api/babies"
        body = {
            "birthday": birthday
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.header)
        return resp