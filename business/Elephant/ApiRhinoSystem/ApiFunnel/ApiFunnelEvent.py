# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 12:04 下午
@Author  : Demon
@File    : ApiFunnelEvent.py
"""

# 漏斗事件、属性控制层

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiFunnelEvent(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            # Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_funnel/funnel'

    def api_funnel_fetch_all_products(self, column, event_keys=None, tb='ods.ods_jlgl_click_log_dis', typ='user'):
        """
        获取所有分类事件
        :param :event_id : 事件ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAllProducts")
        body = {
            "column": column,
            "table": tb,
            "type": typ,
        }

        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_funnel_fetch_all_events(self, product_ids="jlgl"):
        """
        获取事件
        :param :product_ids : 产品ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAllEvents")
        body = {
            "productIds": [product_ids]
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_funnel_fetch_event_props(self, event_id):
        """
        根据事件id获取属性
        :param :event_id : 事件ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchEventProps")
        body = {
            "eventId": event_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_funnel_fetch_column_info(self, column, event_keys=None, tb='ods.ods_jlgl_click_log_dis', typ='user'):
        """
        获取属性字段的枚举值及类型
        :param :event_id : 事件ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchColumnInfo")
        body = {
            "column": column,
            "table": tb,
            "type": typ,
        }
        if event_keys:
            body.update(**dict(eventKeys=event_keys))
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_funnel_fetch_public_props(self, is_dimen=None):
        """
        获取所有通用属性
        :param :event_id : 事件ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchPublicProps")

        body = {
            "isDimension": is_dimen,
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)