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
from business.Jiliguala.sc.ApiScLesson import ApiScLesson
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testlesson :
    dm = Domains()

    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config['CS_user']
        cls.SC_lesson = cls.config["SC_lesson"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user['user'], p=cls.CS_user['pwd'])
        cls.apilesson = ApiScLesson(token=cls.token)


    def test01_lesson(self):
        """
        sc课程详情页
        """

        resp = self.apilesson.api_lesson(self.SC_lesson['bid'],self.SC_lesson["lessonId"],self.SC_lesson["albumId"])
        check.equal(resp["code"], 0)
        # assert resp["data"]['hasCurLesson'] == True
        assert resp["data"]['album']['all'] == 7
