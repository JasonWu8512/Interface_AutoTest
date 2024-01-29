# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/6/1 3:39 下午
@Author   : Anna
@File     : ApiCoupon.py
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty
from business.Reading.user.ApiUser import ApiUser


class ApiCoupon():
    def __init__(self, token, version=None):
        self.host = Domains.config.get('url')
        self.root = '/api/coupon'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_couponList(self, status, page, bid):
        """
        老版本家长中心-优惠券列表接口
        :param status:优惠券类型
        :param page:第x页
        :param bid:宝宝id
        :return:
        """
        api_url = f"{self.host}{self.root}/list"
        body = {
            "status": status,
            "page": page,
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_coupon(self, status, page, bid):
        """
        新版本获取优惠券列表
        :param status:优惠券类型
        :param page:第x页
        :param bid:宝贝
        :return:
        """
        api_url = f"{self.host}{self.root}/list/v2"
        body = {
            "status": status,
            "page": page,
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    # class ApiCoupon(object):
    #     """
    #     优惠券
    #     """
    #
    #     def __init__(self, token):
    #         self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
    #         self.host = Domains.domain

    def api_coupon_purchase(self, itemid):
        """
        5折专区专辑购买页
        """
        api_url = "/api/coupon/purchase"
        body = {"itemid": itemid}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19393123455")
    token = user.basic_auth
    version = config["version"]['ver11.0']

    # 测试老版本获取优惠券接口
    couponlist = ApiCoupon(token, version)
    resp = couponlist.api_get_couponList("available", "0", "bd337e56e9964003b5f23d48e095ffc0")
    print(resp)

    # 测试新版本获取优惠券接口
    couponListV2 = ApiCoupon(token, version)
    resp01 = couponListV2.api_get_coupon("available", "0", "bd337e56e9964003b5f23d48e095ffc0")
    print(resp01)
    mobile = '14021736021'
    user = UserProperty(mobile)
    token = user.basic_auth
    coupon = ApiCoupon(token=token)
    item_id = 'BundleCDS001'
    res = coupon.api_coupon_purchase(item_id)
    print(res)
