"""
=========
Author:WenLing.xu
time:2022/10/24
=========
"""
import pytest
import pytest_check as check
import time
from config.env.domains import Domains
from business.Jiligaga.app.ApiRedeem import ApiRedeem
from business.Jiligaga.app.ApiLogin import Login
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth
from business.Jiligaga.app.ApiVisitorLogin import ApiVisitorLogin
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3


@pytest.mark.GagaReg
class TestApiTradeOrderCreate:
    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        # 获取配置文件的手机号
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.sso = cls.dm.set_env_path('fat')["sso"]
        cls.a_host = cls.dm.set_env_path("fat")["url"]
        cls.apiredeem = ApiRedeem()
        cls.login = Login()
        cls.apivisitorlogin = ApiVisitorLogin()
        cls.apiadminauth = ApiAdminAuth()
        cls.apiAccountV3 = ApiAccountV3()

    def test_api_redeem_getlist(self):
        """兑换记录查询"""
        # 获取token
        authorization = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                         countrycode=self.gaga_app["countryCodeTw"])["data"][
            "auth"]
        print(authorization)
        self.apiredeem = ApiRedeem(token=authorization)
        resp = self.apiredeem.api_redeem_getlist()
        check.equal(resp["code"], 0)

    def test_api_redeem_redeeming(self):
        """输入有效的的兑换码兑换"""
        t = int(round(time.time() * 1000))
        t1 = t + 100000
        # 获取商城后台token
        a_token = self.apiadminauth.api_login(username=self.sso["email"], password=self.sso["pw"])["data"][
            "token"]
        print(a_token)
        # 获取兑换码
        self.apiredeem = ApiRedeem(token=a_token)
        print(self.apiredeem)
        redeemNo = self.apiredeem.redeeming(startTime=t, expireTime=t1)["data"][0]
        # 获取游客token
        authorization = self.apivisitorlogin.visitor_login()["data"]["auth"]
        print(authorization)
        self.apiredeem = ApiRedeem(token=authorization)
        # 兑换码兑换
        resp = self.apiredeem.api_redeem_redeeming(redeemNo=redeemNo)["msg"]
        print(resp)
        check.equal(resp, 'Redemption successful! Ready to embark on a wonderful journey?')

    def test_api_redeem_errorredeeming(self):
        """输入错误的兑换码兑换"""
        # 获取token
        authorization = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                         countrycode=self.gaga_app["countryCodeTw"])["data"][
            "auth"]
        self.apiredeem = ApiRedeem(token=authorization)

        resp = self.apiredeem.api_redeem_redeeming(redeemNo="12344")
        check.equal(resp["msg"], "Oops! The code doesn't exist. Please enter a valid one.")
