# coding=utf-8
# @Time    :
# @Author  : anna

import pytest
import pytest_check as check
import hypothesis
import time

from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.businessQuery import usersQuery
from config.env.domains import Domains
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.Login
class TestSms(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.config = cls.dm.set_env_path('prod')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化用户
        user = ApiUser()
        # 获取用户token信息
        cls.token = user.get_token(typ="mobile", u="19898989831", p="123456")
        # 实例化ApiSmsInfo类
        cls.sms = ApiSmsInfo(cls.token)
        cls.mobile = '19898989831'
        # 获取配置文件中的pandora信息
        cls.pandora = cls.config['onboarding']['pandora']
        # @pytest.mark.skip

    def test_put_guest(self):
        """游客登陆"""
        resp = self.sms.api_put_guest()
        print(resp)
        # 断言游客，可正常登陆
        check.equal(resp['code'], 0)

    # @pytest.mark.skip
    def test_get_login_correct(self):
        """正确手机号，可发送验证码"""
        resp01 = self.sms.api_get_login_v2(self.mobile)
        print(resp01)
        check.equal(resp01['code'], 0)

    def test_get_login_fail(self):
        """短时间内频繁发送验证码，不可发送"""
        resp01 = self.sms.api_get_login_v2(self.mobile)
        print(resp01)
        # 断言，提示操作频率过快，请稍后重试
        check.equal(resp01['msg'], '操作频率过快，请稍后重试')

    # 线上数据库无法查询
    # def test_post_login_success(self):
    #     """输入正确验证码，可登陆成功"""
    #     # pandora = "MTY1NTc5MzQ2NDIwODoyMDIwMDUxNDE1MDgxOWUzOWU2YzExMDNlYzExZTA0NTg4ODY4ZDY2MDM4MWM3MDFiNmE4MjY3ZGM5MWJkNToxNzEzY2YwNzE2MmM2MzE5ZmRmOTNkYzFmYWVmMmEzYg=="
    #     pandora = self.pandora
    #     # 获取验证码
    #     code = usersQuery().get_users(mobile=self.mobile)["sms"]["code"]
    #     print(code)
    #     # 查数据库，获取uid
    #     uid = usersQuery().get_users(mobile=self.mobile)["_id"]
    #     resp02 = self.sms.api_post_login_v2(self.mobile, pandora, uid, code)
    #     print(resp02)
    #     # 断言，登陆成功
    #     check.equal(resp02['code'], 0)

    # 线上数据库无法查询
    # def test_post_login_fail(self):
    #     """输入错误验证码，登陆失败"""
    #     # pandora = "MTY1NTc5MzQ2NDIwODoyMDIwMDUxNDE1MDgxOWUzOWU2YzExMDNlYzExZTA0NTg4ODY4ZDY2MDM4MWM3MDFiNmE4MjY3ZGM5MWJkNToxNzEzY2YwNzE2MmM2MzE5ZmRmOTNkYzFmYWVmMmEzYg=="
    #     pandora = self.pandora
    #     code = "1234"
    #     print(code)
    #     # 查数据库，获取uid
    #     uid = usersQuery().get_users(mobile=self.mobile)["_id"]
    #     resp02 = self.sms.api_post_login_v2(self.mobile, pandora, uid, code)
    #     print(resp02)
    #     # 断言，登陆失败，提示验证码错误
    #     check.equal(resp02['msg'], "验证码错误")

    def test_get_password_success(self):
        """输入正确密码，可登陆成功"""
        resp03 = self.sms.api_get_password("123456", "mobile", self.mobile)
        print(resp03)
        # 断言，登陆成功
        check.equal(resp03['code'], 0)

    def test_get_password_fail(self):
        """输入错误密码，登陆失败"""
        resp03 = self.sms.api_get_password("124569", "mobile", self.mobile)
        print(resp03)
        # 断言，登陆成功
        check.equal(resp03['msg'], '邮箱/手机号码或密码不正确，请重试')


# if __name__ == '__main__':
#     sms = TestSms()
#     sms.setup_class()
#     # 游客登陆
#     sms.test_put_guest()
#     # 发送验证码
#     sms.test_get_login_correct()
#     # sms.test_get_login_fail()
#     # 验证码登陆
#     time.sleep(60)
#     sms.test_post_login_success()
#     time.sleep(60)
#     sms.test_post_login_fail()
#     # 密码登陆
#     sms.test_get_password_success()
#     sms.test_get_password_fail()
