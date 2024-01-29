# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/8/4 3:38 下午
@Author   : Anna
@File     : test_user.py
"""
from business.Jiliguala.magikabiz.ApiUser import ApiStoreUser
from config.env.domains import Domains
from business.Jiliguala.user.ApiUser import ApiUser
import pytest
import pytest_check as check


@pytest.mark.MagikBiz
class TestUser(object):
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
        cls.user = ApiStoreUser(cls.token, cls.version)

    # @pytest.mark.skip
    def test_get_trans(self):
        resp = self.user.api_get_trans('0', 'in')
        # 断言返回code码正常
        check.equal(resp["code"], 0)
        print(resp)
        # 断言页码
        check.equal(resp["data"]["pageNo"], 1)

        # 断言收入tab数据
        check.equal(resp["data"]["transactions"][0]["title"], "学习活动奖励")

        # 断言支出tab数据
        resp01 = self.user.api_get_trans('0', 'out')
        check.equal(resp01["data"]["transactions"][0]["title"], "魔石商城兑换商品")


if __name__ == '__main__':
    user = TestUser()
    user.setup_class()
    user.test_get_trans()
