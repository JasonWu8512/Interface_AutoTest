'''
@Author : degg_wang
@Date : 2022/8/31
@File : StudyReport
'''
# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiStudyReport(object):
    """
    用户的学习报告数据
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    # 获取该lesson的孩子学习报告
    def api_get_baby_study_report(self, bid, lessonId, uid):
        """
        获取该lesson的孩子学习报告
        :param bid:孩子id
        :param lessonId:课程id
        :param uid:用户id
        :return:
        """
        api_url = "/inner/course/study/report/geBabyStudyReportV3"
        body = {
            "bid": bid,
            "lessonId": lessonId,
            "uid": uid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    # 获取该lesson的孩子课后激励报告
    def api_get_baby_Inspire_report(self, bid,nodeId):
        """
        获取该lesson的孩子学习报告
        :param bid:孩子id
        :param nodeId:节点id
        :return:
        """
        api_url = "/inner/course/study/report/getBabyInspireReportV2"
        body = {
            "bid": bid,
            "nodeId": nodeId
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp