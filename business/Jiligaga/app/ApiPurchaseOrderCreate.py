"""
=========
Author:Lisa
time:2022/10/18 6:02 下午
=========
"""
import token
import time

from pandas.conftest import cls

from config.env.domains import Domains

from testcase.Trade import order
from utils.requests.apiRequests import send_api_request
from business.Jiligaga.app.ApiLogin import Login
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3


class ApiPurchaseOrderCreate(object):

    def __init__(self) -> object:
        # self.login = Login()
        self.apiAccountV3 = ApiAccountV3()
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        self.token = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                      countrycode=self.gaga_app["countryCodeTw"])["data"]["auth"]

        print(self.token)
        self.headers = {
            "Authorization": self.token,
            'Content-Type': 'application/json',
            "platform": "ios",
            "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC"
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]
        self.t = int(round(time.time()))
        print(self.t)

    def purchase_order_create(self, payChannel, currency, source, countryCode, payPrice, spuNo, sguNo, num):
        """机转-c端创建订单"""
        api_url = "/api/purchase/order/create"
        body = {
            'payChannel': payChannel,
            'currency': currency,
            'source': source,
            'countryCode': countryCode,
            'payPrice': payPrice,
            'sgus': [{
                'spuNo': spuNo,
                'sguNo': sguNo,
                'num': num
            }]
        }
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    # def purchase_charge_iap(self, orderNo):
    #     """机转-IAP支付回调C端接口"""
    #     api_url = "/api/purchase/charge/iap"
    #     body = {
    #         'orderNo': orderNo,
    #         'goIapReceipt': '{"acknowledged":false,"inAppCurrency":"HKD","inAppPrice":"909.000000","orderId":"GPA.' + str(
    #             self.t) + '-4561-7469-38054","packageName":"com.jiliguala.intl","productId":"sgu_l3l4","purchaseState":1,"purchaseTime":1667553376553,"purchaseToken":"bflegjilgoabghhdpnpaklid.AO-J1Ow0qwKLvj64btL9PeYzSraeEoUP5puFjVLZlb0FaKn3S48qolK5OkXgDt6XpF5XN6rOnMYe8mCr670f6W8JJgMpuThfsQ","quantity":1}',
    #         'inAppPrice': '909.000000',
    #         'inAppCurrency': 'HKD'
    #     }
    #     resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp

    def user_order_query(self, authorization):
        """机转-用户订单查询C端接口"""
        api_url = "/api/purchase/order/user/roadmap"
        body = {
            "Authorization": authorization,
            "timezone": "Asia%2FShanghai",
            "Accept-Language": "zh-Hans-CN"
        }
        print(body)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp
