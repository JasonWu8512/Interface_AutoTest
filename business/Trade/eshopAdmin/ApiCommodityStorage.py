# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:26 上午
# @Author  : zoey
# @File    : ApiCommodityStorage.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiCommodityStorage:
    """
    eshop 商城管理后台-新商品管理-库存管理
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_commoditys_storage(self, page=1, pageSize=10, keyword=None, type=None, state=None):
        """
        获取商品库存列表
        :param page: 页面编号
        :param pageSize: 一页展示的商品数量
        :param keyword: 关键字
        :param type: 商品类型（1：SKU；2：SGU）
        :param state: 商品状态（0：编辑中；1：已启用；2：已下架；3：已禁用）
        """
        api_url = f'{self.host}{self.root}/storage'
        body = {
            "page": page,
            "pageSize": pageSize,
            "keyword": keyword,
            "type": type,
            "state": state
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_edit_commodity_storage(self, commodityId, key, value):
        """
        修改单个商品库存
        :param commodityId: sxuid
        :param key: 库存类型（stockNum：实际库存；reserveLock：保留库存；soldNum：销量）
        :param value: 库存值
        """
        api_url = f'{self.host}{self.root}/storage/{commodityId}'
        body = {
            "key": key,
            "value": value
        }
        resp = send_api_request(url=api_url, method='patch', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_edit_commoditys_storage(self, ids, value):
        """
        批量增加多个商品的实际库存
        :param ids: sxuid列表
        :param value: 库存值
        """
        api_url = f'{self.host}{self.root}/storage'
        body = {
            "ids": ids,
            "value": value
        }
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp