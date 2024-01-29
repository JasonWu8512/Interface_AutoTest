# coding=utf-8
# @Time    : 2021/5/28 下午3:48
# @Author  : Sariel
# @File    : ApiLessonBuy

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains


class ApiLessonBuy(object):
    def __init__(self):
        # 请求头文件
        self.host = Domains.domain
        self.root = '/api/v1/lessonBuy'

    def api_get_user_lesson_buy_info(self, uid):
        """
        根据用户id获取购买的级别信息
        :param uid: 用户id
        :return:
        """
        api_url = f"{self.root}/getUserLessonBuyInfo/{uid}"
        resp = send_api_request(url=api_url, paramType="json", method="post")
        return resp

    def api_create(self, uid, source, levelList=[]):
        """
        用户购课
        :param uid: 用户id
        :param source:  来源
        :param levelList:   级别（数组）
        :return:
        """
        api_url = f"{self.root}/create"
        body = {
            "uid": uid,
            "source": source,
            "levelList": levelList
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_remove(self, uid, source, levelList=[]):
        """
        用户退课
        :param uid: 用户id
        :param source:  来源
        :param levelList:   级别（数组）
        :return:
        """
        api_url = f"{self.root}/remove"
        body = {
            "uid": uid,
            "source": source,
            "levelList": levelList
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['eduplatform_url'])
    lesson_buy = ApiLessonBuy()
    # print(lesson_buy.api_get_user_lesson_buy_info("1f54a187f6384deea960f000a47897ce"))
    # print(lesson_buy.api_create(uid="test060801", source="tiga_test", levelList=["K1GE", "K2GE"]))
    # print(lesson_buy.api_remove(uid="test060801", source="tiga_test", levelList=["K1GE", "K2GE"]))
