# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 1:19 下午
@Author  : Demon
@File    : ApiDataCenterNotificationRecord.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header

class ApiDatacenterNotification(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_basic/datacenter_notification_record'

    def api_notification_record_add(self, notification_id, user, typ="datacenter"):
        """
        通知记录添加
        :param notificationId : 通知id
        :param user :用户名
        :param typ :查询类型 {datacenter}
        :return :
        """
        api_url = self.host + f"{self.root}/notification_record_add"
        body = {
            "notificationId": notification_id,
            "user": user,
            "type": typ
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_notification_record_select(self, notification_id, user, typ="datacenter"):
        """
        查询通知记录
        :param notificationId : 通知id
        :param user :用户名
        :param typ :查询类型 {datacenter}
        :return :
        """
        api_url = self.host + f"{self.root}/notification_record_select"
        body = {
            "notificationId": notification_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)