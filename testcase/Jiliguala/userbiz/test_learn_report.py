''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/8
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.userbiz.Apilearn import Api_Learn_Report
from business.Jiliguala.user.ApiUser import ApiUser

@pytest.mark.menu
class TestDetail:
    """
    呱美2.5报告
    """
    dm = Domains
    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.gm_learn = cls.config["gm_learn"]

        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.apireport = Api_Learn_Report(token=cls.token)

    def test01_apireport(self):
        """
        发送请求
        """
        resp = self.apireport.api_report(self.gm_learn['bid'],self.gm_learn['lessonId'])
        check.equal(resp["code"], 0) # 断言返回状态码
        # assert resp['data']['ava'] == 'https://qiniucdn.jiliguala.com/prod/upload/78beec061c78484fbdc688b8e77ed26a_20220728103414.jpg'
        assert resp["data"]["lessonX"] == "Day 16"
