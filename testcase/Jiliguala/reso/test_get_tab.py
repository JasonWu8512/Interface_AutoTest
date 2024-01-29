''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/2
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.reso.getportrait.ApiGet import ApiGet
from business.Jiliguala.user.ApiUser import ApiUser



@pytest.mark.menu
class Testget_tab:
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
        cls.get_tab= cls.config["get_tab"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.gettab = ApiGet(token=cls.token)

    def test01_get_usertab(self):
        """
        """
        resp = self.gettab.api_get_usertab(self.get_tab["bid"],self.get_tab["mod"],self.get_tab["channel"])
        check.equal(resp["code"], 0)
        # assert resp['data'][0]['id'] == 172 #断言id
        # assert resp['data'][0]['title'] == '邀请有礼'
        # assert resp['data'][0]['content']['buId'] == 'jlgl'
        # check.equal(resp["status_code"], 200)

    def test02_get_buytab(self):
        resp = self.gettab.api_get_usertab(self.get_tab["bid"],self.get_tab["channel"],self.get_tab["mod1"])
        assert resp["code"] == 0


