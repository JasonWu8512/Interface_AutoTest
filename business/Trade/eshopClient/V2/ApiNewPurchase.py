# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 12:07 下午
# @Author  : zoey
# @File    : ApiNewPurchase.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiNewPurchase:
    """
    eshop
    NewPurchaseController
    """

    def __init__(self, token):
        self.host = Domains.domain
        self.root = '/api/eshop/v2/purchase'
        self.headers = {'Authorization': token, "Content-Type": "application/json"}

    """-------------------------------------------purchase相关NewPurchaseController--------------------------------"""

    def api_new_purchase_validation(self, sp2xuId, source=None):
        """
        购买资格校验
        :param sp2xuId：商品id 必填
        :param source：链接来源: 班主任/规划师 非必填
        :return:
        """
        api_url = f'{self.host}{self.root}/qualification/validation'
        body = {
            "sp2xuId": sp2xuId,
            "source": source
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params',
                                headers=self.headers)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    user = UserProperty('17521157699')
    wechattoken = user.encryptWechatToken
    eshop_basic_auth = user.basic_auth
    purchase = ApiNewPurchase(wechattoken, eshop_basic_auth)
    print(purchase.api_new_purchase_validation(sp2xuId=972, source='class_advisor'))
