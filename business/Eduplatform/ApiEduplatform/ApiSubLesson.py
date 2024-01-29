# coding=utf-8
# @Time    : 2021/6/8 下午7:51
# @Author  : Sariel
# @File    : ApiSubLesson

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
# from prettyprinter import cpprint


class ApiSubLesson(object):
    def __init__(self):
        # 请求头文件
        self.host = Domains.domain
        self.root = '/api/v1/subLesson'

    def api_get_baby_sublesson_info(self, bid, lessonId, sublessonId, gameId):
        """
        获取该bid该sublesson的完课情况

        :param bid:         baby id
        :param lessonId:    课程id
        :param sublessonId: 子课程id
        :param gameId:      子课程资源id
        :return:
        """
        api_url = f"{self.root}/getBabySublessonInfo"
        body = {
            "bid": bid,
            "lessonId": lessonId,
            "sublessonId": sublessonId,
            "gameId": gameId
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_batch_get_sublesson_info_v2(self, lessonId, uid, bid):
        """
        获取该bid，该lessonId中sublesson的学习情况，按照sublesson顺序排序，并判断解锁状态

        :param lessonId:    课程id
        :param uid:         用户id,用于区分是否是AB实验/老9块9用户
        :param bid:         baby id
        :return:
        """
        api_url = f"{self.root}/batchGetSublessonInfoV2"
        body = {
            "lessonId": lessonId,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_sublesson_complete_v2(self, lessonId, uid, bid, sublessonId, gameId, score, combNum, finishTime):
        """
        英语分数上报

        :param lessonId:    课程id
        :param uid:         用户id,用于区分是否是AB实验/老9块9用户
        :param bid:         baby id
        :param sublessonId:         子课程id
        :param gameId:         gameId
        :param score:         分数
        :param combNum:         combNum
        :param finishTime:         完成时间
        :return:
        """
        api_url = f"{self.root}/sublessonCompleteV2"
        body = {
            "lessonId": lessonId,
            "uid": uid,
            "bid": bid,
            "sublessonId": sublessonId,
            "gameId": gameId,
            "score": score,
            "combNum": combNum,
            "finishTime": finishTime
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['eduplatform_url'])
    sublesson = ApiSubLesson()
    # cpprint(sublesson.api_get_baby_sublesson_info(bid="e9f18597eae14a3a9aa3e58ec1967793", lessonId="K1GEF002",
    #                                               sublessonId="K1GEF00201", gameId="L1U01W1D2Q1"))
    # cpprint(sublesson.api_batch_get_sublesson_info_v2(lessonId="K1GEF002", uid="abtestsuibianxie",
    #                                                   bid="e9f18597eae14a3a9aa3e58ec1967793", ))
