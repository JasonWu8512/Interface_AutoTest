"""
=========
Author:Lisa
time:2022/8/01 2:00 下午
=========
"""

import pytest
import pytest_check as check
from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiBabyCreate import ApiBabyCreate
from business.Jiligaga.app.ApiLogin import Login
from config.env.domains import Domains
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3


@pytest.mark.GagaReg
class TestBabyCreate:
    dm = Domains

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.dm = Domains()
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.login = Login()
        cls.apiBabyCreate = ApiBabyCreate()
        cls.apiAccountV3 = ApiAccountV3()
        cls.apiAccount = ApiAccount()

    """
        宝贝管理-添加宝贝
    """

    def test_baby_create(self):
        """
        添加宝贝

        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone01"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone01"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone01"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        # 获取token
        authorization = resp1["data"]["auth"]
        self.apiBabyCreate = ApiBabyCreate(token=authorization)
        resp = self.apiBabyCreate.baby_create(birth=self.gaga_app["birth"], nick=self.gaga_app["nick"])
        check.equal(resp["code"], 0)
        """注销-人转用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_baby_create_error(self):
        """
        添加宝贝-缺少auth

        """

        resp = self.apiBabyCreate.baby_create(birth=self.gaga_app["birth"], nick=self.gaga_app["nick"])
        check.equal(resp["code"], 103)
