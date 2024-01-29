"""
=========
Author:Lisa
time:2023/2/22 2:00 下午
=========
"""

import pytest
import pytest_check as check
import hypothesis

from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiUserGetMyInfo import ApiUserGetMyInfo
# from business.Jiligaga.app.ApiHomeParentCenter import *
from config.env.domains import Domains
from business.Jiligaga.app.ApiLogin import Login
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3


@pytest.mark.GagaReg
class TestUserGetMyInfo:
    dm = Domains

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.dm = Domains()
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.login = Login()
        cls.apiAccountV3 = ApiAccountV3()
        cls.apiUserGetMyInfo = ApiUserGetMyInfo()

    def test_post_user_getMyInfo(self):
        """
        查询家长中心
        """
        self.token = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                      countrycode=self.gaga_app["countryCodeTw"])["data"][
            "auth"]
        # self.token = self.login.phone_pwd_login ( phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"] )["data"][
        #     "auth"]
        self.apiUserGetMyInfo = ApiUserGetMyInfo(self.token)
        resp = self.apiUserGetMyInfo.api_user_getMyInfo()
        check.equal(resp["code"], 0)
