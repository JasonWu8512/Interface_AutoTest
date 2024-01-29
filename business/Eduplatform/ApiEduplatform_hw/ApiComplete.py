'''
@Author : degg_wang
@Date : 2022/8/31
@File : ApiComplete
'''


# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiComplete(object):
    """
    知识点分数上报
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    #cocos编辑器课程知识点分数上报
    def api_cocosComplete(self, bid,score,lessonId,sublessonId,gameId,sectionId,sectionType,finishTime,special,detail,roundDetail,sentenceDetail):
        """
        cocos编辑器课程知识点分数上报
        :param bid:   孩子id
        :param score:   分数
        :param lessonId: 课程id
        :param sublessonId: 子课程id
        :param gameId: gameId
        :param sectionId: sectionId
        :param sectionType: sectionType
        :param finishTime: 完成时间
        :param special: 是否为非固定知识点（true-非固定知识点，false-固定知识点）
        :param detail: detail
        :param roundDetail: roundDetail
        :param sentenceDetail: sentenceDetail
        :return:
        """
        api_url = "/inner/course/ge/section/complete"
        body = {
              "bid": bid,
              "score": score,
              "lessonId": lessonId,
              "sublessonId": sublessonId,
              "gameId": gameId,
              "sectionId": sectionId,
              "sectionType": sectionType,
              "finishTime": finishTime,
              "special": special,
              "detail": detail,
              "roundDetail": roundDetail,
              "sentenceDetail": sentenceDetail
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

    # web编辑器课程知识点分数上报
    def api_webComplete(self, bid, score, lessonId, sublessonId, gameId, sectionId,  finishTime, details):
        """
        web编辑器课程知识点分数上报
        :param bid:   孩子id
        :param score:   分数
        :param lessonId: 课程id
        :param sublessonId: 子课程id
        :param gameId: gameId
        :param sectionId: sectionId
        :param finishTime: 完成时间
        :param details: details
        :return:
        """
        api_url = "/inner/course/web/section/complete"
        body = {
            "bid": bid,
            "score": score,
            "gameId": gameId,
            "sectionId": sectionId,
            "sublessonId": sublessonId,
            "lessonId": lessonId,
            "finishTime": finishTime,
            "details": details
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp