# coding=utf-8
# @Time    : 2021/6/3
# @Author  : shery
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class Shanyan(object):

    def __init__(self, token):
        self.headers = {"version": "1", "user-agent": "niuwa/11.5.0 (iPhone; iOS 14.1; Scale/2.00)"
                                                            "190711.020); NiuWa : 110600; AndroidVersion : 11.6.0",
                              "content-Type": "application/json", "x-app-params": "deviceId=f9d57a6e213b975d&"
                                                                                  "deviceType=""vivo V2001A",
                              "x-app-version": "version=110600&platform=1&model=0"}
        self.host = Domains.domain

    def shanyan_login_v3(self, token, appId, pandora):
        """闪验v3"""
        api_url = "/api/user/shanyan/login/v3"
        body = {
            "token": token,
            "appId": appId,
            "pandora": pandora
        }
        res = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                               headers=self.headers)
        return res

    def shanyan_login_v2(self, token, appId, pandora):
        """闪验v2"""
        api_url = "/api/shanyan/login/v2"
        body = {
            "token": token,
            "appId": appId,
            "pandora": pandora
        }
        res = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                               headers=self.headers)
        return res

    def shanyan_login_v1(self, token, appId, pandora):
        """闪验v1"""
        # 线上无调用量，暂不维护
        api_url = "/api/shanyan/login"
        body = {
            "pandora": pandora
        }
        res = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                               headers=self.headers)
        return res

    def shanyan_guest_upgrade(self, token, appId, pandora):
        """从闪验升级"""
        api_url = "/api/shanyan/guest/upgrade"
        body = {
            "token": token,
            "appId": appId,
            "pandora": pandora
        }
        res = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                               headers=self.headers)
        return res
