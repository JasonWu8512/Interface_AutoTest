''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/23
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.sc.ApiScBuy import ApiScBuy
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testscbuy :
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.SC_buy = cls.config["SC_buy"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.apiscbuy = ApiScBuy(token=cls.token) #传入token


    def test01_sc_buy(self):
        """
        sc专辑购买页
        """
        resp = self.apiscbuy.api_buy(self.SC_buy["lessonId"],self.SC_buy["albumId"])
        check.equal(resp["code"], 0)
        assert resp["data"]['albums']['AlbumCIX001']['_id'] == 'AlbumCIX001'
        assert resp["data"]['albums']['AlbumCIX001']['purchaseUi']['bgColor'] == '#E8FEE8'
