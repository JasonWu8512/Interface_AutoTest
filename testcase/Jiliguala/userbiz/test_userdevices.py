''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/18
===============
'''
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.userbiz.ApiDevices import UserDevices
from business.Jiliguala.user.ApiUser import ApiUser



@pytest.mark.menu
class Testchildsong:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        # cls.childsong = ChildSong()

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.userdevices = UserDevices(token=cls.token)

    def test01_userdevices(self):
        resp = self.userdevices.devices()
        check.equal(resp["code"], 0)
        assert resp['code'] == 0
        assert resp['requestId'] != 'e5b22bb8ca0bfe2e'
        """
        获取不同设备
        """
        # assert resp['data']['devices'][0]['deviceType'] == 'iPhone SE 第二代'
        # assert resp['data']['devices'][1]['deviceType'] == 'vivo V2001A'