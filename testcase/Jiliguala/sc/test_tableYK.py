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
from business.Jiliguala.userbiz.ApiDeleteDevices import DeleteDevices

@pytest.mark.menu
class Testtable :
    dm = Domains()

    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = DeleteDevices()
        cls.SC_tableYK = cls.config["SC_tableYK"]
        cls.token = cls.user.get_token()
        cls.apiscbuy = Apitable(token=cls.token)


    def test01_table(self):
        """
        游客拓展tab页
        """
        resp = self.apiscbuy.api_table(self.SC_tableYK['bid'])
        check.equal(resp["code"], 0)
        # assert resp["data"]["childsong"]['level'] == 'S1GE'
        assert resp["data"]["entrances"][0]["name"] == "0-1岁亲子陪伴资源"
        assert resp["data"]["entrances"][1]["name"] == "口语交流室"
