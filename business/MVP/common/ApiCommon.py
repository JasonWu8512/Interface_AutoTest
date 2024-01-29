# coding=utf-8
# @Time    : 2022/9/20 3:29 下午
# @Author  : Karen
# @File    : ApiCommon.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiCommon(object):
    ''' 图书馆首页专辑tab '''

    def __init__(self, token,ggheader):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8', "GGHeader-V2": ggheader}
        self.host = Domains.domain


    def api_library(self):
        """ 01）图书馆首页专辑tab """
        api_url = "/api/hot"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp