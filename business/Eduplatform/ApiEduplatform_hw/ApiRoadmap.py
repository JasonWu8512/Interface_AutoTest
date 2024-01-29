'''
@Author : degg_wang
@Date : 2022/9/1
@File : ApiRoadmap
'''


# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiRoadmap(object):
    """
    组合路线图元数据与状态信息
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    #获取路线图的元数据
    def api_getSimpleLevelInfo(self, bid,levelId,localeLang,uid):
        """
        获取路线图的元数据
        :param bid:   孩子id
        :param levelId:   级别id
        :param localeLang: 多语言配置
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/roadmap/getSimpleLevelInfo"
        body = {
            "bid": bid,
            "levelId": levelId,
            "localeLang":  localeLang,
            "uid":  uid
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

    # 获取level及单元元数据
    def api_getLevelMetaInfoV2(self, bid, levelId, localeLang, uid):
        """
        获取level及单元元数据
        :param bid:   孩子id
        :param levelId:   级别id
        :param localeLang: 多语言配置
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/roadmap/getLevelMetaInfoV2"
        body = {
            "bid": bid,
            "levelId": levelId,
            "localeLang": localeLang,
            "uid": uid
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

    # 获取lesson和sublesson元数据
    def api_getLessonMetaInfoV2(self, bid, nodeId, localeLang, uid):
        """
        获取lesson和sublesson元数据
        :param bid:   孩子id
        :param nodeId:   nodeId
        :param localeLang: 多语言配置
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/roadmap/getLessonMetaInfoV2"
        body = {
            "bid": bid,
            "nodeId": nodeId,
            "localeLang": localeLang,
            "uid": uid
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

