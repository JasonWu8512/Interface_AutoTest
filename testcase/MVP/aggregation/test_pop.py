# coding=utf-8
# @Time    : 2022/9/29 1:32 下午
# @Author  : Karen
# @File    : test_pop.py


import pytest
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from business.MVP.aggregation.ApiPop import ApiPop
from config.env.domains import Domains


@pytest.mark.MVP
class TestPop(object):
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
        cls.guest = ApiPop(token=cls.guest_token)  # 创建游客实例

    def test_vip_popup(self):
        """01）领取VIP弹窗"""
        resp = self.guest.api_ggraggregation_pop('jlgl_introduce_none')
        assert resp['code'] == 0
        assert resp['data']['picUrl'] == 'https://gaeacdn.jiliguala.com/jlgl/ggr-wap/03d99757715b30738dcf5e3e724b9a5c.png'
        assert resp['data']['jumpLink'] == 'jlglr://activity?url=https%3A%2F%2Ffatspa.jiliguala.com%2Fggr-wap%2Fjlgl%2Findex.html%23%2Fvip-gift%3Fsource%3D***'