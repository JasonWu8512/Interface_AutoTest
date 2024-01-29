# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:26 上午
# @Author  : zoey
# @File    : ApiCommodity.py
# @Software: PyCharm
import res as res

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCommodity:
    """
    eshop 商城管理后台
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_sxu_list(self, pageNo=1, pageSize=10, sxuType=1, keyword=None, commodityNo=None, state=None,
                         priceBy=None):
        """
        SKU/SGU管理：获取SKU/SGU列表
        :param pageNo: 当前页数
        :param pageSize: 每页数据量
        :param sxuType: 商品类型，1：SKU，2：SGU
        :param keyword: 查询关键字
        :param commodityNo:SKU/SGU商品ID
        :param state: 商品状态，0：编辑中，1：已启用，2：已下架，3：已禁用
        :param priceBy: 商品类型，0：现金 1：积分
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/sku'
        body = {
            'pageNo': pageNo,
            'pageSize': pageSize,
            'type': sxuType,
            'keyword': keyword,
            'commodityNo': commodityNo,
            'state': state,
            'priceBy': priceBy,
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_create_edit_sxu(self, sxuBody):
        """
        SKU/SGU管理：新增、编辑SKU/SGU
        :param sxuBody: SKU/SGU商品信息
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/sku'
        body = sxuBody
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_sxu_detail(self, sxuId):
        """
        SKU/SGU管理：获取SKU/SGU详情
        :param sxuId: SKU/SGU商品数据库id
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/sku/{sxuId}'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_get_spu_list(self, pageNo=1, pageSize=10, priceBy=0, keyword=None, commodityNo=None, channelId=None,
                         state=None):
        """
        SPU管理：获取SPU列表
        :param pageNo: 当前页数
        :param pageSize: 每页数据量
        :param keyword: 查询关键字
        :param commodityNo: SPU商品ID
        :param channelId: 归属业务
        :param state: 商品状态，0：编辑中，1：已启用，2：已下架，3：已禁用
        :param priceBy: 商品类型，0：现金 1：积分
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/spu'
        body = {
            'pageNo': pageNo,
            'pageSize': pageSize,
            'type': 0,
            'keyword': keyword,
            'commodityNo': commodityNo,
            'channelId': channelId,
            'state': state,
            'priceBy': priceBy
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_create_edit_spu(self, spuBody):
        """
        SPU管理：新增、编辑SPU
        :param spuBody: SPU商品信息
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/spu'
        body = spuBody
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_spu_detail(self, spuId):
        """
        SPU管理：获取SPU详情
        :param spuId: SPU商品数据库id
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/spu/{spuId}'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_import_spu(self, keyword=None, commodityNo=None, channelId=None, state=None):
        """
        SPU管理：导出SPU
        :param keyword: 查询关键字
        :param commodityNo: SPUID
        :param channelId: 归属业务
        :param state: SPU状态
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/spu/csv'
        body = {
            'keyword': keyword,
            'commodityNo': commodityNo,
            'type': 0,
            'channelId': channelId,
            'state': state
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_partial_edit_sxu_title(self, sxuId, title, priceDiamond=None, priceGuaDouPp=None, priceMagika=None,
                                   priceRmb=None):
        """
        SXU管理：列表中快速修改SXU部分信息
        :param sxuId: SXU数据库id
        :param title: SXU标题
        :param priceDiamond: 积分类型SKU/SGU钻石价格（暂无此修改需求）
        :param priceMagika: 积分类型SKU/SGU魔石价格（暂无此修改需求）
        :param priceRmb: 现金类型SKU/SGU指定售价（暂无此修改需求）
        :param priceGuaDouPp: 现金类型SKU/SGU呱豆抵扣比例（暂无此修改需求）
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/sxu/{sxuId}'
        body = {
            'title': title,
            'priceDiamond': priceDiamond,
            'priceGuaDouPp': priceGuaDouPp,
            'priceMagika': priceMagika,
            'priceRmb': priceRmb
        }
        resp = send_api_request(method='patch', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_channel_list(self, keyword=None):
        """
        获取归属业务列表
        :param keyword: 归属业务搜索关键字
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/channel'
        body = {
            'keyword': keyword
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_get_category_list(self):
        """
        获取商品类型列表
        :return:
        """

        api_url = f'{self.host}{self.root}/commodity/category'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_domain('https://dev.jiliguala.com')
    eshop = ApiCommodity('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c3IiOiIwZTg2YWNiY2EyODk0YTMxYTY1OGUyMjhmZmI0MDA1YSIs'
                         'ImV4cCI6MTYxMjU4MDA5OH0.MyFmQ1SY_KLkMN6WVuAVn9Ao561f63ef0RlOBqlTWgiIaF9D6S3dTK2_Y-3F1ifg-vVYS'
                         'bXydJcNiV-4PUowjUknSD63KWHFeRMMjUe5cM4qWSIKMLWAs5HwdKczKGBgy7I385Q2ahmuK0NsCQJA7V3uvJdNvGwx_U'
                         'P52p-0eEz7wPUYFV8GZ-SwnoCqGowLZs0kv6nPwG0h4o4A15RwqEoIoFLhe8QPHdS_YXSDffegvx7h0V3CAQLr3M7Ib2z'
                         'hU6h9t8fS3JNUv1ziSRjJpWuLz1uFrlwykWMwE1iZIZ0_-wJOAXTakvnrEOPkQLd6o93qUBcuHNiM05geBL76Zg')
    # res = eshop.api_get_spu_detail(1157)
    sxu = res['data']
    sxu['id'] = 0
    sxu['commodityNo'] = 'automation-test'
    print(eshop.api_create_edit_spu(sxu))
    # print(eshop.api_partial_edit_sxu_title(1172, '测试', priceGuaDouPp=50, priceRmb=10000))
    # print(eshop.api_import_spu(keyword='IAN-COPY-TEST-01', commodityNo='IAN-COPY-TEST-01', channelId=4, state=1))

