# coding=utf-8
# @Time    : 2020/8/12 10:55 上午
# @Author  : keith
# @File    : test_pay


import pytest
import pytest_check as check

from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder
from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains


@pytest.mark.pay
class TestPay(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['url'])
        cls.account = cls.config["account"]
        cls.user = ApiUser()
        # keith token
        # cls.token = cls.user.get_token(typ="mobile", u=cls.account["mobile"], p=cls.account["pwd"])
        cls.xshare_refund_token = "Basic MTNjNDlkNmM3YmI1NGQzYWE5NjNiMThkMjBlNGExNjE6MmNiMTBiYmQyMzZkNDIwNjkzY2JhMjE3ZDlmNjBhZWI="
        # 用户信息实例
        # cls.user_info = ApiUserInfo(token=cls.token)
        # 支付实例
        # cls.pay = ApiPingppOrder(token=cls.token)
        # 退款99实例
        cls.refund_pay = ApiPingppOrder(token=cls.xshare_refund_token)
        # 编辑瓜豆，充值500
        # cls.user_info.api_manage_guadou(guaid=cls.account['guaid'], guadouBalance=500)

    def test_order_detail_without_oid(self):
        """测试订单详情缺失oid字段"""
        resp = self.pay.api_get_order_detail(oid=None)
        check.equal(resp['msg'], "request validation error")
        check.equal(resp['status_code'], 400)

    # C78438
    def test_pay_with_guadou_deduct(self):
        """测试瓜豆支付抵扣"""
        oid = None
        try:
            # 瓜豆支付订单
            resp = self.pay.api_order_purchase(physical=False, bid=self.account["b_id"], channel="guadou",
                                               itemid="L2XX")
            # 断言支付状态
            check.equal(resp["data"]["status"], "paid")
            oid = resp["data"]["oid"]
        finally:
            # 退款
            self.pay.api_order_refund(order_id=oid)

    def test_order_detail(self):
        """测试订单详情"""
        oid = None
        try:
            # 瓜豆支付订单
            resp = self.pay.api_order_purchase(physical=False, bid=self.account["b_id"], channel="guadou",
                                               itemid="L2XX")
            # 断言
            check.equal(resp["data"]["status"], "paid")
            oid = resp["data"]["oid"]
            # 订单详情
            detail = self.pay.api_get_order_detail(oid=oid)
            check.equal(detail['data']['oid'], oid)
            check.equal(detail['data']['channel'], "guadou")
            check.equal(detail['status_code'], 200)
            # 订单
            order = self.pay.api_get_order(oid=oid)
            check.equal(order['data']['status'], "paid")
            check.equal(order['status_code'], 200)
        finally:
            self.pay.api_order_refund(order_id=oid)

    def test_refund(self):
        self.refund_pay.api_order_refund(order_id="C80780")


if __name__ == '__main__':
    a = TestPay()
    a.setup_class()
    a.test_refund()
