''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/9
===============
'''



import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.lessonbiz.Apilessondetail import ApiLessonDetail
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testlessondetail:
    """
    1.5课程详情页
    """
    dm = Domains
    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(config['url'])
        cls.user = ApiUser()
        cls.agent = config['agent']['ios_11.12.3']
        cls.CS_user = config["CS_user"]
        cls.lessondetail = config["LessonDetail"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(cls.token)
        cls.apilessondetail = ApiLessonDetail(token=cls.token, agent=cls.agent)


    def test01_lessondetail(self):
        """
        发送请求
        """
        resp = self.apilessondetail.api_lessondetail(self.lessondetail['bid'])
        check.equal(resp["code"], 0) # 断言返回状态码
        # assert resp['data']['score'] == -1
        assert resp['data']['cn_ttl'] == '听说复习'
        assert resp['data']['unit'] == 'L3XXU13'

