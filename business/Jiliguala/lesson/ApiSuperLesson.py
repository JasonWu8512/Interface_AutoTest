# -*- coding: utf-8 -*-
# @Time : 2021/5/27 8:22 下午
# @Author : Cassie
# @File : ApiSuperLesson.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSuperLesson():
    """
    lessonbiz  C端：老呱美1.5学习模式切换相关接口
    SuperLessonController
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/super/lesson/mode'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_switch(self, bid, lv):
        """
        切换学习模式的展示信息
        :param bid:宝贝id
        :param lv:当前课程级别
        :return:
        """
        api_url = f"{self.host}{self.root}/switch/meta"
        body = {
            "bid": bid,
            "nonce": "f8d9dda0-eace-4bb8-be33-f03d3fbd28cf",
            "lv": lv
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_switch_mode(self, mode, bid, lv):
        """
        操作切换学习模式
        :param mode:学习模式(freedom/planning)
        :param bid:宝贝id
        :param lv:当前课程级别
        :return:
        """
        api_url = f"{self.host}{self.root}/switch"
        body = {
            "mode": mode,
            "lv": lv,
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_init_mode(self, mode, bid, lv):
        """
        初始化学习模式
        :param mode:学习模式(freedom/planning)
        :param bid:宝贝id
        :param lv:当前课程级别
        :return:
        """
        api_url = f"{self.host}{self.root}/init"
        body = {
            "mode": mode,
            "lv": lv,
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19000000020")
    token = user.basic_auth
    version = config['version']['ver11.6']
    super_lesson = ApiSuperLesson(token, version)
    # resp = super.api_get_coupon("A", "L1XX")
    #resp = super.api_get_lesson("L1XX", "B", "B")
    # resp = super_lesson.api_get_switch("0e5c5f66135641e881a9000fe60d2622", "L1XX")
    # resp = super_lesson.api_switch_mode("planning", "0e5c5f66135641e881a9000fe60d2622", "L1XX")
    resp = super_lesson.api_init_mode("planning", "0e5c5f66135641e881a9000fe60d2622", "L1XX")
    print(resp)
