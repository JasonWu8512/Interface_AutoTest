''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/27
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.systemlesson.Apidetail import ApiDetail
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class TestLessonDetail:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.detail = cls.config["detail"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.apidetail = ApiDetail(token=cls.token)

    def test_Detail(self):
        """3.0课程详情页"""
        resp = self.apidetail.api_detail(self.detail["bid"], self.detail["lid"])
        check.equal(resp["code"], 0)  # 断言返回状态码
        assert resp['data']['_id'] == 'F1GEF002'  # 断言用户id
        assert resp['data']['lv'] == 'F1GE'  # 断言用户等级
        assert resp['data']['subject'] == 'GE'

