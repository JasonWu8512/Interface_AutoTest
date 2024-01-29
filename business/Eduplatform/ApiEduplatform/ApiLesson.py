# coding=utf-8
# @Time    : 2021/6/8 下午6:11
# @Author  : Sariel
# @File    : ApiLesson

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
# from prettyprinter import cpprint


class ApiLesson(object):
    def __init__(self):
        # 请求头文件
        self.host = Domains.domain
        self.root = '/api/v1/lesson'

    def api_get_baby_lesson_info_list_v2(self, levelId, paidCurrent99, uid, bid):
        """
        根据levelId返回level下lesson的是否完课信息
        若bid一节lesson都未完成，不返回数据

        :param levelId: 路线图id
        :param paidCurrent99:   是否包含9块9 1-是 0-不是
        :param uid: 用户id,用于区分是否是AB实验/老9块9用户
        :param bid: baby id
        :return:
        """
        api_url = f"{self.root}/getBabyLessonInfoListV2"
        body = {
            "levelId": levelId,
            "paidCurrent99": paidCurrent99,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_baby_lesson_info_list_v3(self, levelId, paidCurrent99, uid, bid, lessonIds=[]):
        """
        根据levelId和lesson数组返回level下lesson的是否完课信息

        :param levelId: 路线图id
        :param paidCurrent99:   是否包含9块9 1-是 0-不是
        :param uid: 用户id,用于区分是否是AB实验/老9块9用户
        :param bid: baby id
        :param lessonIds:   课程ID（数组）
        :return:
        """
        api_url = f"{self.root}/getBabyLessonInfoListV3"
        body = {
            "levelId": levelId,
            "paidCurrent99": paidCurrent99,
            "uid": uid,
            "bid": bid,
            "lessonIds": lessonIds
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_baby_lesson_info(self, bid, lessonId):
        """
        获取该bid该lesson的完课情况

        :param bid: baby id
        :param lessonId: lessonId 课程id
        :return:
        """
        api_url = f"/api/v1/lesson/getBabyLessonInfo/{bid}/{lessonId}"
        resp = send_api_request(url=api_url, paramType="json", method="post")
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['eduplatform_url'])
    lesson = ApiLesson()
    # cpprint(lesson.api_get_baby_lesson_info_list_v2(levelId="K1GE", paidCurrent99="true", uid="abtestsuibianxie",
    #                                                     bid="e9f18597eae14a3a9aa3e58ec1967793"))
    # cpprint(lesson.api_get_baby_lesson_info_list_v3(levelId="K1GE", paidCurrent99="true", uid="abtestsuibianxie",
    #                                                     bid="e9f18597eae14a3a9aa3e58ec1967793",
    #                                                     lessonIds=["K1GEF002", "K1GEF003"]))
    # cpprint(lesson.api_get_baby_lesson_info(bid="e9f18597eae14a3a9aa3e58ec1967793", lessonId="K1GEF002"))
