"""
=========
Author:Lisa
time:2022/10/21
=========
"""
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiligaga.app.ApiPurchaseOrderCreate import ApiPurchaseOrderCreate
from business.Jiligaga.app.ApiLogin import Login
from business.Jiligaga.app.ApiVisitorLogin import ApiVisitorLogin
from business.businessQuery import usersQuery



@pytest.mark.GagaReg
class TestApiTradeOrderCreate:
    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        # 获取配置文件的手机号
        cls.config = cls.dm.set_env_path()
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.login = Login()
        cls.ApiVisitorLogin = ApiVisitorLogin()
        cls.apipurchaseordercreate = ApiPurchaseOrderCreate()
        cls.payChannel = cls.config['gaga_app']['payChannel']
        cls.currency = cls.config['gaga_app']['currency']
        cls.countryCode = cls.config['gaga_app']['countryCodeTw']
        cls.source = cls.config['gaga_app']['source']
        cls.payPrice = cls.config['gaga_app']['payPrice']
        cls.sguNo = cls.config['gaga_app']['sguNo']
        cls.spuNo = cls.config['gaga_app']['spuNo']
        cls.num = cls.config['gaga_app']['num']

    # def test_purchase_charge_iap(self):
    #     """IAP支付回调C端接口"""
    #     # 获取订单编号
    #     order = self.apipurchaseordercreate.purchase_order_create(payPrice=self.gaga_app["payPrice"],
    #                                                               countryCode=self.gaga_app["countryCodeTw"],
    #                                                               payChannel="iap",
    #                                                               currency=self.gaga_app["currency"],
    #                                                               source="roadmap_purchase",
    #                                                               sguNo=self.gaga_app["sguNo"],
    #                                                               spuNo=self.gaga_app["spuNo"], num=1)[
    #         "data"]["orderNo"]
    #     resp = self.apipurchaseordercreate.purchase_charge_iap(orderNo=order)
    #     check.equal(resp["code"], 0)

    # def test_user_order_query(self):
    #     """机转-用户订单查询C端接口"""
    #     # 获取token
    #     resp = self.apipurchaseordercreate.user_order_query(authorization=self.apipurchaseordercreate.token)
    #     check.equal(resp["code"], 0)

    def test_purchase_order_create(self):
        """机转-c端用户创建订单"""
        payChannel = self.payChannel
        currency = self.currency
        source = self.source
        countryCode = self.countryCode
        payPrice = self.payPrice
        spuNo = self.spuNo
        sguNo = self.sguNo
        num = self.num
        resp = self.apipurchaseordercreate.purchase_order_create(payChannel, currency, source, countryCode, payPrice,
                                                                 spuNo,
                                                                 sguNo, num)
        check.equal(resp["code"], 0)
