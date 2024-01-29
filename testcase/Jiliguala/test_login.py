# coding=utf-8
# @Time    : 2020/8/6 1:07 下午
# @Author  : keith
# @File    : testLogin

import pytest
import pytest_check as check

from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains


@pytest.mark.user
class TestLogin(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path('dev')
        # 设置域名host
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        print(111)

    def test_login(self):
        resp = self.user.api_login(typ="mobile", u=self.config['account']['mobile'], p=self.config['account']['pwd'])
        check.equal(resp["status_code"], 200)
        check.equal(resp["data"]["mobile"], "13818207214")
        check.equal(resp["data"]["typ"], "mobile")


if __name__ == '__main__':
    login = TestLogin()
    login.setup_class()
    login.test_login()
