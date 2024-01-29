# coding=utf-8
# @Time    : 2021/3/24 11:41 上午
# @Author  : jerry
# @File    : ApiHomeSpu.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiHome:
    """HomeController"""
    root = "/api/promoter"

    def __init__(self, wechat_token=None, basic_auth = None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    def api_promoter_home(self):
        """
        获取推广人首页信息
        """
        api_url = f'{self.host}{self.root}/home'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_income_detail(self):
        """
        推荐人收入明细
        """
        api_url = f'{self.host}{self.root}/income/detail'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_income_overview(self):
        """
        推荐人账户概览
        """
        api_url = f'{self.host}{self.root}/income/overview'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    promo = UserProperty("13951782841")
    wechattoken = promo.encryptWechatToken_promoter
    basic = promo.basic_auth
    promoter = ApiHome(wechattoken, basic)
    res = promoter.api_income_overview()
    print(res)