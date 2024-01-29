# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/8/3 5:17 下午
@Author   : Anna
@File     : test_store.py
"""
from config.env.domains import Domains
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.magikabiz.ApiStore import ApiStore
import pytest
import pytest_check as check


@pytest.mark.MagikBiz
class TestStore(object):
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
        cls.stone = ApiStore(cls.token, cls.version)

    # @pytest.mark.skip
    def test_get_home(self):
        resp = self.stone.api_get_home()
        # 断言返回code码正常
        check.equal(resp["code"], 0)
        print(resp)
        # 断言用户状态为1(魔石商城用户)
        check.equal(resp["data"]["userStatus"], 1)

    def test_get_item(self):
        resp = self.stone.api_get_item()
        # 断言接口正常返回商品
        check.equal(resp["data"]["items"][0]["commodityTitle"], "呱呱手机支架")

    def test_get_detail(self):
        resp = self.stone.api_get_detail("MG_goods_012_SPU")
        resp01=resp["data"]["itemName"]
        print(resp01)
        # 断言商品信息与接口返回一致
        check.equal(resp["data"]["itemName"], "呱呱手机支架")
        print(resp)


if __name__ == '__main__':
    store = TestStore()
    store.setup_class()
    store.test_get_home()
    store.test_get_item()
    store.test_get_detail()