# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 1:17 下午
@Author  : Demon
@File    : ApiDataCenterNotification.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header

class ApiDataCenterNotification(object):
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
        self.root = '/api_basic/datacenter_notification'

    def api_notification_select(self, user, typ="datacenter"):
        """
        查询公告信息
        :param user :用户名
        :param typ :查询类型 {datacenter}
        :return :
        """
        api_url = self.host + f"{self.root}/notification_select"
        body = {
            "user": user,
            "type": typ
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_notification_del(self, article_id, typ="datacenter"):
        """
        删除公告信息
        :param article_id :公告id
        :param typ :查询类型 {datacenter}
        :return :
        """
        api_url = self.host + f"{self.root}/notification_del"
        body = {
            "id": article_id,
            "type": typ
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_notification_add(self, user, content, title, typ="datacenter"):
        """
        增加公告描述信息
        :param user: 用户名
        :param typ: 公告通知类型
        :param content: 公告通知内容正文
        :param title: 公告通知标题
        :return:
        """
        api_url = self.host + f"{self.root}/notification_add"

        body = {
            "user": user,
            "type": typ,
            "content": content,
            "title": title
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_notification_update(self, article_id, user, content, title, typ="datacenter"):
        """
        编辑公告描述信息
        :param article_id: 用户名
        :param user: 用户名
        :param typ: 公告通知类型
        :param content: 公告通知内容正文
        :param title: 公告通知标题
        :return:
        """
        api_url = self.host + f"{self.root}/notification_update"

        body = {
            "id": article_id,
            "user": user,
            "type": typ,
            "content": content,
            "title": title
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)



