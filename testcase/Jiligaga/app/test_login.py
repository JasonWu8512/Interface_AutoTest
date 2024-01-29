"""
=========
Author:WenLing.xu
time:2022/7/6
=========
"""
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiligaga.app.ApiLogin import Login
from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3
from business.mysqlQuery import HwQuery


@pytest.mark.GagaReg
class TestPhone:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('fat')
        cls.dm = Domains()
        cls.db = HwQuery()
        # 获取配置文件的手机号
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.login = Login()
        cls.apiaccount = ApiAccount()
        cls.apiAccountV3 = ApiAccountV3()

    # def test_phone_pwd_login(self):
    #     """
    #     手机号密码登录
    #     正确手机号正确密码
    #     已下线
    #     """
    #     resp = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone"])
    #     check.equal(resp["code"], 0)

    # def test_phone_errorpwd_login(self):
    #     """
    #     手机号密码登录（已下线）
    #     正确手机号,错误密码
    #     """
    #     resp = self.login.phone_pwd_login(pwd="12345", phone=self.gaga_app["phone"])
    #     check.equal(resp["msg"], 'Incorrect phone number/password, please try again.')

    # def test_errorphone_pwd_login(self):
    #     """
    #     手机号密码登录（强更之后接口没用了）
    #     错误手机号,正确密码
    #     """
    #     resp = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone01"])
    #     check.equal(resp["msg"], 'Incorrect phone number/password, please try again.')

    def test_mail_pwd_login(self):
        """
        邮箱密码登录
        正确邮箱,正确密码
        """
        resp = self.login.mail_pwd_login(pwd=self.gaga_app["pwd"], mail=self.gaga_app["qq"])
        check.equal(resp["code"], 0)

    def test_errormail_pwd_login(self):
        """
        邮箱密码登录
        错误邮箱,正确密码
        """
        resp = self.login.mail_pwd_login(pwd=self.gaga_app["pwd"], mail=self.gaga_app["errormail"])
        check.equal(resp["msg"], 'Incorrect email address/password, please try again.')

    def test_mail_errorpwd_login(self):
        """
        邮箱密码登录
        正确邮箱,错误密码
        """
        resp = self.login.mail_pwd_login(pwd="123456", mail=self.gaga_app["qq"])
        check.equal(resp["msg"], 'Incorrect email address/password, please try again.')

    # def test_code_login(self):
    #     """
    # 调用的发送验证码的接口已下线
    #     验证码登录
    #     正确的验证码，成功登录
    #     """
    #     resp = self.login.login_getcode(region="86", phone=self.gaga_app["phone"])
    #     getcode = self.apiaccount.return_phone_code(phone=self.gaga_app["phone"], country=self.gaga_app["countrycn"])
    #     # print(getcode)
    #     resp = self.login.code_login(code=getcode, phone=self.gaga_app["phone"])
    #     check.equal(resp["code"], 0)

    # def test_errorcode_login(self):
    #     """
    #     验证码登录：（强更之后接口没用了）
    #     错误的验证码，toast提示：
    #     """
    #     resp = self.login.code_login(code="000", phone=self.gaga_app["phone"])
    #     check.equal(resp["msg"], 'Verification code error, please try again.')

    def test_phone_login_getcode(self):
        """
        登录-发送验证码
        输入正确的手机号验证获取验证码
        """
        # resp = self.login.login_getcode(region="86", phone=self.gaga_app["phone"])
        resp = self.apiAccountV3.login_send_code(countrycode=self.gaga_app["countryCodeTw"],
                                                 account=self.gaga_app["phone"])
        check.equal(resp["code"], 0)

    # def test_mail_login_getcode(self):
    #     """
    #     登录-发送验证码
    #     输入正确的邮箱获取验证码
    #     """
    #     # resp = self.login.login_getcode(mail=self.gaga_app["mail"])
    #     resp = self.apiAccountV3.login_send_code(account=self.gaga_app["mail"])
    #     print(resp)
    #     check.equal(resp["code"], 0)

    # def test_get_user_info(self):
    #     """
    #     获取当前登陆用户信息（强更之后接口没用了）
    #     """
    #     authorization = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone"])["data"][
    #         "auth"]
    #     resp = self.login.getMyInfo(authorization=authorization)
    #     print(resp)
    #     check.equal(resp["code"], 0)
