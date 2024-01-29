# coding=utf-8
# @Time    : 2022/9/5 11:32 上午
# @Author  : Karen
# @File    : ApiGpen.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiGpen(object):

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_goldentouch_gpen_token(self):
        """ 01）进入点读笔首页 获取点读笔信息 """
        api_url = "/api/gpen/token"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get", headers=self.headers)
        return resp
