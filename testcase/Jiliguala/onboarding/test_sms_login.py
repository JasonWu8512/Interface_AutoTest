# -*- coding: utf-8 -*-
# @Time : 2021/7/1 4:02 下午
# @Author : Cassie
# @File : test_sms_login.py
import pytest

from business.Jiliguala.onboarding.ApiGetsmslogin import ApiGetsmslogin
from business.Jiliguala.onboarding.ApiSmslogin import ApiSmslogin
from business.businessQuery import usersQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.onboarding
class TestSmsLogin(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.version = cls.config['version']['ver11.6']
        cls.agent = cls.config['agent']['ios_11.6']
        cls.mobile = cls.config['onboarding']['sms_user']  # 获取配置文件中发送手机号校验的测试账号
        cls.uid = UserProperty(cls.mobile).user["_id"]  # 获取手机号对应的uid
        cls.sms = ApiGetsmslogin()
        cls.login = ApiSmslogin()

    def test_sms_login_correct(self):
        """验证码正确性校验"""
        # 发送验证码
        self.sms.api_get_sms(target=self.mobile)
        # 输入错误的验证码进行登录
        res_fail = self.login.api_sms_login(code=1111, target=self.mobile, uid=self.uid)
        assert res_fail["code"] == 269
        assert res_fail["msg"] == "验证码错误"
        # 数据库查询正确的验证码进行登录
        code = usersQuery().get_users(mobile=self.mobile)["sms"]["code"]
        res_suc = self.login.api_sms_login(code=code, target=self.mobile, uid=self.uid)
        assert res_suc["code"] == 0

    def test_sms_login_valid(self):
        """校验验证码失效无法登录"""
        # 发送验证码
        self.sms.api_get_sms(target=self.mobile)
        code = usersQuery().get_users(mobile=self.mobile)["sms"]["code"]
        # 再次发送验证码
        self.sms.api_get_sms(target=self.mobile)
        # 输入上一次获取的验证码进行登录
        res_fail = self.login.api_sms_login(code=code, target=self.mobile, uid=self.uid)
        assert res_fail["code"] == 269
        assert res_fail["msg"] == "验证码错误"
