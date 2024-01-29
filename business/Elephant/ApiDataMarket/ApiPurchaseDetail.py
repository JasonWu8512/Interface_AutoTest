# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/24 4:55 下午
@Author  : Demon
@File    : ApiPurchaseDetail.py
"""



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse
import os



class ApiPurchaseDetail(object):

    def __init__(self, token):
        # 请求头文件
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/purchaseDetail'

    def api_adhoc_sql_info_sql_list(self, user_name='demon_jiao', ):
        """该用户当前历史查询并保存sql脚本"""
        url = parse.urljoin(self.host, f'{self.root}/sqlList')
        body = {
            "user": user_name,
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)