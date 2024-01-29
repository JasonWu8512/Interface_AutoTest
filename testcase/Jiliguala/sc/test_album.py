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
from business.Jiliguala.sc.ApiScAlbum import Apialbum
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testalbum :
    dm = Domains()

    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.SC_album = cls.config["SC_album"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.apialbum = Apialbum(token=cls.token)


    def test01_apialbum(self):
        """
        sc课程专辑详情页
        """

        resp = self.apialbum.api_album(self.SC_album['bid'],self.SC_album["albumId"])
        check.equal(resp["code"], 0)
        assert resp["data"]["_id"] == "AlbumCIX001"

