# coding=utf-8
import pytest
import pytest_check as check

from business.Reading.user.ApiUser import ApiUser
from config.env.domains import Domains


@pytest.mark.reg
class TestUser(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])
        cls.user = ApiUser()

    def test_login(self):
        """01.手机号-密码登录"""
        resp = self.user.api_login(typ="mobile", u=self.config['reading_account']['user'],
                                   p=self.config['reading_account']['pwd'])
        check.equal(resp["code"], 0)
        #check.equal(resp["data"]["mobile"], "13162592038")
        check.equal(resp["data"]["typ"], "mobile")
