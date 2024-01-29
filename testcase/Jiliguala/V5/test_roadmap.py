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
from business.Jiliguala.v5.Apiroadmap import ApiRoadmap
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testroadmap :
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.roadmap = cls.config["roadmap"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.apiroadmap = ApiRoadmap(token=cls.token)


    def test01_roadmapKC(self):
        """
        英语课程路线图
        """
        resp = self.apiroadmap.api_roadmapKC(self.roadmap["bid"])
        check.equal(resp["code"], 0)



    def test02_roadmapSW(self):
        """
        思维路线图
        """
        resp = self.apiroadmap.api_roadmapSW(self.roadmap["bid"])
        check.equal(resp['code'],0)
