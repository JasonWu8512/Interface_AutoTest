'''
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/8/10
===============
'''




import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.mytab.ZptFh import Zpt
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
        cls.CS_user = cls.config["Cj_ZptFh"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.myapi = Zpt(token=cls.token)

    def test01_web_sms(self):

        """
        获取验证码
        """
        resp = self.myapi.api_WebSms()
        assert resp["code"] == 0
        check.equal(resp["code"], 0)

    def test02_tokensV3(self):
        """
        输入验证码
        """
        self.code = usersQuery().get_users(mobile=self.mobile["mobile1"])["sms"]["code"]
        resp = self.myapi.api_tokensV3(self.mobile["mobile1"],self.code)
        assert resp["code"] == 0
        check.equal(resp["code"],0)

    def test03_stock_v2(self):
        """

        """
        resp = self.myapi.api_stock_v2()
        assert resp["code"] == 0
        assert resp['data']['items'][0]['sguList'][0]['sguImg'] == 'https://qiniucdn.jiliguala.com/eshop/6927ac6f-00c7-44e5-9e6d-582e2cbd54e9.png'


    def test04_config_v2(self):
        """

        """
        resp = self.myapi.api_config_v2()
        assert resp["code"] == 0
        check.equal(resp["code"],0)
        assert resp['data']['join']['jumpUrl'] == "https://fatspa.jiliguala.com/store/share/index.html#/item?itemid=H5_XX_Sample&spu=K1GEFC_0_SPU_WXstore"



