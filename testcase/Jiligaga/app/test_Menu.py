"""
=========
Author:Lisa
time:2022/8/01 2:00 下午
=========
"""

import pytest
import pytest_check as check
from business.Jiligaga.app.ApiMenuReport import ApiMenuReport
from config.env.domains import Domains
from utils.middleware.dbLib import MySQL
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3


@pytest.mark.GagaReg
class TestMenuReport:
    dm = Domains

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.dm = Domains()
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.apiAccountV3 = ApiAccountV3()

    """
        家长中心侧边栏
    """

    def test_menu_report_Menu001(self):
        """家长中心侧边栏获取"""
        login = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                 countrycode=self.gaga_app["countryCodeTw"])
        print(login)
        token = login["data"]["auth"]
        print(token)
        bid = login["data"]["user"]["babyList"][0]["bid"]
        # mysql = MySQL(pre_db='jlgg', db_name='user')
        # menuno = mysql.query("SELECT * FROM inter_menu where menu_type='1'")
        # print(menuno)
        self.apimenureport= ApiMenuReport(token=token)
        resp = self.apimenureport.menu_report(bid=bid)
        check.equal(resp['code'], 0)
