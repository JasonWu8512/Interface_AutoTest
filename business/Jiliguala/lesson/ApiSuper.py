# -*- coding: utf-8 -*-
# @Time : 2021/5/27 7:42 下午
# @Author : Cassie
# @File : ApiSuper.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSuper():
    """
    lessonbiz  C端：老呱美1.5课程相关接口
    SuperController
    """

    def __init__(self, token, version=None):
        self.host = Domains.config.get('url')
        self.root = '/api/super'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }
        if version:
            self.headers['X-APP-Version'] = version

    def api_get_coupon(self, id, type):
        """
        查询呱美课优惠券列表
        :param id:960版本需求点4.3吆喝实验标识位(A/B)
        :param type:请求购买页面时的type(L1XX-L6XX)
        :return:
        """
        api_url = f"{self.host}{self.root}/lesson/buy/coupon/list"
        body = {
            "TestPlan_PurchaseGainCoupon": id,
            "nonce": "f8d9dda0-eace-4bb8-be33-f03d3fbd28cf",
            "type": type
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_lesson(self, type, ab, modules):
        """
        查询呱美课购买页信息
        :param type:请求购买页面时的type(L1XX-L6XX)
        :param ab:实验标识位
        :return:
        """
        api_url = f"{self.host}{self.root}/lesson/buy"
        body = {
            "type": type,
            "ab": ab,
            "ab_modules": modules,
            "nonce": "f8d9dda0-eace-4bb8-be33-f03d3fbd28cf"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_lesson_progress(self, bid, lessonid, sublessonid, units):
        """
        老呱美1.5的sublesson完课
        :param bid:宝贝id
        :param lessonid:课程id
        :param sublessonid:子课id
        :param units:section对应的id和得分
        :return:
        """
        api_url = f"{self.host}{self.root}/lessonprogress"
        body = {
            "bid": bid,
            "lessonid": lessonid,
            "sublessonid": sublessonid,
            "units": units
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_get_pay_detail(self, itemid, coupon=None):
        """
        获取商品价格
        :param itemid：商品sku id
        :param couponTypActivity:使用的优惠券
        :return:
        """
        api_url = f"{self.host}{self.root}/paydetail"
        body = {
            "itemid": itemid,
            "couponTypActivity": coupon,
            "nonce": "5d6739c0-dce1-492e-adfc-c853adfe21f4"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_lesson_detail(self, bid, lesson_click, popup, lid):
        """
        查询课程详情页
        :param bid:宝贝id
        :param lesson_click:
        :param popup:是否需要弹窗
        :param lid:lesson id
        """
        api_url = f"{self.host}{self.root}/v2/lessondetail"
        body = {
            "bid": bid,
            "lesson_click": lesson_click,
            "nonce": "5d6739c0-dce1-492e-adfc-c853adfe21f4",
            "popup": popup,
            "lid": lid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("15958112857")
    token = user.basic_auth
    version = config['version']['ver11.6']
    super = ApiSuper(token, version)
    # resp = super.api_get_coupon("A", "L1XX")
    # resp = super.api_get_lesson("L1XX", "B", "B")
    resp = super.api_lesson_progress("2311b54d0566404ebe5140318aef86c0", "L1XXP01", "L1XXP01sub01", [])
    # resp = super.api_get_pay_detail("K1GE")
    print(resp)
