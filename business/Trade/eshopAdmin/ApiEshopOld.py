# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:27 上午
# @Author  : zoey
# @File    : ApiEshopOld.py
# @Software: PyCharm
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiEshopOld:
    """
    eshop 商城管理后台-商品管理
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_commodities(self, pageNo=1, pageSize=10):
        '''商品列表'''
        api_url = f'{self.host}{self.root}/commodities'
        body = {
            "pageNo": pageNo,
            "pageSize": pageSize
        }
        resp = send_api_request(url=api_url, method='get',
                                paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_get_commodity_details(self, itemid):
        """
        获取商品详情
        :param itemid:
        :return:
        """
        api_url = f'{self.host}{self.root}/commodity/{itemid}'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_edit_commodity_details(self, itemid, storage=None, purchaseLimit=None, bannerMedia=[],
                                   desc='', subject=None, intro=None, originPirce=None, price=None,
                                   detailHtml=None, onsale=None, enable=None, payload={}):
        """
        修改商品详情，上下架商品，启用禁用商品
        :param itemid: 商品id
        :param storage:
        :param purchaseLimit:
        :param bannerMedia:
        :param desc:
        :param subject:
        :param intro:
        :param originPirce:
        :param price:
        :param detailHtml:
        :param onsale:
        :param enable:
        :param payload: 整个商品object，如果其他参数没传，只传了payload，那可以只用payload作为请求参数
        :return:
        """
        api_url = f'{self.host}{self.root}/commodity/{itemid}'
        if onsale is not None:
            body = {
                "onsale": onsale
            }
        elif enable is not None:
            body = {
                "enable": enable
            }
        elif payload:
            body = payload
        else:
            body = {
                "storage": storage,
                "purchaseLimit": purchaseLimit,
                "bannerMedia": bannerMedia,
                "desc": desc,
                "id": itemid,
                "subject": subject,
                "intro": intro,
                "originPrice": originPirce,
                "price": price,
                "detailHtml": detailHtml
            }

        resp = send_api_request(url=api_url, method='patch', paramData=body,
                                paramType='json', headers=self.headers)
        return resp

    def api_down_commodity_csv(self, q: str = ''):
        """
        下载 commodities 的详情
        :param q:
        :return:
        """
        api_url = f'{self.host}{self.root}/commodities/csv'
        body = {'q': q}
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_del_sweet_amount(self, id: str, name: str = 'sweetamount'):
        """
        删除优惠价
        :param id: 商品id
        :param name: 优惠价字段名
        :return:
        """
        api_url = f'{self.host}{self.root}/commodity/{id}/field/{name}'
        resp = send_api_request(url=api_url, method='delete', headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://dev.jiliguala.com')
    from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth

    a_token = ApiAdminAuth().api_login(username='testtesttest@jiliguala.com',
                                       password='123456').get('data').get('token')
    eshop = ApiEshopOld(a_token)
    # eshop.api_down_commodity_csv()
    eshop.api_del_sweet_amount(id='CRM_H5_ST_K3_6')