# coding=utf-8
# @Time    : 2020/8/12 3:57 下午
# @Author  : keith
# @File    : test_user


import pytest
import pytest_check as check

from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.user.ApiUserInfo import ApiUserInfo
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
        cls.token = cls.user.get_token(typ="mobile", u=cls.account["mobile"], p=cls.account["pwd"])
        cls.pay = ApiPingppOrder(token=cls.token)
        cls.user_info = ApiUserInfo(token=cls.token)

    def test_manage_guadou(self):
        """测试充值瓜豆"""
        user = self.user_info.api_get_users(self.account['_id'])
        resp = self.user_info.api_manage_guadou(guaid=self.account["guaid"], guadouBalance=1000)
        check.equal(resp["data"], "success")
        check.equal(resp["status_code"], 200)

    # def test_user_center(self):
    #     """测试用户中心"""
    #     resp = self.user_info.api_get_user_center(bid=self.account['b_id'], id=self.account['_id'], level="L1XX")


if __name__ == '__main__':
    a = TestPay()
    a.setup_class()
    a.test_manage_guadou()
