# coding=utf-8
# @Time    :
# @Author  : anna
import os

import pytest
import pytest_check as check
import hypothesis
import time
import base64

from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.Jiliguala.onboarding.ApiUseronboarding import ApiUseronboarding
from business.Jiliguala.systemlesson.ApiHome import ApiHome
from business.businessQuery import usersQuery
from config.env.domains import Domains
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.Login
class TestSms(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        # env = os.environ.get('env')
        # 【代码提交用】获取环境变量
        # cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        # print(env)
        # 本地调试用
        cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        print(cls.config['url'])
        # 实例化用户
        user = ApiUser()
        # 获取用户token信息
        cls.token = user.get_token(typ="mobile", u="11100000001", p="123456")
        # 实例化ApiSmsInfo类
        cls.sms = ApiSmsInfo(cls.token)
        cls.mobile = '11100000001'
        # pandora 自动生成，根据当前时间戳:+固定字段然后base64加密
        current_timestamp = int(time.time() * 1000)
        auth_part = '2022090617204537dac25b2d811d716af3478aff70a2e70113ebf958de83b1:50b665b76488e1d3a565d3d05b63cc69'
        cls.pandora = base64.b64encode(f'{current_timestamp}:{auth_part}'.encode('utf-8'))
        print(current_timestamp)
        print(cls.pandora)
        cls.version = cls.config['version']['ver11.31.0']
        cls.agent = cls.config['User-Agent']['ios_11.31.0']
        cls.onboard = ApiUseronboarding(cls.version, cls.agent)
        # 宝贝年龄
        cls.birth = cls.config['regression']['birth']
        # 宝贝昵称
        cls.nick = cls.config['regression']['nick']

    # @pytest.mark.skip
    def test_put_guest(self):
        """游客登录"""
        guest = self.sms.api_put_guest()
        print(guest)
        # 断言游客，可正常登陆
        check.equal(guest['code'], 0)
        uid = guest['data']['_id']
        tok = guest['data']['tok']
        code = base64.b64encode(f'{uid}:{tok}'.encode('utf-8'))
        auth01 = 'Basic ' + str(code, encoding="utf-8")
        print("uid", uid)
        print("tok", tok)
        print("code", code)
        print("auth01", auth01)

        """ 选择年龄 """
        bd = self.onboard.api_user_onboarding(self.nick, self.birth, auth01)
        bid = bd['data']['_id']
        print(bid)
        # 断言接口返回成功
        check.equal(bd['code'], 0)

        """游客登录成功，检查首页，首页内容确认，展示体验营相关信息"""
        # 实例化首页，验证首页内容
        self.home = ApiHome(auth01)
        home = self.home.api_get_v4_home(bid)
        # 断言首页推荐的是英语体验营
        assert home['data']['roadmap']['elements'][1]['weekTitle'] == '体验营'

    # @pytest.mark.skip
    def test_get_login_correct(self):
        """正确手机号，可发送验证码"""
        resp01 = self.sms.api_get_login_v2(self.mobile, self.pandora)
        print(resp01)
        check.equal(resp01['code'], 0)

    def test_get_login_fail(self):
        """短时间内频繁发送验证码，不可发送"""
        resp01 = self.sms.api_get_login_v2(self.mobile, self.pandora)
        print(resp01)
        # 断言，提示操作频率过快，请稍后重试
        check.equal(resp01['msg'], '操作频率过快，请稍后重试')
        time.sleep(10)

    def test_post_login_success(self):
        """输入正确验证码，可登陆成功"""
        # pandora = "MTY1NTc5MzQ2NDIwODoyMDIwMDUxNDE1MDgxOWUzOWU2YzExMDNlYzExZTA0NTg4ODY4ZDY2MDM4MWM3MDFiNmE4MjY3ZGM5MWJkNToxNzEzY2YwNzE2MmM2MzE5ZmRmOTNkYzFmYWVmMmEzYg=="
        print(1, self.pandora)
        # 点击获取验证码
        resp01 = self.sms.api_get_login_v2(self.mobile, self.pandora)
        print(resp01)
        time.sleep(10)
        # 查询数据库，获取验证码
        code = usersQuery().get_users(mobile=self.mobile)["sms"]["code"]
        print(code)
        # 查数据库，获取uid
        uid = usersQuery().get_users(mobile=self.mobile)["_id"]
        print(uid)
        print(2, self.pandora)
        print(self.mobile)
        resp02 = self.sms.api_post_login_v2(self.mobile, self.pandora, uid, code)
        print(resp02)
        # 断言，登陆成功
        check.equal(resp02['code'], 0)

    def test_post_login_fail(self):
        """输入错误验证码，登陆失败"""
        # pandora = "MTY1NTc5MzQ2NDIwODoyMDIwMDUxNDE1MDgxOWUzOWU2YzExMDNlYzExZTA0NTg4ODY4ZDY2MDM4MWM3MDFiNmE4MjY3ZGM5MWJkNToxNzEzY2YwNzE2MmM2MzE5ZmRmOTNkYzFmYWVmMmEzYg=="
        pandora = self.pandora
        code = "1234"
        print(code)
        # 查数据库，获取uid
        uid = usersQuery().get_users(mobile=self.mobile)["_id"]
        resp02 = self.sms.api_post_login_v2(self.mobile, pandora, uid, code)
        print(resp02)
        # 断言，登陆失败，提示验证码错误
        check.equal(resp02['msg'], "验证码错误")

    # @pytest.mark.skip
    def test_get_password_success(self):
        """输入正确密码，可登陆成功"""
        resp03 = self.sms.api_get_password("123456", "mobile", self.mobile)
        print(resp03)
        # 断言，登陆成功
        check.equal(resp03['code'], 0)

    # @pytest.mark.skip
    def test_get_password_fail(self):
        """输入错误密码，登陆失败"""
        resp03 = self.sms.api_get_password("124569", "mobile", self.mobile)
        print(resp03)
        # 断言，登陆失败
        check.equal(resp03['msg'], '邮箱/手机号码或密码不正确，请重试')


if __name__ == '__main__':
    sms = TestSms()
    sms.setup_class()
    # 游客登陆
    sms.test_put_guest()
    # 发送验证码
    sms.test_get_login_correct()
    # sms.test_get_login_fail()
    # 验证码登陆
    time.sleep(60)
    sms.test_post_login_success()
    time.sleep(60)
    sms.test_post_login_fail()
    # 密码登陆
    sms.test_get_password_success()
    sms.test_get_password_fail()
