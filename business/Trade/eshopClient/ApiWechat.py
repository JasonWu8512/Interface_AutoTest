# -*- coding: utf-8 -*-
# @Time    : 2020/10/10 5:57 下午
# @Author  : zoey
# @File    : ApiWechat.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiWechat:

    def __init__(self, basic_token, wechat_token):
        self.headers = {'Authorization': basic_token, "wechattoken": wechat_token, "Content-Type": "application/json"}
        self.host = Domains.domain
        self.root = "/api/eshop/wechat"
        self.wechat_token = wechat_token

    def api_get_wechat_info(self):
        api_url = f'{self.host}{self.root}/info'
        body = {'wechatToken': self.wechat_token}
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp
