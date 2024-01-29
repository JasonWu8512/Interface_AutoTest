# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/7/6 4:24 下午
@Author   : Anna
@File     : test_circulars.py
"""
import json

from business.Jiliguala.pay.ApiCirculars import ApiCirculars
from config.env.domains import Domains
from business.Jiliguala.user.ApiUser import ApiUser
import pytest
import pytest_check as check


@pytest.mark.pay
class TestCirculars(object):
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
        cls.token = user.get_token(typ="mobile", u="15921263812", p="123456")
        # 获取版本信息
        cls.version = cls.config['version']['ver11.0']
        # 实例化测试类
        cls.circulars = ApiCirculars(cls.token, cls.version)

    # @pytest.mark.skip
    def test_post_redeem(self):
        """生成兑换码"""
        resp = self.circulars.api_post_redeem("L0XX", "test", 1)
        check.equal(resp["status_code"], 200)
        # 断言生成的itemid是L0XX
        check.equal(resp["data"]["itemid"], "L0XX")
        # 断言生成了1条数据
        check.equal(resp["data"]["num"], 1)
        code = resp["data"]["code"]
        print(code)

    # @pytest.mark.skip
    def test_post_refund(self):
        """兑换码注销"""
        # 生成兑换码
        resp = self.circulars.api_post_redeem("L0XX", "test", 1)
        # 拿到兑换码
        code = resp["data"]["code"][0]
        # print(code)
        # 将取得的兑换码，当成参数，注销
        resp01 = self.circulars.api_post_refund(code)
        # print(resp01)
        # 断言接口正常返回
        check.equal(resp01["code"], 0)
        # 接口正常注销
        check.equal(resp01["data"], True)


if __name__ == '__main__':
    circulars = TestCirculars()
    circulars.setup_class()
    circulars.test_post_redeem()
    circulars.test_post_refund()
