# -*- coding: utf-8 -*-
# @Time : 2021/6/30 1:26 下午
# @Author : Cassie
# @File : test_onboarding_mobile.py
import base64

import pytest

from business.Jiliguala.onboarding.ApiGetsmslogin import ApiGetsmslogin
from business.Jiliguala.onboarding.ApiSmslogin import ApiSmslogin
from business.Jiliguala.onboarding.ApiUseronboarding import ApiUseronboarding
from business.businessQuery import usersQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.format.format import dateToTimeStamp


@pytest.mark.Onboarding
class TestOnboardingMobile:
    """
       游客账号新机转/老机转/9.9导流相关用例，针对11.4以上版本
       """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.version = cls.config['version']['ver11.6']
        cls.agent = cls.config['agent']['ios_11.6']
        cls.sms = ApiGetsmslogin()  # 实例化获取验证码类
        cls.login = ApiSmslogin()  # 实例化验证码登录类
        cls.onboarding = ApiUseronboarding(cls.version, cls.agent)

    @classmethod
    def teardown_class(cls):
        pass

    def get_smscode(self):
        """根据手机号查询验证码"""
        uid = self.sms.api_get_sms("19000000088")["data"]["uid"]
        code = usersQuery().get_users(_id=uid)["sms"]["code"]
        return code

    def get_sms_auth(self, mobile):
        """获取验证码注册的新手机号的鉴权信息"""
        register = self.sms.api_get_sms(mobile)
        uid = register["data"]["uid"]
        code = usersQuery().get_users(_id=uid)["sms"]["code"]
        res = self.login.api_sms_login(code=code, target=mobile, uid=uid)
        token = res["data"]["tok"]
        new_uid = res["data"]["_id"]
        basic = base64.b64encode(f'{new_uid}:{token}'.encode('utf-8'))
        return 'Basic ' + str(basic, encoding="utf-8")

    @pytest.mark.parametrize("mobile,day", [("19000000888", -731), ("19000000888", -822), ("19000000888", -1000)])
    def test_mobile_F2GE(self, mobile, day):
        """手机账号宝贝年龄>=2岁且<3岁导流到新机转，F2GE"""
        auth = self.get_sms_auth(mobile)
        bd = dateToTimeStamp(day=day)
        res = self.onboarding.api_user_onboarding(
            auth=auth,
            nick="自动化测试", bd=bd)
        uid = res["data"]["prt"]
        user_flags = usersQuery().get_user_flags(_id=uid)
        assert user_flags["allotNormalState"] == "JZ_NewMode_GEDoubleM"
        assert user_flags["allotNormalLevel"] == "F2GE"

    @pytest.mark.parametrize("mobile,day", [("19000000889", -1096), ("19000000889", -1338), ("19000000889", -2069)])
    def test_mobile_S1GE(self, mobile, day):
        """手机账号宝贝年龄>=3岁导流到新机转，S1GE"""
        auth = self.get_sms_auth(mobile)
        bd = dateToTimeStamp(day=day)
        res = self.onboarding.api_user_onboarding(
            auth=auth,
            nick="自动化测试", bd=bd)
        uid = res["data"]["prt"]
        user_flags = usersQuery().get_user_flags(_id=uid)
        assert user_flags["allotNormalState"] == "JZ_NewMode_GEDoubleM"
        assert user_flags["allotNormalLevel"] == "S1GE"

    @pytest.mark.parametrize("mobile,day",
                             [("19000000887", -730), ("19000000887", -365), ("19000000887", 0), ("19000000887", 11)])
    def test_mobile_tc(self, mobile, day):
        """手机账号宝贝年龄<2岁导流到9.9，K1GETC"""
        auth = self.get_sms_auth(mobile)
        bd = dateToTimeStamp(day=day)
        res = self.onboarding.api_user_onboarding(
            auth=auth,
            nick="自动化测试", bd=bd)
        uid = res["data"]["prt"]
        user_flags = usersQuery().get_user_flags(_id=uid)
        assert user_flags["allot99State"] == "GETC_NEW"
        assert user_flags["allot99Level"] == "K1GETC"
