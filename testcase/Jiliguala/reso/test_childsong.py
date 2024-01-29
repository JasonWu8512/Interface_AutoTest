''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/15
===============
'''
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.reso.Childsong.ApichildSong import ChildSong
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testchildsong:
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        # cls.childsong = ChildSong()


        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.song = cls.config["Song"]
        cls.CS_user = cls.config["CS_user"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.childsong = ChildSong(token=cls.token)

    def test01_childsong(self):
        """
        儿歌学堂
        """
        resp = self.childsong.songs(self.song["bid"],self.song["nonce"])
        check.equal(resp["code"], 0)
        check.equal(resp["status_code"], 200)
