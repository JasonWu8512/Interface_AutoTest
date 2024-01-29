"""
=========
Author:Lisa
time:2022/6/23 1:23 下午
=========
"""
import email
import pytest
import lazy_property

from business.common.UserProperty import UserProperty
from config.env.domains import Domains

from testcase.Trade import order
from utils.requests.apiRequests import send_api_request


class ApiTradeOrderCreate():
    """
    创建订单
    OrderController
    """
    def __init__(self, authorization,):
        self.host = Domains.get_gaga_host()
        self.root='/api/trade/order'
        self.header={
            "authorization":"Basic ZmM4ODgyYjVmYTY3NGU4MGIyM2ZlNzYzNjBlZmEyZTk6MGVmNDg3ZjU0ZmM3NDcwNWIxZmMxYTE3MjRjZjE3ODE6ZWU1NGMxMThlMjA0MGNhNw==",
            "Content-Type":"application/json",


        }

    def api_trade_order_create(self, payChannel, currency, source, payPrice, spuNo='SPU_CARD2_CN',skuNo='vipcard30',num='1') :
        """
        
        创建订单
        """
        api_url='/create'
        body= {
                'payChannel': payChannel,
                'currency': currency,
                'source': source,
                'payPrice': payPrice,
                'skus':[{
                    'spuNo': spuNo,
                    'skuNo': skuNo,
                    'num': num
                        }]
        }

        print(self.host + self.root+api_url)
        resp=send_api_request(url=self.host + self.root + api_url, paramType='json', paramData=body, method="post",
                                  headers=self.header)


        print(resp)



# if __name__ == '__main__':
#     dm = Domains()
#     config = dm.set_env_path("fat")
#     token = UserProperty('lisa02@qq.com').basic_auth
#     order = ApiTradeOrderCreate(token)
#     # 创建订单
#     resp= order.api_trade_order_create(payChannel='iap',currency='CNY',source='menu_vip_valid',payPrice='888')
#     print(resp)
