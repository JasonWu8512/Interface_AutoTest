# -*- coding: utf-8 -*-
# @Time : 2021/7/1 3:20 下午
# @Author : Cassie
# @File : test_password_login.py
from time import sleep

import pytest

from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.Jiliguala.onboarding.ApiUserstokensv2 import ApiUserstokensv2
from business.businessQuery import usersQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.onboarding
class TestPasswordLogin(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.mobile = cls.config['onboarding']['password_user']  # 获取配置文件中密码校验的测试账号
        cls.uid = UserProperty(cls.mobile).user["_id"]  # 获取手机号对应的uid
        cls.user = UserProperty(cls.mobile)
        cls.token = cls.user.basic_auth
        cls.password = ApiUserstokensv2()
        cls.sms = ApiSmsInfo(cls.token)

    @classmethod
    def teardown_class(cls):
        pass

    @pytest.mark.parametrize("p", {"123456", "abcd1234", "!@AHSHH"})
    def test_set_new_password(self, p):
        """重新设置新密码"""
        # 发送验证码
        self.sms.api_sms_password_g(target=self.mobile, nonce="23B765F2-359F-44FA-9020-FB41280D24AB",
                                    pandora="M1YyNTQ1NTgyNTMzMjoyMDIwMDUwODE2NTYxMzdlZDQyNTNmYTI4ZGViMGE0ZTdkNmE0NTA4MWQ1NTY5MDFlM2MwYTljZTc3YjBlNDphY2U4NDQ1NGVhODk4Mzg4MzRjOWE2M2NhOTU1YzlkYg==")
        # 数据库查询验证码
        code = usersQuery().get_users(mobile=self.mobile)["sms"]["code"]
        print(code)
        # 重置密码，输入错误的验证码
        res_fail = self.sms.api_sms_password_p(target=self.mobile, code=1234,
                                               pandora="MTYyNTQ1NTgyNTMzMjoyMDIwMDUwODE2NTYxMzdlZDQyNTNmYTI4ZGViMGE0ZTdkNmE0NTA4MWQ1NTY5MDFlM2MwYTljZTc3YjBlNDphY2U4NDQ1NGVhODk4Mzg4MzRjOWE2M2NhOTU1YzlkYg==",
                                               p=p)
        assert res_fail["code"] == 140
        assert res_fail["msg"] == "验证码错误"
        # 重置密码，输入正确的验证码
        res_fail = self.sms.api_sms_password_p(target=self.mobile, code=code,
                                               pandora="MTYyNTQ1NTgyNTMzMjoyMDIwMDUwODE2NTYxMzdlZDQyNTNmYTI4ZGViMGE0ZTdkNmE0NTA4MWQ1NTY5MDFlM2MwYTljZTc3YjBlNDphY2U4NDQ1NGVhODk4Mzg4MzRjOWE2M2NhOTU1YzlkYg==",
                                               p=p)
        assert res_fail["code"] == 0
        # 使用新密码进行登录
        login = self.password.api_users_tokensv2(p=p, typ="mobile", u=self.mobile)
        assert login["code"] == 0
        sleep(60)

    def test_password_correct(self):
        """密码正确性校验"""
        res_fail = self.password.api_users_tokensv2(p="1234567", typ="mobile", u=self.mobile)
        assert res_fail["code"] == 135
        assert res_fail["msg"] == "邮箱/手机号码或密码不正确，请重试"
