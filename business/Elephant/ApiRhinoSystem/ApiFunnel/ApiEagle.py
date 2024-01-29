# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 12:04 下午
@Author  : Demon
@File    : ApiEagle.py
"""

# 调度画像外部接口

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
        self.root = '/api_funnel/eagle'

    def api_save_as_group(self, file_path):
        """保存为分群"""
        api_url = parse.urljoin(self.host, f"{self.root}/saveAsGroup")
        body = {
            "report_id": file_path
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)