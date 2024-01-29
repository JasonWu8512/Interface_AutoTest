"""
=========
Author:WenLing.xu
time:2022/7/6
=========
"""
import time
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3
from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiVisitorLogin import ApiVisitorLogin


@pytest.mark.GagaReg
class TestPhone:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        # 获取配置文件的手机号
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.apiAccountV3 = ApiAccountV3()
        cls.apiAccount = ApiAccount()
        cls.apivisitorlogin = ApiVisitorLogin()

    def test_create_account_mo(self):
        """
        创建游客账户
        澳门
        """
        resp = self.apiAccountV3.create_account(countryCode="mo")
        check.equal(resp["code"], 0)

    def test_create_account_tw(self):
        """
        创建游客账户
        台湾
        """
        resp = self.apiAccountV3.create_account(countryCode="tw")
        check.equal(resp["code"], 0)

    def test_create_account_hk(self):
        """
        创建游客账户
        香港
        """
        resp = self.apiAccountV3.create_account(countryCode="hk")
        check.equal(resp["code"], 0)

    def test_create_account_th(self):
        """
        创建游客账户
        泰国
        """
        resp = self.apiAccountV3.create_account(countryCode="th")
        check.equal(resp["code"], 0)

    def test_phone_login_password(self):
        """
        密码登录/注册
        正确的手机号账号密码
        """
        resp = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_phone_login_error_password(self):
        """
        密码登录/注册
        正确手机号，密码错误
        """
        resp = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["phone"],
                                                countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'Incorrect phone number/password, please try again.')

    def test_mail_login_password(self):
        """
        密码登录/注册
        正确的邮箱账号密码
        """
        resp = self.apiAccountV3.login_password(phone=self.gaga_app["mail"], pwd=self.gaga_app["pwd"],
                                                countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_mail_login_error_password(self):
        """
        密码登录/注册
        正确邮箱，密码错误
        """
        resp = self.apiAccountV3.login_password(phone=self.gaga_app["mail"], pwd=self.gaga_app["phone"],
                                                countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'Incorrect email address/password, please try again.')

    def test_phone_login_send_code(self):
        """
        验证码登录/注册
        已注册的手机号
        """
        time.sleep(10)
        resp = self.apiAccountV3.login_send_code(account=self.gaga_app["phone"],
                                                 countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_unregistered_phone_login_send_code(self):
        """
        验证码登录/注册
        未注册的手机号
        """
        resp = self.apiAccountV3.login_send_code(account=self.gaga_app["phone01"],
                                                 countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_error_phone_login_send_code(self):
        """
        验证码登录/注册
        错误格式的手机号
        """
        resp = self.apiAccountV3.login_send_code(account=self.gaga_app["pwd"], countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'Incorrect phone number. Please try again.')

    def test_mail_login_send_code(self):
        """
        验证码登录/注册
        已注册的邮箱
        """
        resp = self.apiAccountV3.login_send_code(account=self.gaga_app["mail"],
                                                 countrycode=self.gaga_app["countryCodeTh"])
        check.equal(resp["code"], 0)

    def test_unregistered_mail_login_send_code(self):
        """
        验证码登录/注册
        未注册的邮箱
        """
        resp = self.apiAccountV3.login_send_code(account=self.gaga_app["mail01"],
                                                 countrycode=self.gaga_app["countryCodeTh"])
        check.equal(resp["code"], 0)

    def test_error_mail_login_send_code(self):
        """
        验证码登录/注册
        错误格式的邮箱
        """
        resp = self.apiAccountV3.login_send_code(account=self.gaga_app["errormail"],
                                                 countrycode=self.gaga_app["countryCodeTh"])
        check.equal(resp["msg"], 'Please enter a valid email address.')

    def test_phone_login_validate_code(self):
        """
        验证码登录-校验验证码
        正确的手机验证码
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone"], countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone"], code=code,
                                                     countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_twphone_login_validate_code(self):
        """
        验证码登录-校验验证码
        正确的手机验证码
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone"], countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone"], code=code,
                                                     countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_mail_login_validate_code(self):
        """
        验证码登录-校验验证码
        正确的邮箱验证码
        """
        # 获取邮箱验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["mail"], countrycode=self.gaga_app["countryCodeTh"])
        # return验证码F
        code = self.apiAccount.return_phone_code(mail=self.gaga_app["mail"])
        # 验证码登录
        resp = self.apiAccountV3.login_validate_code(account=self.gaga_app["mail"], code=code,
                                                     countrycode=self.gaga_app["countryCodeTh"])
        check.equal(resp["code"], 0)

    def test_mail_login_validate_error_code(self):
        """
        验证码登录-校验验证码
        错误的邮箱验证码
        """
        # 验证码登录
        resp = self.apiAccountV3.login_validate_code(account=self.gaga_app["mail"], code="123",
                                                     countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'Verification code error, please try again.')

    def test_phone_login_validate_error_code(self):
        """
        验证码登录-校验验证码
        错误的手机号验证码
        """
        # 验证码登录
        resp = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone"], code="123",
                                                     countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'Verification code error, please try again.')

    def test_phone_forgit_reset_code(self):
        """
        忘记密码第1步-发送验证码
        输入已注册的手机号
        """
        resp = self.apiAccountV3.forget_send_code(account=self.gaga_app["phone"],
                                                  countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_un_phone_forgit_reset_code(self):
        """
        忘记密码第1步-发送验证码
        输入未注册的手机号
        """
        resp = self.apiAccountV3.forget_send_code(account=self.gaga_app["phone01"],
                                                  countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'The phone number is not linked to any existing account.')

    def test_error_phone_forgit_reset_code(self):
        """
        忘记密码第1步-发送验证码
        输入格式错误的手机号
        """
        resp = self.apiAccountV3.forget_send_code(account=self.gaga_app["pwd"],
                                                  countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'Incorrect phone number. Please try again.')

    def test_mail_forgit_reset_code(self):
        """
        忘记密码第1步-发送验证码
        输入已注册的邮箱
        """
        resp = self.apiAccountV3.forget_send_code(account=self.gaga_app["mail"],
                                                  countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_un_mail_forgit_reset_code(self):
        """
        忘记密码第1步-发送验证码
        输入未注册的邮箱
        """
        resp = self.apiAccountV3.forget_send_code(account=self.gaga_app["mail01"],
                                                  countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'This email is not linked to any existing account.')

    def test_error_mail_forgit_reset_code(self):
        """
        忘记密码第1步-发送验证码
        输入未注册的邮箱
        """
        resp = self.apiAccountV3.forget_send_code(account=self.gaga_app["mail01"],
                                                  countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'This email is not linked to any existing account.')

    def test_forget_validate_code(self):
        """
        忘记密码第2步-验证验证码
        输入正确的验证码
        """
        # 发送获取验证码
        self.apiAccountV3.forget_send_code(account=self.gaga_app["phone"], countrycode=self.gaga_app["countryCodeTw"])
        # 获取验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone"], country=self.gaga_app["countrytw"])
        # 验证验证码
        resp = self.apiAccountV3.forget_validate_code(account=self.gaga_app["phone"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["code"], 0)

    def test_forget_validate_error_code(self):
        """
        忘记密码第2步-验证验证码
        输入错误的验证码
        """
        resp = self.apiAccountV3.forget_validate_code(account=self.gaga_app["phone"], code="111",
                                                      countrycode=self.gaga_app["countryCodeTw"])
        check.equal(resp["msg"], 'Verification code error, please try again.')

    def test_forget_reset_password(self):
        """
        忘记密码第3步-重置密码
        输入新的密码
        """
        #   获取token
        #  忘记密码第1步-发送验证码
        self.apiAccountV3.forget_send_code(account=self.gaga_app["phone02"], countrycode=self.gaga_app["countryCodeTw"])
        #  忘记密码第2步-验证验证码,获取token
        self.token = (self.apiAccountV3.forget_validate_code(account=self.gaga_app["phone02"],
                                                             code=self.apiAccount.return_phone_code(
                                                                 phone=self.gaga_app["phone02"],
                                                                 country=self.gaga_app["countrytw"]),
                                                             countrycode=self.gaga_app["countryCodeTw"]))["data"][
            "token"]
        print(self.token)
        resp = self.apiAccountV3.forget_reset_password(password=self.gaga_app["pwd"],
                                                       confirmpassword=self.gaga_app["pwd"],
                                                       token=self.token, password01=self.gaga_app["pwd01"],
                                                       confirmpassword01=self.gaga_app["pwd01"])
        check.equal(resp["code"], 0)

    def test_forget_reset_old_password(self):
        """
        忘记密码第3步-重置密码
        输入旧的密码
        """
        #   获取token
        #  忘记密码第1步-发送验证码
        self.apiAccountV3.forget_send_code(account=self.gaga_app["phone"], countrycode=self.gaga_app["countryCodeTw"])
        #  忘记密码第2步-验证验证码,获取token
        self.token = (self.apiAccountV3.forget_validate_code(account=self.gaga_app["phone"],
                                                             code=self.apiAccount.return_phone_code(
                                                                 phone=self.gaga_app["phone"],
                                                                 country=self.gaga_app["countrytw"]),
                                                             countrycode=self.gaga_app["countryCodeTw"]))["data"]["token"]
        resp = self.apiAccountV3.forget_reset_password(password=self.gaga_app["pwd"],
                                                       confirmpassword=self.gaga_app["pwd"],
                                                       password01=self.gaga_app["pwd"],
                                                       confirmpassword01=self.gaga_app["pwd"],
                                                       token=self.token)
        check.equal(resp["msg"], 'Your new password cannot be the same as the current one.')
