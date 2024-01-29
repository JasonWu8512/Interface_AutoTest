# coding=utf-8
# @Time    :
# @Author  : anna
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.businessQuery import usersQuery


class ApiSmsInfo(object):

    def __init__(self, token=None, version=None, anVersion=None, xApp=None):
        self.headers = {"authorization": token, "Content-Type": "application/json"}
        # if token:
        #     self.headers = {"Content-Type": "application/json"}
        if version:
            self.headers["X-App-Version"] = version
        if anVersion:
            self.headers["android-oaid-version"] = anVersion
        if xApp:
            self.headers["X-App-Params"] = xApp

        self.host = Domains.config.get('url')
        self.root = '/api/sms'
        self.root01 = '/api/users'

    def api_get_mobile(self):
        """开发内部接口查询可用手机号"""
        api_url = f"{self.host}/api/qa/fetchTestMobile"
        resp = send_api_request(url=api_url, method="get")
        print(resp)
        return resp

    def api_put_guest(self):
        """游客登陆"""
        api_url = f"{self.host}{self.root01}/guest/v2"

        resp = send_api_request(url=api_url, method="put",
                                headers=self.headers)
        return resp

    def api_get_login_v2(self, target, pandora):
        """
        获取验证码
        :param target:目标手机号
        :param pandora:登陆授权
        :return:
        """
        api_url = f"{self.host}/api/user/sms/login/v2"
        body = {
            "target": target,
            "pandora": pandora
        }

        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_post_login_v2(self, target, pandora, uid, code):
        """
        验证码登陆
        :param target:目标手机号
        :param pandora:登陆授权
        :param uid:用户id
        :param code:验证码
        :return:
        """
        api_url = f"{self.host}/api/user/sms/login/v2"
        body = {
            "target": target,
            "pandora": str(pandora, encoding='utf-8'),
            "uid": uid,
            "code": code
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_get_password(self, p, typ, u):
        """
       密码登陆
       :param p:密码
       :param typ:登陆类型
       :param u:手机号
       :return:
       """

        api_url = f"{self.host}{self.root01}/tokens/v2"
        body = {
            "p": p,
            "typ": typ,
            "u": u
        }
        resp = send_api_request(url=api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_get_sms(self, target, pandora=None):
        """
        购买详情页，登录获取验证码
        :param target:手机号
        :param pandora:用户token
        : return:
        """

        api_url = f"{self.host}{self.root}"
        body = {
            "target": target
        }
        if pandora:
            body['pandora'] = pandora

        resp = send_api_request(url=api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_post_sms(self, code, target):
        """
        游客绑定手机号后，更新用户信息
        :param pandora:用户token
        :param code:验证码
        :param target:手机号
        : return:
        """

        api_url = f"{self.host}{self.root}/guest/upgrade"
        body = {
            # "pandora": pandora,
            "code": code,
            "target": target

        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    def api_post_shanyan(self, token, pandora, appId):
        """
        闪验登录
        :param token:用户token
        :param pandora:授权信息
        :param appId:appId
        : return:
        """

        api_url = f"{self.host}/api/user/shanyan/login/v3"
        body = {
            "token": token,
            "appId": appId,
            "pandora": str(pandora, encoding='utf-8')
            # "pandora": pandora
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    def api_post_ping(self):
        """心跳监测"""
        api_url = f"{self.host}/api/user/ping"
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json")
        return resp




if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("fat")

    # # mobile = "15921263812"
    # # user = UserProperty(mobile)
    # # token = user.basic_auth
    # sms = ApiSmsInfo(token)
    #
    # # 验证游客账号登陆
    # resp01 = sms.api_put_guest()
    # print(resp01)
    #
    # # 验证获取验证码
    # resp02 = sms.api_get_login_v2(mobile)
    # print(resp02)
    #
    # pandora = "MTY1NTc5MzQ2NDIwODoyMDIwMDUxNDE1MDgxOWUzOWU2YzExMDNlYzExZTA0NTg4ODY4ZDY2MDM4MWM3MDFiNmE4MjY3ZGM5MWJkNToxNzEzY2YwNzE2MmM2MzE5ZmRmOTNkYzFmYWVmMmEzYg=="
    # # 查数据库，获取验证码
    # code = usersQuery().get_users(mobile=mobile)["sms"]["code"]
    # # 查数据库，获取uid
    # uid = usersQuery().get_users(mobile=mobile)["_id"]
    # print(code)
    # print(uid)
    # resp03 = sms.api_post_login_v2(mobile, pandora, uid, code)
    # print(resp03)
    #
    # # 验证密码登陆
    # p = '123456'
    # typ = 'mobile'
    # resp04 = sms.api_get_password('123456', 'mobile', '15921263812')
    # print(resp04)
