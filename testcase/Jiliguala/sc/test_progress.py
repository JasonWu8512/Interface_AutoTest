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
from business.Jiliguala.sc.ApiProgress import ApiProgress
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testprogress :
    dm = Domains()

    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.SC_progress = cls.config["SC_progress"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user['user'], p=cls.CS_user['pwd'])
        cls.apiprogress = ApiProgress(token=cls.token)


    def test01_lesson(self):
        """
        sc课程上报
        """
        resp = self.apiprogress.api_progress(self.SC_progress['bid'])
        check.equal(resp["code"], 0)
        assert resp["status_code"] == 200
