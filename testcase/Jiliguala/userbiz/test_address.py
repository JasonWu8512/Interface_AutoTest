# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/6/10 2:02 下午
@Author   : Anna
@File     : test_address.py
"""
from business.Jiliguala.userbiz.ApiAddress import ApiAddress
from config.env.domains import Domains
from business.Jiliguala.user.ApiUser import ApiUser
import pytest
import pytest_check as check


@pytest.mark.UserBiz
class TestAddress(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 用户实例化
        user = ApiUser()
        # 获取用户token信息
        cls.token = user.get_token(typ="mobile", u="19393123455", p="123456")
        cls.version = cls.config['version']['ver11.6']
        # 实例化ApiAddress类
        cls.address = ApiAddress(cls.token, cls.version)
        print("setup")

    @pytest.mark.skip
    def test_get_address(self):
        resp = self.address.api_get_address()
        # 断言请求正常
        check.equal(resp["status_code"], 200)
        # 断言返回code码正常
        check.equal(resp["code"], 0)
        return resp

    def test_put_address(self):
        resp = self.address.api_put_address('tester', '19696969696', '北京市 东城区', '测试订单地址')
        check.equal(resp["status_code"], 200)
        check.equal(resp["data"]["status"], "success")
        return resp


if __name__ == '__main__':
    address = TestAddress()
    address.setup_class()
    address.test_get_address()
    address.test_put_address()
