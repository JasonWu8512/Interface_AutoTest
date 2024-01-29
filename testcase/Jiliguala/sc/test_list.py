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
from business.Jiliguala.sc.ApiList import ApiList
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testlist :
    dm = Domains()

    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        cls.apilist = ApiList(token=cls.token)


    def test01_list(self):
        """
        sc拓展资源列表
        """

        resp = self.apilist.api_list()
        check.equal(resp["code"], 0)
        assert resp["data"]['albums'][0]['_id'] == 'AlbumCIX001'
        assert resp["data"]['albums'][0]['desc'] == '拓展资源在家上'
        assert resp['data']['albums'][1]['desc'] == '迪士尼分级阅读'