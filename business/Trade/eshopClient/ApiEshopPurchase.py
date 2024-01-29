# coding=utf-8
# @Time    : 2020/12/3 9:47 上午
# @Author  : jerry
# @File    : ApiEshopPurchase.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiEshopPurchase:
    """
    eshop
    PurchaseController
    """

    def __init__(self, wechat_token, basic_token=None):
        self.host = Domains.domain
        self.root = '/api/eshop/purchase'
        self.headers = {'Authorization': basic_token, "wechattoken": wechat_token, "Content-Type": "application/json"}

    """-------------------------------------------purchase相关PurchaseController--------------------------------"""

    def api_purchase_validation(self, itemId, source=None):
        """
        购买资格校验
        :param itemId:商品id 必填
        :param source:链接来源: 班主任/规划师 非必填
        :return:
        """
        api_url = f'{self.host}{self.root}/qualification/validation'
        body = {
            'itemid': itemId,
            "source": source
        }
        # if source:
        #     body.update({"source": source})
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params',
                                headers=self.headers)
        return resp