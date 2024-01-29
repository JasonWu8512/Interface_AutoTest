''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/31
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.sc.Apitable import Apitable
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testtable :
    dm = Domains()

    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.SC_table = cls.config["SC_table"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.apiscbuy = Apitable(token=cls.token)


    def test01_table(self):
        """
        拓展tab
        """
        resp = self.apiscbuy.api_table(self.SC_table['bid'])
        check.equal(resp["code"], 0)
        # assert resp["data"]['albums']['AlbumCIX001']['purchaseUi']['bgColor'] == '#E8FEE8'
        assert resp["data"]["entrances"][0]["name"] == "0-1岁亲子陪伴资源"
        assert resp["data"]["entrances"][1]["name"] == "口语交流室"
        assert resp["data"]["entrances"][2]["name"] == "智能闯关"
        assert resp["data"]["entrances"][3]["name"] == "呱呱阅读" or "呱呱小屋"