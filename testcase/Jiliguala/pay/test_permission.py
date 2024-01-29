# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/7/6 1:58 下午
@Author   : Anna
@File     : test_permission.py
"""
from business.Jiliguala.pay.ApiPermission import ApiPermission
from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains
import pytest
import pytest_check as check


@pytest.mark.pay
class TestPermission(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.config = cls.dm.set_env_path("fat")
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化用户
        user = ApiUser()
        # 获取用户token信息
        cls.token = user.get_token(typ="mobile", u="19393123455", p="123456")
        cls.version = cls.config['version']['ver11.0']
        # 实例化ApiPermission类
        cls.permission = ApiPermission(cls.token, cls.version)

    def test_permission(self):
        resp = self.permission.api_get_permission("c_type_h5")
        # 断言用户有购买权限，返回正常
        check.equal(resp["data"]["hasPermission"], True)


if __name__ == '__main__':
    permission = TestPermission()
    permission.setup_class()
    permission.test_permission()
