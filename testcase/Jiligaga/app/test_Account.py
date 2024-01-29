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
from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiVisitorLogin import ApiVisitorLogin


@pytest.mark.GagaReg
class TestPhone:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        #获取配置文件的手机号
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.apiaccount = ApiAccount()
        cls.apivisitorlogin = ApiVisitorLogin()

    def test_query_error_phone(self):
        """
        查询手机号使用状态
        输入错误的手机号验证获取验证码
        """
        resp = self.apiaccount.query_phone(region=self.gaga_app["countrytw"], phone=self.gaga_app["pwd"])
        check.equal(resp["data"]["errorMsg"], 'Incorrect phone number. Please try again.')

    def test_query_registered_phone(self):
        """
        查询手机号使用状态
        输入已注册的手机号验证获取验证码
        """
        resp = self.apiaccount.query_phone(region=self.gaga_app["countrytw"], phone=self.gaga_app["phone"])
        check.equal(resp["code"], 0)

    def test_query_unregistered_phone(self):
        """
        查询手机号使用状态
        输入未注册的手机号验证获取验证码
        """
        resp = self.apiaccount.query_phone(region=self.gaga_app["countrytw"], phone=self.gaga_app["phone01"])
        check.equal(resp["data"]["errorMsg"], 'The phone number is not linked to any existing account.')

    def test_query_nonsupport_zone(self):
        """
        查询手机号使用状态
        输入不支持的区号验证获取验证码
        """
        resp = self.apiaccount.query_phone(region="355", phone=self.gaga_app["phone"])
        check.equal(resp["data"]["errorMsg"], "Sorry, the service is not available in your region yet.")

    def test_query_error_mail(self):
        """
        查询邮箱使用状态
        输入错误格式的邮箱获取验证码
        """
        resp = self.apiaccount.query_mail(mail=self.gaga_app["phone"])
        check.equal(resp["data"]["errorMsg"], 'Please enter a valid email address.')

    def test_query_registered_mail(self):
        """
        查询邮箱使用状态
        输入已注册的邮箱获取验证码
        """
        resp = self.apiaccount.query_mail(mail=self.gaga_app["mail"])
        check.equal(resp["code"], 0)

    def test_query_unregistered_mail(self):
        """
        查询邮箱使用状态
        输入未注册的邮箱获取验证码
        """
        resp = self.apiaccount.query_mail(mail=self.gaga_app["mail01"])
        check.equal(resp["data"]["errorMsg"], 'This email is not linked to any existing account.')

    def test_register_unregistered_getcode(self):
        """
        注册-发送码验证
        输入未注册的手机号获取验证码
        """
        time.sleep(10)
        resp = self.apiaccount.register_getcode(country=self.gaga_app["countrytw"],
                                                countryCode=self.gaga_app["countryCodeTw"],
                                                languageCode=self.gaga_app["languageCodetw"],
                                                phone01=self.gaga_app["phone01"])
        check.equal(resp["code"], 0)

    def test_query_registered_phone_mail(self):
        """
        验证邮箱/手机是否已使用，返回0表示已使用
        输入已注册的手机号获取验证码
        """
        resp = self.apiaccount.query_phone_mail(country=self.gaga_app["countrytw"], phone=self.gaga_app["phone"])
        check.equal(resp["code"], 0)

    def test_query_unregisteredphone_mail(self):
        """
        验证邮箱/手机是否已使用，返回0表示已使用
        输入未注册的邮箱获取验证码
        """
        resp = self.apiaccount.query_phone_mail(country=self.gaga_app["countrytw"], phone=self.gaga_app["phone01"])
        check.equal(resp["msg"], 'The phone number is not linked to any existing account.')

    def test_query_level(self):
        """
        查询推荐级别
        宝贝昵称不为空
        """
        resp = self.apiaccount.query_level(birthdesc="2015-06", nick="宝贝")
        check.equal(resp["code"], 0)

    def test_phone_send_code(self):
        """
        忘记密码第1步-发送验证码
        输入正确的手机号发送验证码
        """
        resp = self.apiaccount.send_code(country=self.gaga_app["countrytw"], phone=self.gaga_app["phone"])
        check.equal(resp["code"], 0)

    def test_validate(self):
        """
        忘记密码第2步-验证验证码
        输入正确的手机号发送验证码
        """
        self.apiaccount.send_code(country=self.gaga_app["countrytw"], phone=self.gaga_app["phone02"])
        resp = self.apiaccount.validate(country=self.gaga_app["countrytw"], phone02=self.gaga_app["phone02"],
                                        code=self.apiaccount.return_phone_code(phone=self.gaga_app["phone02"],
                                                                               country=self.gaga_app["countrytw"]))
        check.equal(resp["code"], 0)

    def test_reset_password(self):
        """
        忘记密码第3步-重置密码
        输入新的密码
        """
        #   获取token
        #  忘记密码第1步-发送验证码
        time.sleep(10)
        self.apiaccount.send_code(country=self.gaga_app["countrytw"], phone=self.gaga_app["phone02"])
        #  忘记密码第2步-验证验证码,获取token
        self.token = (self.apiaccount.validate(country=self.gaga_app["countrytw"], phone02=self.gaga_app["phone02"],
                                               code=self.apiaccount.return_phone_code(phone=self.gaga_app["phone02"],
                                                                                      country=self.gaga_app[
                                                                                          "countrytw"])))[
            "data"][
            "token"]
        print(self.token)
        resp = self.apiaccount.reset_password(password=self.gaga_app["pwd"], confirmpassword=self.gaga_app["pwd"],
                                              token=self.token, password01=self.gaga_app["pwd01"],
                                              confirmpassword01=self.gaga_app["pwd01"])
        check.equal(resp["code"], 0)

    def test_close_account(self):
        """
        用户销户
        """
        token = self.apivisitorlogin.visitor_login()["data"]["auth"]
        print(token)
        resp = self.apiaccount.close_account(token=token)
        check.equal(resp["code"], 0)

    def test_error_code_validate(self):
        """
        注册-验证验证码
        输入错误的验证码
        """
        resp = self.apiaccount.register_validate(country=self.gaga_app["countrytw"],
                                                 countryCode=self.gaga_app["countryCodeTw"],
                                                 languageCode=self.gaga_app["languageCodetw"],
                                                 code="000000", phone=self.gaga_app["phone01"])
        check.equal(resp["msg"], 'Verification code error, please try again.')

    def test_code_validate(self):
        """
        注册-验证验证码
        输入正确的验证码
        """
        #  发送验证码
        self.apiaccount.register_getcode(country=self.gaga_app["countrytw"],
                                         countryCode=self.gaga_app["countryCodeTw"],
                                         languageCode=self.gaga_app["languageCodetw"],
                                         phone01=self.gaga_app["phone01"])
        #  return验证码
        code = self.apiaccount.return_phone_code(phone=self.gaga_app["phone01"], country=self.gaga_app["countrytw"])
        resp = self.apiaccount.register_validate(country=self.gaga_app["countrytw"],
                                                 countryCode=self.gaga_app["countryCodeTw"],
                                                 languageCode=self.gaga_app["languageCodetw"], code=code,
                                                 phone=self.gaga_app["phone01"])
        #  此手机号用户注销
        token = resp["data"]["auth"]
        self.apiaccount.close_account(token=token)
        # 验证码验证断言
        check.equal(resp["code"], 0)

    def test_bind_phone_send_code(self):
        """
        绑定-发送手机/邮箱验证码
        输入已绑定的手机号
        """
        resp = self.apiaccount.bind_send_code(phone=self.gaga_app["phone"], areaCode=self.gaga_app["countrytw"])
        check.equal(resp["msg"], 'Oops! This phone number has already been taken.')

    def test_not_bind_phone_send_code(self):
        """
        绑定-发送手机/邮箱验证码
        输入未绑定的手机号
        """
        resp = self.apiaccount.bind_send_code(phone=self.gaga_app["phone01"], areaCode=self.gaga_app["countrytw"])
        check.equal(resp["code"], 0)

    def test_error_phone_send_code(self):
        """
        绑定-发送手机/邮箱验证码
        输入格式错误的手机号
        """
        resp = self.apiaccount.bind_send_code(phone=self.gaga_app["pwd"], areaCode=self.gaga_app["countrytw"])
        check.equal(resp["msg"], 'Incorrect phone number. Please try again.')

    def test_not_bind_mail_send_code(self):
        """
        绑定-发送手机/邮箱验证码
        输入未绑定的邮箱
        """
        resp = self.apiaccount.bind_send_code(mail=self.gaga_app["mail01"])
        check.equal(resp["code"], 0)

    def test_bind_mail_send_code(self):
        """
        绑定-发送手机/邮箱验证码
        输入已绑定的邮箱
        """
        resp = self.apiaccount.bind_send_code(mail=self.gaga_app["mail"])
        check.equal(resp["msg"], 'Oops! This email has already been taken.')

    def test_error_bind_mail_send_code(self):
        """
        绑定-发送手机/邮箱验证码
        输入格式错误的邮箱
        """
        resp = self.apiaccount.bind_send_code(mail=self.gaga_app["phone"])
        check.equal(resp["msg"], 'Please enter a valid email address.')

    def test_set_password(self):
        """
        设置密码
        输入正确格式的密码
        """
        #  游客登录获取auth
        auth = self.apivisitorlogin.visitor_login()["data"]["auth"]
        #  设置密码
        resp = self.apiaccount.set_password(password=self.gaga_app["pwd"], confirmPassword=self.gaga_app["pwd"],
                                            auth=auth)
        check.equal(resp["code"], 0)
        #  注销此游客账户
        self.apiaccount.close_account(token=resp["data"]["auth"])

    def test_set_error_password(self):
        """
        设置密码
        输入错误格式的密码
        """
        #  游客登录获取auth
        auth = self.apivisitorlogin.visitor_login()["data"]["auth"]
        #  设置密码
        resp = self.apiaccount.set_password(password=self.gaga_app["phone"], confirmPassword=self.gaga_app["phone"],
                                            auth=auth)
        check.equal(resp["msg"], 'The password must contain 8 to 16 characters')

    def test_bind_phone_validate_error_code(self):
        """
        验证code-绑定手机/邮箱
        输入错误的手机号验证码绑定
        """
        #  游客登录获取auth
        auth = self.apivisitorlogin.visitor_login()["data"]["auth"]
        #  验证code-绑定手机/邮箱
        resp = self.apiaccount.bind_phonemail_validate_code(areaCode=self.gaga_app["countrytw"],
                                                            phone=self.gaga_app["phone01"], code="0000",
                                                            auth=auth)
        check.equal(resp["msg"], 'Verification code error, please try again.')
        #  注销此游客账户
        self.apiaccount.close_account(token=auth)

    def test_bind_phone_validate_code(self):
        """
        验证code-绑定手机/邮箱
        输入正确的手机号验证码绑定
        """
        #  游客登录获取auth
        auth = self.apivisitorlogin.visitor_login()["data"]["auth"]
        #  发送验证码
        self.apiaccount.register_getcode(country=self.gaga_app["countrytw"], countryCode=self.gaga_app["countryCodeTw"],
                                         languageCode=self.gaga_app["languageCodetw"], phone01=self.gaga_app["phone01"])
        #  return验证码
        code = self.apiaccount.return_phone_code(phone=self.gaga_app["phone01"], country=self.gaga_app["countrytw"])
        """
        验证code-绑定手机/邮箱
        """
        print(auth)
        resp = self.apiaccount.bind_phonemail_validate_code(areaCode=self.gaga_app["countrytw"],
                                                            phone=self.gaga_app["phone01"], code=code,
                                                            auth=auth)
        check.equal(resp["code"], 0)
        #  注销此游客账户
        self.apiaccount.close_account(token=auth)

    def test_bind_mail_validate_code(self):
        """
        验证code-绑定手机/邮箱
        输入正确的邮箱验证码绑定
        """
        # 游客登录获取auth
        auth = self.apivisitorlogin.visitor_login()["data"]["auth"]
        # 发送验证码
        self.apiaccount.register_getcode(country=self.gaga_app["countrytw"], countryCode=self.gaga_app["countryCodeTw"],
                                         languageCode=self.gaga_app["languageCodetw"],mail=self.gaga_app["mail01"])
        # return验证码
        code = self.apiaccount.return_phone_code(mail=self.gaga_app["mail01"])
        # 验证code-绑定手机/邮箱
        resp = self.apiaccount.bind_phonemail_validate_code(mail=self.gaga_app["mail01"], code=code, auth=auth)
        check.equal(resp["code"], 0)
        # 注销此游客账户
        self.apiaccount.close_account(token=auth)

    def test_bind_mail_validate_error_code(self):
        """
        验证code-绑定手机/邮箱
        输入错误的邮箱验证码绑定
        """
        #  游客登录获取auth
        auth = self.apivisitorlogin.visitor_login()["data"]["auth"]
        #  验证code-绑定手机/邮箱
        print(auth)
        resp = self.apiaccount.bind_phonemail_validate_code(mail=self.gaga_app["mail01"], code="000", auth=auth)
        check.equal(resp["msg"], 'Verification code error, please try again.')
        #  注销此游客账户
        self.apiaccount.close_account(token=auth)
