# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 11:53 上午
@Author  : Demon
@File    : ApiEventConfig.py
"""

# 事件配置控制层

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiEventConfig(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/eventConfig'

    def api_fetch_all_events(self, project_id):
        """
        获取所有事件属性信息,所有分类事件
        :param :project_id : 项目ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAllEvents")
        body = {
            "projectId": project_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_fetch_all_projects(self):
        """
        获取所有事件属性信息
        :param :project_id : 项目ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAllProjects")
        body = {
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_fetch_all_props(self):
        """
        获取所有属性 用户/事件
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAllProps")
        body = {
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_fetch_column_info(self, project_id):
        """
        获取属性字段的枚举值及类型
        :param :project_id : 项目ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchColumnInfo")
        body = {
            "projectId": project_id
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)
