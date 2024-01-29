'''
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/8/8
===============
'''



import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.mytab.zpt import Zpt
from business.Jiliguala.user.ApiUser import ApiUser
from business.businessQuery import usersQuery


@pytest.mark.menu
class TestZpt(object):
    dm = Domains()

    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('fat')  # 测试环境
        cls.dm.set_domain(cls.config['url'])  # 准备测试的url地址
        cls.user = ApiUser()
        cls.mobile = cls.config["CJ_Zpt"]
        cls.CS_user = cls.config["CS_user"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.myapi = Zpt(token=cls.token)

    def test01_web_sms(self):

        """
        获取验证码
        """
        resp = self.myapi.api_web_sms()
        assert resp["code"] == 0
        check.equal(resp["code"], 0)

    def test02_tokens_v3(self):
        """
        输入验证码
        """
        self.code = usersQuery().get_users(mobile=self.mobile["mobile"])["sms"]["code"]
        resp = self.myapi.api_tokens_v3(self.mobile["mobile"],self.code)
        assert resp["code"] == 0
        check.equal(resp["code"],0)

    def test03_popup(self):
        """

        """
        resp = self.myapi.api_popup()
        assert resp["code"] == 0
