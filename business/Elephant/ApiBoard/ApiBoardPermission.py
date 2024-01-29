# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/23 2：58 下午
@Author  : Cora
@File    : ApiBoardPermission.py
"""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header

class ApiBoardPermission(object):
    def __init__(self, token):
        """
        公共数据
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_board/board/permission'

    def api_board_permission_approve_user(self, ids):
        """
        拉取审批人
        :param ids: id
        :return :
        """
        api_url = self.host + f"{self.root}/fetchApproveUser"
        body = {
            "id": ids
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_board_permission_approve_by_user(self, filter, page_size, orders, current_page, status=0):
        """
        拉取审批记录列表
        :param filter: 搜索框的搜索条件
        :param status: 审批状态
        :param page_size: 每页数据条数
        :param current_page：当前页面
        :param orders:排序
        :return :
        """
        api_url = self.host + f"{self.root}/fetchApproveByUser"
        body = {
            "filter": filter,
            "status": status,
            "pageSize": page_size,
            "currentPage": current_page,
            "orders": orders
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)


    def api_board_permission_apply(self, ids, apply_reason):
        """
        看板权限申请
        :param ids: 看板id
        :param apply_reason: 审批结果
        :return :
        """
        api_url = self.host + f"{self.root}/apply"
        body = {
            "id": ids,
            "applyReason": apply_reason
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_board_permission_approve(self, ids, approve_response,status):
        """
        看板审批
        :param ids: 看板id
        :param status: 审批状态
        :param approve_response: 审批结果
        :return :
        """
        api_url = self.host + f"{self.root}/apply"
        body = {
            "id": ids,
            "status": status,
            "approveResponse": approve_response
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)
