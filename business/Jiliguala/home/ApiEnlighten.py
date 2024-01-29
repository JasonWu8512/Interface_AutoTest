# -*- coding: utf-8 -*-
# @Time : 2021/5/23 9:21 下午
# @Author : Cassie
# @File : ApiEnlighten.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiEnlighten():
    """
    客户端获取课外资源集合（每日五分钟、资源位、热门专辑等）
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/enlightenworld'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_enlighten(self, bid):
        """
        获取课外资源集合（每日五分钟、资源位、热门专辑等）
        :param bid:宝贝id
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
            "bid": bid,
            "nonce": "44894767-d2c8-423a-8259-2184bc5a634e"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("15958112857")
    token = user.basic_auth
    version = config['version']['ver16.0']
    enlighten = ApiEnlighten(token, version)
    # resp = pop.api_get_pop("22ee5af5a227487d8979d73fa34faea3", "K1MA", "math")
    # resp=pop.api_tab_get("3aec6bbdc84048f8b9e68580390a300c","buyTab","popup")
    resp = enlighten.api_get_enlighten("0984f6359cd140bc887b73b0c44f28f1")
    print(resp)
