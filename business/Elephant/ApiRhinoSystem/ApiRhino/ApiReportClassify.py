# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 11:46 上午
@Author  : Demon
@File    : ApiReportClassify.py
"""

# 报表分类

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ParamConfigs(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.header = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/reportEnum'

    def api_report_enum_fetch_all(self):
        """
        获取土拨鼠报告下的配置 报表分类，业务线
        :return :
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAll")
        return send_api_request(url=api_url, headers=self.header, method="post")

    def api_report_enum_add_tag_value(self, ids, val):
        """
        增加业务线/分类 value
        :param ids: id ，api_get_enum_all
        :param val: 新增的名称
        :return :
        """
        api_url = parse.urljoin(self.host, f"{self.root}/addTagValue")
        body = {
            "id": ids,
            "value": val
        }
        return send_api_request(url=api_url, headers=self.header, method="post", paramType="json", paramData=body)

    def api_report_enum_delete_tag_value(self, ids):
        """
        删除业务线/分类 value
        :param ids: id ，业务线/分类的ID
        :return :
        """
        api_url = parse.urljoin(self.host, f"{self.root}/deleteTagValue")
        body = {
            "id": ids,
        }
        return send_api_request(url=api_url, headers=self.header, method="post", paramType="json", paramData=body)

    def api_report_enum_update_tag_value(self, ids, value):
        """
        删除业务线/分类 value
        :param ids: id ，业务线/分类的ID
        :param value: value ，业务线/分类的ID对应的内容
        :return :
        """
        api_url = parse.urljoin(self.host, f"{self.root}/updateTagValue")
        body = {
            "id": ids,
            "value": value,
        }
        return send_api_request(url=api_url, headers=self.header, method="post", paramType="json", paramData=body)

    def api_report_enum_add_tag(self, ids, val):
        """
        增加业务线/分类 tag
        :param ids: id ，api_get_enum_all
        :param val: 新增的名称
        :return :
        """
        api_url = parse.urljoin(self.host, f"{self.root}/addTag")
        body = {
            "id": ids,
            "value": val
        }
        return send_api_request(url=api_url, headers=self.header, method="post", paramType="json", paramData=body)

    def api_report_enum_delete_tag(self, ids):
        """
        删除业务线/分类 tag
        :param ids: id ，业务线/分类的ID
        :return :
        """
        api_url = parse.urljoin(self.host, f"{self.root}/deleteTag")
        body = {
            "id": ids,
        }
        return send_api_request(url=api_url, headers=self.header, method="post", paramType="json", paramData=body)

    def api_report_enum_update_tag(self, ids, value):
        """
        删除业务线/分类 tag
        :param ids: id ，业务线/分类的ID
        :param value: value ，业务线/分类的ID对应的内容
        :return :
        """
        api_url = parse.urljoin(self.host, f"{self.root}/updateTag")
        body = {
            "id": ids,
            "value": value,
        }
        return send_api_request(url=api_url, headers=self.header, method="post", paramType="json", paramData=body)
