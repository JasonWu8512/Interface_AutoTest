'''
@Author : degg_wang
@Date : 2022/9/1
@File : ApiFlexible
'''


# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiFlexible(object):
    """
    组合路线图元数据与状态信息
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    #获取叶节点，叶节点父节点的元数据 + 节点的完课/解锁/拥有 信息
    def api_getBabyLessonNodesInfo(self, bid,nodeId,localeLang,uid):
        """
        获取叶节点，叶节点父节点的元数据 + 节点的完课/解锁/拥有 信息
        :param bid:   孩子id
        :param nodeId:   nodeId
        :param localeLang: 多语言配置
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/flexible/roadmap/pipeline/getBabyLessonNodesInfo"
        body = {
            "bid": bid,
            "nodeId": nodeId,
            "localeLang":  localeLang,
            "uid":  uid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    # 获取level+根节点下两层的节点元数据 + 节点的完课/解锁/拥有 信息
    def api_getBabyLevelNodesInfo(self, bid, levelId, localeLang, uid):
        """
        获取level+根节点下两层的节点元数据 + 节点的完课/解锁/拥有 信息
        :param bid:   孩子id
        :param levelId:   级别id
        :param localeLang: 多语言配置
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/flexible/roadmap/pipeline/getBabyLevelNodesInfo"
        body = {
            "bid": bid,
            "levelId": levelId,
            "localeLang": localeLang,
            "uid": uid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    # 获取level列表，包含了是否解锁，是否是当前级别，学习进度
    def api_getUserPossessLevelInfoV2(self, bid, curriculumId, uid):
        """
        获取level列表，包含了是否解锁，是否是当前级别，学习进度
        :param bid:   孩子id
        :param curriculumId:   课程Id
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/flexible/roadmap/pipeline/getUserPossessLevelInfoV2"
        body = {
            "bid": bid,
            "curriculumId": curriculumId,
            "uid": uid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp