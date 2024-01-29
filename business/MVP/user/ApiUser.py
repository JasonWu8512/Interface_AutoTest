# coding=utf-8
# @Time    : 2022/9/20 3:32 下午
# @Author  : Karen
# @File    : ApiUser.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiUser(object):
    ''' 用户信息 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_user_info(self):
        """ 01）获取用户信息 """
        api_url = "/api/user"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_corrections_times(self):
        """ 02）查询用户剩余的纠音次数 """
        api_url = "/api/user/corrections"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_correct_record(self,bid):
        """ 03）进行纠音 """
        api_url = "/api/user/corrections"
        body = {"bid": bid}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="json", method="post",
                                headers=self.headers)
        return resp


    def api_record_setting(self):
        """ 04）录音评分设置 """
        api_url = "/api/user/settings"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp