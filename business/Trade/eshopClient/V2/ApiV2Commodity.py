# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 12:07 下午
# @Author  : zoey
# @File    : ApiV2Commodity.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiV2Commodity:
    """
    eshop 商城微信C端
    """

    def __init__(self, token):
        self.host = Domains.domain
        self.root = '/api/eshop/v2/commodity/spu'
        self.headers = {'Authorization': token, "Content-Type": "application/json"}

    """--------------------------------商品相关CommodityController-------------------------------------"""
    def api_get_v2_commodity_detail(self, spuNo, promotionId=None):
        """
        获取商品、活动详情
        :param spuNo：商品编号
        :param promotionId：活动Id
        :return：
        """
        api_url = f'{self.host}{self.root}/{spuNo}'
        body = {
            "promotionId": promotionId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_get_v2_commodity_groups_detail(self, spuNo, promotionId):
        """
        获取商品某一拼团活动的拼团团列表
        :param spuNo：商品编号
        :param promotionId：团id
        :return：
        """
        api_url = f'{self.host}{self.root}/{spuNo}/groups'
        body = {
            "promotionId": promotionId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_get_v2_commodity_list_by_tag(self, tagName, page=1, pageSize=10):
        """
        获取商品列表（根据标签）
        :param tagName：商品标签名称
        :param page：页码
        :param pageSize：每页数量
        :return：
        """
        api_url = f'{self.host}{self.root}'
        body = {
            "tagName": tagName,
            "page": page,
            "pageSize": pageSize
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_get_v2_commodity_banner(self, tagName):
        """
        获取商品列表的banner（根据标签）
        :param tagName：商品标签名称
        :return：
        """
        api_url = f'{self.host}{self.root}/banner'
        body = {
            "tagName": tagName
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://fat.jiliguala.com")
    user = UserProperty('17521157699')
    auth = user.basic_auth
    commodityV2 = ApiV2Commodity(auth)
    print(commodityV2.api_get_v2_commodity_banner(tagName='STSC'))
    # print(commodityV2.api_get_v2_commodity_groups_detail(spuNo='Ian-Test-MA-SPU', promotionId='DACT_420'))
