# coding=utf-8
# @Time    : 2020/9/10 1:18 下午
# @Author  : keith
# @File    : test99


import pytest

from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder
from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains


@pytest.mark.xShare
class TestPay(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['url'])
        cls.account = cls.config["account"]
        cls.user = ApiUser()
        # keith token
        # cls.token = cls.user.get_token(typ="mobile", u=cls.account["user"], p=cls.account["pwd"])
        cls.xshare_refund_token = "Basic MTNjNDlkNmM3YmI1NGQzYWE5NjNiMThkMjBlNGExNjE6MmNiMTBiYmQyMzZkNDIwNjkzY2JhMjE3ZDlmNjBhZWI="
        # 用户信息实例
        # cls.user_info = ApiUserInfo(token=cls.token)
        # 支付实例
        # cls.pay = ApiPingppOrder(token=cls.token)
        # 退款99实例
        cls.refund_pay = ApiPingppOrder(token=cls.xshare_refund_token)

    def test_switch_modes(self):
        pass
