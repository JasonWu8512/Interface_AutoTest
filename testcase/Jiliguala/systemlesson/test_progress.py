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
from business.Jiliguala.systemlesson.ApiProgress import ApiProgress
from business.Jiliguala.user.ApiUser import ApiUser



@pytest.mark.menu
class TestProgress:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.progress = cls.config["progress"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.apiprogress = ApiProgress(token=cls.token)

    def test01_apiprogress(self):
        resp = self.apiprogress.api_progress(self.progress["bid"])
        check.equal(resp["code"], 0) # 断言返回状态码
        assert resp['code'] == 0
        assert resp['status_code'] == 200
