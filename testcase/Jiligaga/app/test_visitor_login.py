"""
=========
Author:WenLing.xu
time:2022/7/6
=========
"""
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiligaga.app.ApiVisitorLogin import ApiVisitorLogin


@pytest.mark.GagaReg
class TestPhone:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        # 获取配置文件的手机号
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.apivisitorlogin = ApiVisitorLogin()

    def test_visitor_login(self):
        """
        游客登录
        """
        resp = self.apivisitorlogin.visitor_login()
        check.equal(resp["code"], 0)
