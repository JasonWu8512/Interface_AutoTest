"""
=========
Author:Lisa
time:2022/8/01 2:00 下午
=========
"""

import pytest
import pytest_check as check
from business.Jiligaga.app.ApiBabyCreate import ApiBabyCreate
from business.Jiligaga.app.ApiBabyDelete import ApiBabyDelete
from business.Jiligaga.app.ApiLogin import Login
from config.env.domains import Domains
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3
from business.Jiligaga.app.ApiAccount import ApiAccount


@pytest.mark.GagaReg
class TestBabyDelete:
    dm = Domains

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.dm = Domains()
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.login = Login()
        cls.apiAccountV3 = ApiAccountV3()
        cls.apiAccount = ApiAccount()

    """
        删除存在的baby
    """

    def test_baby_delete(self):
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
        bid = self.apiBabyCreate.baby_create(birth=self.gaga_app["birth"], nick=self.gaga_app["nick"])["data"][
            "bid"]
        apiBabyDelete = ApiBabyDelete(authorization)
        resp = apiBabyDelete.baby_delete(bid)
        check.equal(resp["code"], 0)
        """注销-人转用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    """
        删除不存在的babyid
    """

    def test_errorbaby_delete(self):
        token = self.apiAccountV3.login_password(phone=self.gaga_app["phone02"], pwd=self.gaga_app["pwd"],
                                                 countrycode=self.gaga_app["countryCodeTw"])
        if token["code"] == 50125:
            token = self.apiAccountV3.login_password(phone=self.gaga_app["phone02"], pwd=self.gaga_app["pwd01"],
                                                     countrycode=self.gaga_app["countryCodeTw"])["data"][
                "auth"]
            apiBabyDelete = ApiBabyDelete(token)
            resp = apiBabyDelete.baby_delete(bid=self.gaga_app["bid"])
            check.equal(resp["code"], 50201)
        else:
            apiBabyDelete = ApiBabyDelete(token["data"][
                                              "auth"])
            resp = apiBabyDelete.baby_delete(bid=self.gaga_app["bid"])
            check.equal(resp["code"], 50201)
