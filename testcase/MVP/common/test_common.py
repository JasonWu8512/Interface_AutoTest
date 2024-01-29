# coding=utf-8
# @Time    : 2022/9/29 1:43 下午
# @Author  : Karen
# @File    : test_common.py


import pytest
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from business.MVP.common.ApiCommon import ApiCommon
from config.env.domains import Domains


@pytest.mark.MVP
class TestCommon(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = g().get_guest_token()  # 创建游客并获取token
        ApiBaby(token=cls.guest_token).api_put_baby()  # 创建宝贝
        cls.guest = ApiCommon(token=cls.guest_token, ggheader=cls.config['ggheader_v2'])  # 创建游客实例

    def test_library_home(self):
        """01)图书馆首页热门专辑"""
        resp = self.guest.api_library()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['modules'][0]['type'] == 'banners'
        assert len(resp['data']['modules'][0]['contents']) > 0
        assert len(resp['data']['modules'][1]['contents']) > 0