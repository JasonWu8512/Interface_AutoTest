# @Time : 2021/7/30
# @Author : kira
# @File : ApiCommodityCategory.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCommodityPropertys:
    """
    eshop 商城管理后台---商品属性管理
    """
    root = '/api/eshop-admin'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_property_list(self):
        """
        获取商品属性列表
        """
        api_url = f'{self.host}{self.root}/commodity/properties'
        resp = send_api_request(method='get', url=api_url, paramType='params', headers=self.headers)
        return resp

    def api_create_edit_property(self, batchRequest=None):
        """
        新增/编辑商品属性
        batchRequest：所有属性项和属性值的集合
        """
        api_url = f'{self.host}{self.root}/commodity/properties/value'
        body = {
            'batchRequest': batchRequest
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp
