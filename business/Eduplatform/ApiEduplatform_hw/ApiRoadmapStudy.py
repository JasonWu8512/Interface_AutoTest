'''
@Author : degg_wang
@Date : 2022/9/1
@File : ApiRoadmapStudy
'''
# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiRoadmapStudy(object):
    """
    灵活路线图完课
    """

    def __init__(self, token=None):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    # 叶节点完课
    def api_leafNodeComplete(self, bid, uid, finishTime, nodeId, score):
        """
        叶节点完课
        :param bid: 孩子id
        :param finishTime:  完成时间
        :param nodeId: nodeId
        :param score:  分数
        :return:
        """
        api_url = "/inner/roadmap/study/leafNodeComplete"
        body = {
            "bid": bid,
            "uid": uid,
            "finishTime": finishTime,
            "nodeId": nodeId,
            "score": score
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

    # 用户当前所在级别
    def api_setUserCurrentLevel(self, uid,bid,levelId):
        """
        用户当前所在级别
        :param uid: 用户id
        :param bid: 孩子id
        :param levelId: 级别id
        :return:
        """
        api_url = "/inner/roadmap/study/setUserCurrentLevel"
        body = {
            "uid": uid,
            "bid": bid,
            "levelId": levelId
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    #跳过课程
    def api_skipLesson(self, uid,bid,nodeId):
        """
        用户当前所在级别
        :param uid: 用户id
        :param bid: 孩子id
        :param nodeId: nodeId
        :return:
        """
        api_url = "/inner/roadmap/study/skipLesson"
        body = {
            "uid": uid,
            "bid": bid,
            "nodeId": nodeId
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp
