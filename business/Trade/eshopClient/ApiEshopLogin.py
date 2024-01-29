# coding=utf-8
# @Time    : 2020/12/3 9:59 上午
# @Author  : jerry
# @File    : ApiEshopLogin.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiEshoLogin:
    """
    eshop
    LoginController
    """

    def __init__(self, wechat_token):
        self.host = Domains.domain
        self.root = '/api/eshop/login'
        self.headers = {"wechattoken": wechat_token, "Content-Type": "application/json"}

    """-------------------------------------------login相关LoginController--------------------------------"""

    def api_eshop_login_wechat(self, wechatToken):
        """
        eshop登陆接口
        """
        api_url = f'{self.host}{self.root}/wechat'
        body = {
            "wechatToken": wechatToken
        }
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp