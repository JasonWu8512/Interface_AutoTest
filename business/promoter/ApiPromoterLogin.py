# coding=utf-8
# @Time    : 2020/12/3 10:37 上午
# @Author  : jerry
# @File    : ApiPromoterLogin.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPromoterLogin:
    """
    promoter
    LoginController
    """

    root = "/api/promoter"

    def __init__(self, wechat_token=None, basic_auth=None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    """-------------------------------------LoginController--------------------------------"""

    def api_promoter_login(self, mobile):
        """
        推广人注册登陆
        """
        headers = self.headers
        headers["X-CustomHeader"] = '{"mobile":' + mobile + ',"sign":""}'
        api_url = f'{self.host}{self.root}/login'
        body = {}
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=headers)
        return resp

    def api_check_bind(self):
        """
        获取绑定状态接口
        """
        api_url = f'{self.host}{self.root}/login/check/bind'
        resp = send_api_request(url=api_url, method='post', headers=self.headers)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    dm.set_domain("https://fat.jiliguala.com")
    promo = UserProperty('15502180495')
    #wechattoken = promo.encryptWechatToken_promoter
    basic = promo.basic_auth
    promoter = ApiPromoterLogin(basic_auth=basic)
    res = promoter.api_promoter_login('15502180495')
    print(res)
    # re = promoter.api_check_bind()
    # print(re)