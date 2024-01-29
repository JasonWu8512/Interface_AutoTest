# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2022/6/23 10:58 上午
@Author   : Anna
@File     : ApiHome.py
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty
from business.Reading.user.ApiUser import ApiUser


class ApiHome():
    def __init__(self, token=None, version=None, xApp=None):
        self.host = Domains.config.get('url')
        self.root = '/api/v4/home'
        self.headers = {
            # "authorization": token, "Content-Type": "application/json"
            "Content-Type": "application/json"
        }
        if version:
            self.headers["User-Agent"] = version
        if token:
            self.headers["authorization"] = token
        if xApp:
            self.headers['x-app-params'] = xApp

    def api_get_v4_home(self, bid, subject=None, level=None, selectWeekOperation=None):
        """
         v4/home 首页
        :param bid:宝宝id
        :param subject:科目
        :param level:级别
        :param selectWeekOperation：选择周
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
            "bid": bid,
        }
        if subject:
            body["subject"] = subject
        if level:
            body["level"] = level
        if selectWeekOperation:
            body['selectWeekOperation'] = selectWeekOperation
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_globe(self, anch, anver, bid):
        """
         全局用户信息
        :param anch:版本
        :param anver:app版本
        :param bid:宝贝id
        :return:
        """
        api_url = f"{self.host}/api/globe"
        body = {
            "android_ch": anch,
            "android_ver": anver,
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_ownsgu(self):
        """查看拥有课程"""
        api_url = f"{self.host}/api/report/ownsgu"
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="json")
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("12345678001")
    token = user.basic_auth
    version = config["version"]['ver11.0']

    # 进入v4首页
    home = ApiHome(token)
    resp = home.api_get_v4_home("467f0668aeec404382e504cd5731e994")
    print(resp)
