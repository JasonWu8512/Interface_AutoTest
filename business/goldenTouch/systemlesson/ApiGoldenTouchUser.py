# coding=utf-8
# @Time    : 2022/7/15 6:33 下午
# @Author  : Karen
# @File    : ApiGoldenTouchUser.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiGoldenTouchUser(object):

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_goldentouch_user_login(self):
        """ 01）账号登录 """
        api_url = "/api/goldentouch/user/login"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json',method="post", headers=self.headers)
        return resp


    def api_goldentouch_user_bind(self):
        """ 02）账号绑定 """
        api_url = "/api/goldentouch/user/bind"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json',method="post", headers=self.headers)
        return resp


    def api_goldentouch_user_myAssistant(self):
        """ 03）添加启蒙顾问 """
        api_url = "/api/goldentouch/user/myAssistant"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="params", method="get",
                                headers=self.headers)
        return resp


    def api_goldentouch_user_awardStatus(self):
        """ 04）获取用户奖励信息 """
        api_url = "/api/goldentouch/user/awardStatus"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json',method="post", headers=self.headers)
        return resp


    def api_goldentouch_possessed(self):
        """ 05）是否拥有课程，前端用来判断是让他购买还是进路线图 """
        api_url = "/api/goldentouch/possessed"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='params', method="get",
                                headers=self.headers)
        return resp
