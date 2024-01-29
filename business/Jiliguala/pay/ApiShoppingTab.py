# -*- coding: utf-8 -*-
# @Time : 2021/7/13 3:26 下午
# @Author : Cassie
# @File : ApiShoppingTab.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiShoppingTab():
    """
    11.5及以上版本购买页相关接口
    ShoppingTabController
    """

    def __init__(self, token, version, agent):
        self.host = Domains.config.get('url')
        self.root = '/api/pay/shopping'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version,
            "User-Agent": agent
        }

    def api_get_shopping_tab(self, bid):
        """
        竖版app购买tab页查询
        :param bid：宝贝id
        :return:
        """
        api_url = f"{self.host}{self.root}/tab"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_shopping_video(self):
        """
        :return:
        """
        api_url = f"{self.host}{self.root}/video"
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params")
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19000000020")
    token = user.basic_auth
    version = config['version']['ver11.6']
    agent = config['agent']['ios_11.6']
    # tab = ApiShoppingTab(token, version, agent)
    tab = ApiShoppingTab(token, version, agent)
    # resp = tab.api_get_shopping_tab("0e5c5f66135641e881a9000fe60d2622")
    resp1 = tab.api_get_shopping_video()

    print(resp1)
