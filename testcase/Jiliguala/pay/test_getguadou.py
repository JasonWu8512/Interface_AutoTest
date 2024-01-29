''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/22
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.pay.Apigetguadou import GetGuadou
from business.Jiliguala.user.ApiUser import ApiUser



@pytest.mark.menu
class TestUserController:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])

        #获取鉴权token
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.apiguadoustate = GetGuadou(token=cls.token)


    def test01_usercontroller(self):
        """
        获取瓜豆状态
        """
        resp = self.apiguadoustate.guadou_state()
        check.equal(resp["code"], 0)
        # assert resp['data']['balance'] == 8796530
        assert resp['data']["purchaseHelp"]["flow"] == "consultation" or "qrcode"
        assert resp["data"]["purchaseHelp"]["qrcode"]["title"] == '微信扫一扫'


