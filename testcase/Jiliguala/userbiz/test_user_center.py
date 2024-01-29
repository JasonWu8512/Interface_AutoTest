''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/29
===============
'''
import pytest
from config.env.domains import Domains
from business.common.UserProperty import UserProperty
from business.Jiliguala.userbiz.ApiUserCenter import ApiUserCenter



@pytest.mark.menu
class TestDetail:
    dm = Domains

    @classmethod
    def setup_class(cls):
        dm = Domains()
        config = dm.set_env_path("fat")
        user = UserProperty("13242040693")
        cls.token = user.basic_auth
        cls.version = config['version']['ver11.6']
        cls.usercenter = ApiUserCenter(token=cls.token, version=cls.version)

    def test01_get_usercenter(self):
        """10.5一下版本 家长中心数据"""

        resp=self.usercenter.api_get_usercenter(bid='b1d4ffd0b19b4dd9b8e5aeb29c13ac0d', id='5286509c471e48bbb2705985d695dea2', level='L1XX')
        assert resp['code'] == 0

    def test02_get_usercenter_v2(self):
        """ 10.5及以上版本 家长中心数据"""

        resp = self.usercenter.api_get_usercenter_v2(bid='b1d4ffd0b19b4dd9b8e5aeb29c13ac0d', id='5286509c471e48bbb2705985d695dea2', level='T1GE')
        assert resp['code'] == 0

    def test03_get_usercenter_v3(self):
        """11.4及以上 家长中心数据"""
        resp = self.usercenter.api_get_usercenter_v3(bid='ee46b9f8738b4b3a9472d95de1d74003',id='5286509c471e48bbb2705985d695dea2')
        assert resp['code'] == 0


