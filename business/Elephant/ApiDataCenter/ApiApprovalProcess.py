# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 1:27 下午
@Author  : Demon
@File    : ApiApprovalProcess.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header

class ApiApprovalProcess(object):
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
        self.root = '/api_basic/permissionApproval'

    def api_approval_process(self, uid, tbname, dbname):
        """
        获取库表的权限操作人，一级与二级
        :param uid,
        :param tbname,
        :param dbname
        :return
        """
        url = self.host + f'{self.root}/approvalProcess'
        body = {
            "userId": uid,
            "tableName": tbname,
            "databaseName": dbname
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

