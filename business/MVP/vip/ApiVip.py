# coding=utf-8
# @Time    : 2022/9/20 3:24 下午
# @Author  : Karen
# @File    : ApiVip.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiVip(object):
    ''' 获取VIP状态 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_get_vip(self):
        """ 01）获取vip状态 """
        api_url = "/api/vip"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp

