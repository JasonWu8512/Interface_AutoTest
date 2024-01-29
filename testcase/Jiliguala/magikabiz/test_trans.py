''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/14
===============
'''
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.reso.Usercontroller.ApiUserController import ApiUserController
from business.Jiliguala.user.ApiUser import ApiUser



@pytest.mark.menu
class TestUserController:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.token = cls.user.get_token(typ="mobile", u="18664309513", p="123456")
        print(cls.token)
        cls.apiUserController = ApiUserController(token=cls.token)


    def test01_usercontroller(self):
        """
        查看魔石明细
        """
        resp = self.apiUserController.magika()
        check.equal(resp["code"], 0)


