# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 11:34 上午
@Author  : Demon
@File    : ApiSync.py
"""

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiSync(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/sync'

    def api_report_sync_table(self, body):
        """
        异步刷新缓存相关参数, 数据库.表 信息/缓存管理-刷新指定表的缓存
        :param body: {"jlgl_rpt": ["rpt_revenue_reading_total_add_d"]}
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/syncTable")
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_sync_init(self):
        """
        每天的初始化方法：八点半、九点半、十点半定时刷新保存的报表，预览不刷新
        :param body: {"jlgl_rpt": ["rpt_revenue_reading_total_add_d"]}
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/init")
        body = {}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)