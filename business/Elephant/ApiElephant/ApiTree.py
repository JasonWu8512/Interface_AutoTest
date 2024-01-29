# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/22 2:11 下午
@Author  : Demon
@File    : ApiTree.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse
import os



class ApiTree(object):

    def __init__(self, token):
        # 请求头文件
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_adhoc/leftTree'

    def api_adhoc_left_tree_list(self, user_name='demon_jiao', ):
        """查看左侧数据库表字段列表"""
        url = parse.urljoin(self.host, f'{self.root}/list')
        body = {
            "user": user_name
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_left_tree_list_database(self, user_name='demon_jiao', ):
        """查看左侧数据库列表"""
        url = parse.urljoin(self.host, f'{self.root}/listDatabase')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_left_tree_list_table(self, user_name='demon_jiao', ):
        """查看左侧数据库表列表"""
        url = parse.urljoin(self.host, f'{self.root}/listTable')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_left_tree_list_column(self, user_name='demon_jiao', ):
        """查看左侧数据库表字段列表"""
        url = parse.urljoin(self.host, f'{self.root}/listColumn')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

