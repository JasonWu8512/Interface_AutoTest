# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:26 上午
# @Author  : zoey
# @File    : ApiCommodityTag.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from urllib.parse import urlencode

class ApiCommodityTag:
    """
    eshop 商城管理后台-标签查询与新建
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_commodity_tag(self, pageNo=1, pageSize=50, queryCondition=None):
        """
        获取商品标签
        :param pageNo: 页面编号
        :param pageSize: 每页大小
        :param queryCondition: 查询条件（要进行URL编码）
        """
        api_url = f'{self.host}{self.root}/tag/list'
        body = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "queryCondition": queryCondition
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_create_commodity_tag(self, name):
        """
        创建商品标签
        :param name：标签名字
        """
        api_url = f'{self.host}{self.root}/tag/create'
        body = {
            "name": name
        }
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp