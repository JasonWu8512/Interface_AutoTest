# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 12:04 下午
@Author  : Demon
@File    : ApiFunnel.py
"""



from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiFunnel(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            # Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_funnel/funnel'

    def api_funnel_fetch_funnel_status(self, report_id):
        """
        获取漏斗分析的状态 0正常1计算中2异常
        :param :report_id : 产品ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchFunnelStatus")
        body = {
            "report_id": report_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_funnel_delete(self, report_id):
        """
        删除漏斗分析
        :param :report_id : 产品ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/delete")
        body = {
            "report_id": report_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_funnel_add(self, report_id):
        """
        新建/保存漏斗分析
        :param :
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/add")
        body = {
            "report_id": report_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_funnel_fetch_last_preview(self):
        """
        上一次漏斗分析内容
        :param :event_id : 漏斗事件ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchLastPreview")

        body = {}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)