# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/8/4 2:26 下午
@Author   : Anna
@File     : test_order.py
"""
from business.Jiliguala.magikabiz.ApiStore import ApiStore
from config.env.domains import Domains
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.magikabiz.ApiOrder import ApiOrder
import pytest
import pytest_check as check


@pytest.mark.MagikBiz
class TestOrder(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化用户
        user = ApiUser()
        # 获取用户token信息
        cls.token = user.get_token(typ="mobile", u="19393123455", p="123456")
        cls.version = cls.config['version']['ver11.6']
        # 实例化ApiAddress类
        cls.order = ApiOrder(cls.token, cls.version)
        cls.store = ApiStore(cls.token, cls.version)

    # @pytest.mark.skip
    def test_put_order(self):
        # 先获取用户的魔石数
        resp01 = self.store.api_get_home()
        userStones = resp01["data"]["userStones"]
        # 已知商品价格，获取兑换成功后的魔石数
        finnalStones = userStones - 3000
        print(finnalStones)
        resp = self.order.api_put_order("ParentCenterEntry", "MG_goods_012_SPU", "北京市", "东城区", "北京市", "测试订单地址", [{
            "amount": 1,
            "id": 2561
        }], "3000", "3000", "19696969696", "tester", "true")
        # 断言返回code码正常
        check.equal(resp["code"], 0)
        print(resp)

        # 兑换成功后，重新获取用户魔石数
        resp02 = self.store.api_get_home()
        afterStones = resp02["data"]["userStones"]
        print(afterStones)

        # 验证用户最终魔石数量与预期一致
        check.equal(afterStones, finnalStones)


if __name__ == '__main__':
    order = TestOrder()
    order.test_put_order()
