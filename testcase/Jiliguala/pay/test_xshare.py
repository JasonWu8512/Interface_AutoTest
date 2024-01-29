# coding=utf-8
# @Time    : 2020/9/3 3:05 下午
# @Author  : keith
# @File    : test_xshare


import pytest
import pytest_check as check

from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder
from business.Jiliguala.user.ApiUser import ApiUser
from business.xshare.ApiMiniMall import ApiMiniMall
from business.xshare.ApiSwitches import ApiSwitches

from business.businessQuery import openuserQuery

from config.env.domains import Domains


@pytest.mark.xShare
@pytest.mark.minimall
class TestXshare(object):

    dm = Domains()
    db = openuserQuery

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['url'])
        cls.mobile = cls.config["account"]['mobile']
        cls.user = ApiUser()
        # 获取token
        cls.token = cls.db.get_openuser(mobile=cls.mobile)['sp99']['token']

        # 支付实例
        cls.pay = ApiPingppOrder(token=cls.token)
        # 小程序商城实例
        cls.mini = ApiMiniMall(token=cls.token)
        # 售卖开关
        cls.switch = ApiSwitches(token=cls.token)

    def test_purchase_99_order(self):
        try:


            pass
        finally:

            self.pay.api_order_refund(order_id=123)

    def test_xshare_switches(self):
        resp = self.switch.api_get_switches_mode("minimall")
        check.is_in(resp['data']['mode'], [1, 2, 0])
    
    def test_xshare_bind_status(self):
        pass


if __name__ == '__main__':
    a = TestXshare()
    a.setup_class()
    a.test_xshare_switches()