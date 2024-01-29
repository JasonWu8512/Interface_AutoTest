# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/22 1：58 下午
@Author  : Cora
@File    : ApiBoard.py
接口：看板的增删改查
 /api_board/board/add
 /api_board/board/save
 /api_board/board/fetchList
 /api_board/board/fetchById
 /api_board/board/delete
"""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header

class ApiBoard(object):
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
        self.root = '/api_board/board'

    def api_board_add(self, name, is_public):
        """
        新增看板
        :param name :看板名称
        :param is_public :是否公开
        :return :
        """
        api_url = self.host + f"{self.root}/add"
        body = {
            "name": name,
            "isPublic": is_public
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_board_save(self, name, ids, desc, is_public, chart_config, update_time,
                       owner, has_permission, global_filter, index_rpt, rpt_count):
        """
        更新保存看板
        :param ids :看板id
        :param name :看板名称
        :param is_public :是否公开
        :param desc :描述信息
        :param chart_config: 报表的配置信息
        :param update_time: 更新保存的时间
        :param owner: 看板负责人
        :param has_permission: 是否拥有看板权限
        :param global_filter: 全剧筛选
        :param index_rpt: 默认图表的大小
        :param rpt_count: 图表个数
        :return :
        """
        api_url = self.host + f"{self.root}/save"
        body = {
            "id": ids,
            "name": name,
            "desc": desc,
            "isPublic": is_public,
            "chartConfig": chart_config,
            "updateTime": update_time,
            "owner": owner,
            "hasPermission": has_permission,
            "globalFilter": global_filter,
            "indexRpt": index_rpt,
            "rptCount": rpt_count

        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_board_delete(self, ids):
        """
        删除看板
        :param ids :看板id
        :return :
        """
        api_url = self.host + f"{self.root}/delete"
        body = {
            "id": ids
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_board_list(self):
        """s
        获取看板列表
        :return :
        """
        api_url = self.host + f"{self.root}/fetchList"
        body = {

        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_board_fetch_id(self, ids):
        """
        获取看板信息
        :param ids :看板id
        :return :
        """
        api_url = self.host + f"{self.root}/fetchById"
        body = {
            "id": ids
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)
