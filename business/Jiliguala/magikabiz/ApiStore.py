# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/7/21 1:16 下午
@Author   : Anna
@File     : ApiStore.py
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiStore():
    """
    魔石商城
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/magika'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_home(self):
        """
        魔石商城头部用户魔石信息
        """
        api_url = f"{self.host}{self.root}/home"
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp

    def api_get_item(self):
        """
        魔石商城商品列表
        """
        api_url = f"{self.host}{self.root}/item"
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp

    def api_get_detail(self, commodityno):
        """
        魔石商城商品详情
        :param commodityno:商品id
        :return：
        """
        api_url = f"{self.host}{self.root}/item/detail"
        body = {
            "commodityNo": commodityno
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19393123455")
    token = user.basic_auth
    version = config['version']['ver11.6']
    stone = ApiStore(token, version)
    # 调用魔石商城头部接口
    resp = stone.api_get_home()
    print(resp)

    # 调用商品列表接口
    resp01 = stone.api_get_item()
    print(resp01)

    # 调用商品详情接口
    resp02 = stone.api_get_detail("MG_goods_012_SPU")
    print(resp02)
