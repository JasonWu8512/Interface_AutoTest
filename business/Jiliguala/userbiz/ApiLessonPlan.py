# -*- coding: utf-8 -*-
# @Time : 2021/6/3 13:30 下午
# @Author : nana
# @File : ApiLessonPlan.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiLessonPlan():
    """
    /api/user/lesson/plan    1.0学习计划页
    /api/user/lesson/plan/v2  2.0学习计划页
    /api/user/lesson/plan/v3  3.0学习计划页
    """
    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root1 = '/api/user/lesson/plan'
        self.root2 = '/api/user/lesson/plan/v2'
        self.root3 = '/api/user/lesson/plan/v3'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_lessonplan(self, bid, lv):
        """
        1.0学习计划页
        :param bid:宝贝
        :param lv:当前要查看的级别
        :return:
        """
        api_url = f"{self.host}{self.root1}"
        body = {
            "bid": bid,
            "lv": lv
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_lessonplan_v2(self, bid, lv):
        """
        2.0学习计划页
        :param bid:宝贝
        :param lv:当前要查看的级别
        :return:
        """
        api_url = f"{self.host}{self.root2}"
        body = {
            "bid": bid,
            "lv": lv
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_lessonplan_v3(self, bid, lv):
        """
        3.0学习计划页
        :param bid:宝贝
        :param lv:当前要查看的级别
        :return:
        """
        api_url = f"{self.host}{self.root3}"
        body = {
            "bid": bid,
            "lv": lv
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("13242040693")
    token = user.basic_auth
    version = config['version']['ver11.6']
    lessonplan = ApiLessonPlan(token, version)

    # /api/user/lesson/plan
    resp = lessonplan.api_get_lessonplan('b1d4ffd0b19b4dd9b8e5aeb29c13ac0d', 'L1XX')
    print(resp)

    # /api/user/lesson/plan/v2
    resp = lessonplan.api_get_lessonplan_v2('b1d4ffd0b19b4dd9b8e5aeb29c13ac0d', 'L1XX')
    print(resp)

    # /api/user/lesson/plan/v3
    resp = lessonplan.api_get_lessonplan_v3('b1d4ffd0b19b4dd9b8e5aeb29c13ac0d', 'T2GE')
    print(resp)
