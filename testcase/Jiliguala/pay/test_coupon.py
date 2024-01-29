# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/7/9 6:36 下午
@Author   : Anna
@File     : test_coupon.py
"""
from business.Jiliguala.pay.ApiCoupon import ApiCoupon
from business.Jiliguala.user.ApiUser import ApiUser
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
import pytest_check as check
import pytest


@pytest.mark.pay
class TestCoupon(object):
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
        cls.token = user.get_token(typ="mobile", u="19898989871", p="123456")
        # 获取版本信息
        cls.version = cls.config['version']['ver11.0']
        # 实例化测试类
        cls.coupon = ApiCoupon(cls.token, cls.version)

    # @pytest.mark.skip
    def test_get_couponList(self):
        """
        老版本家长中心-优惠券列表接口
        user="19898989871"
        优惠券=1张
        """
        resp = self.coupon.api_get_couponList("available", "0", "825d31937e04494b80a2eae6c95a9dd4")
        # 查询未使用优惠券，断言接口返回正常
        check.equal(resp["code"], 0)

        # 断言已过期的有1个优惠券
        resp01 = self.coupon.api_get_couponList("expired", "0", "825d31937e04494b80a2eae6c95a9dd4")
        check.equal(resp01["data"][0]["amount"], 10000)

        # 查询已使用优惠券，断言接口返回正常
        resp02 = self.coupon.api_get_couponList("available", "0", "825d31937e04494b80a2eae6c95a9dd4")
        check.equal(resp02["code"], 0)

    # @pytest.mark.skip
    def test_get_coupon(self):
        """
        新版本家长中心-优惠券列表接口
        user="19898989871"
        优惠券=1张
        """
        resp = self.coupon.api_get_coupon("available", "0", "825d31937e04494b80a2eae6c95a9dd4")
        print(resp)
        # 查询未使用优惠券，断言接口返回正常
        check.equal(resp["code"], 0)

        # 断言已过期的有1个优惠券
        resp01 = self.coupon.api_get_coupon("expired", "0", "825d31937e04494b80a2eae6c95a9dd4")
        check.equal(resp01["data"]["list"][0]["amount"], 10000)

        # 查询已使用优惠券，断言接口返回正常
        resp02 = self.coupon.api_get_coupon("available", "0", "825d31937e04494b80a2eae6c95a9dd4")
        check.equal(resp02["code"], 0)


if __name__ == '__main__':
    coupon = TestCoupon()
    coupon.test_get_couponList()
    coupon.test_get_coupon()
