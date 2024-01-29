# -*- coding: utf-8 -*-
# @Time : 2021/6/22 9:24 下午
# @Author : Cassie
# @File : test_onboarding_guest.py
import base64

import pytest

from business.Jiliguala.onboarding.ApiUseronboarding import ApiUseronboarding
from business.Jiliguala.onboarding.ApiUsersguestv2 import ApiUsersguestv2
from business.businessQuery import usersQuery
from config.env.domains import Domains
from utils.format.format import dateToTimeStamp


@pytest.mark.Onboarding
class TestOnboardingGuest:
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
        cls.guest = ApiUsersguestv2(cls.version, cls.agent)
        cls.onboarding = ApiUseronboarding(cls.version, cls.agent)

        # cls.user_flags = usersQuery().get_user_flags(_id=cls.uid)
        # print(cls.user_flags)

    @classmethod
    def teardown_class(cls):
        pass

    def get_guest_auth(self):
        """获取游客账号对应的鉴权信息"""
        res = self.guest.api_users_guestv2()
        token = res["data"]["tok"]
        uid = res["data"]["_id"]
        code = base64.b64encode(f'{uid}:{token}'.encode('utf-8'))
        return 'Basic ' + str(code, encoding="utf-8")

    def test_create_guest(self):
        """创建游客账号"""
        res = self.guest.api_users_guestv2()
        print(res)
        assert res["code"] == 0
        assert res["data"]["typ"] == "guest"

    # @pytest.mark.parametrize("day", [-731, -822, -1000])
    # @pytest.mark.parametrize("day", [-731])
    # def test_guest_F2GE(self, day):
    #     """游客账号宝贝年龄>=2岁且<3岁导流到新机转，F2GE"""
    #     auth = self.get_guest_auth()
    #     bd = dateToTimeStamp(day=day)
    #     res = self.onboarding.api_user_onboarding(
    #         auth=auth,
    #         nick="自动化测试", bd=bd)
    #     uid = res["data"]["prt"]
    #     user_flags = usersQuery().get_user_flags(_id=uid)
    #     print(user_flags)
    #     assert user_flags["allotNormalState"] == "JZ_NewMode_GEDoubleM"
    #     assert user_flags["allotNormalLevel"] == "F2GE"

    # @pytest.mark.parametrize("day", [-1096, -1338, -2069])
    # def test_guest_S1GE(self, day):
    #     """游客账号宝贝年龄>=3岁导流到新机转，S1GE"""
    #     auth = self.get_guest_auth()
    #     bd = dateToTimeStamp(day=day)
    #     res = self.onboarding.api_user_onboarding(
    #         auth=auth,
    #         nick="自动化测试", bd=bd)
    #     uid = res["data"]["prt"]
    #     user_flags = usersQuery().get_user_flags(_id=uid)
    #     assert user_flags["allotNormalState"] == "JZ_NewMode_GEDoubleM"
    #     assert user_flags["allotNormalLevel"] == "S1GE"

    # v11.12.0以后，增量用户全部导到GETC_NEW
    @pytest.mark.parametrize("day", [-730, -365, 0, 11])
    def test_guest_tc(self, day):
        """游客账号宝贝年龄<2岁导流到9.9，K1GETC"""
        auth = self.get_guest_auth()
        bd = dateToTimeStamp(day=day)
        res = self.onboarding.api_user_onboarding(
            auth=auth,
            nick="自动化测试", bd=bd)
        uid = res["data"]["prt"]
        user_flags = usersQuery().get_user_flags(_id=uid)
        assert user_flags["allot99State"] == "GETC_NEW"
        assert user_flags["allot99Level"] == "K1GETC"
