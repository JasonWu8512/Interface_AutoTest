'''
@Author : degg_wang
@Date : 2022/9/1
@File : ApiService
'''

# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiService(object):
    """
    海外用户课程拥有数据维护
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    #购买服务
    def api_create(self, appId ,startTime,endTime,uid):
        """
        购买服务
        :param appId:   appId
        :param startTime:   服务开始时间
        :param endTime: 服务结束时间
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/course/service/possess/create"
        body = {
            "appId": appId,
            "startTime": startTime,
            "endTime":  endTime,
            "uid":  uid
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

    #停止服务
    def api_remove(self, uid,appId):
        """
        停止服务
        :param uid: 用户id
        :param appId:   appId
        :return:
        """
        api_url = "/inner/course/service/possess/remove"
        body = {
            "uid": uid,
            "appId": appId
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

    # 更新服务
    def api_update(self, appId, uid,startTime,endTime):
        """
        更新服务
        :param appId:   appId
        :param uid: 用户id
        :param startTime:   服务开始时间
        :param endTime: 服务结束时间
        :return:
        """
        api_url = "/inner/course/service/possess/update"
        body = {
            "appId": appId,
            "uid": uid,
            "startTime": startTime,
            "endTime": endTime
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp

    # 获取用户购课服务时间
    def api_getPossessPeriod(self, appId, uid):
        """
        获取用户购课服务时间
        :param appId:   appId
        :param uid: 用户id
        :return:
        """
        api_url = "/inner/course/service/possess/getPossessPeriod"
        body = {
            "appId": appId,
            "uid": uid
        }
        resp = send_api_request(url= api_url, paramType="json", paramData=body, method="post")
        return resp