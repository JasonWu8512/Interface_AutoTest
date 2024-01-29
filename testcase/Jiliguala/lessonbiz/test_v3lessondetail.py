''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/10
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.lessonbiz.Apiv3lessondetail import ApiV3LessonDetail
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testv3lessondetail:
    """
    课程详情页
    """
    dm = Domains
    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(config['url'])
        cls.user = ApiUser()
        cls.v3 = config["v3lessondetail"]
        cls.CS_user = config["CS_user"]
        token = cls.user.get_token(typ='mobile', u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.apiv3lessondetail = ApiV3LessonDetail(token=token)


    def test01_v3lessondetailBD(self):
        """
        呱呱爱表达课程详情页
        """
        resp = self.apiv3lessondetail.api_v3lessondetailBD(self.v3["bid"],self.v3["noncebd"])
        check.equal(resp["code"], 0) # 断言返回状态码
        assert resp['data']['_id'] == "K1GEE001"
        assert resp['data']['lv'] == 'K1GE'
        assert resp['data']['subject'] == 'GE'

    def test02_v3lessondetailSk(self):
        """
        呱呱爱思考课程详情页
        """
        resp = self.apiv3lessondetail.api_v3lessondetailSk(self.v3["bid"],self.v3['noncesk'])
        check.equal(resp["code"],0) # 断言返回状态码
        assert resp["data"]['_id'] == "K1MAE001"
        assert resp["data"]['lv'] == "K1MA"
        assert resp["data"]["subject"] == "MA"


