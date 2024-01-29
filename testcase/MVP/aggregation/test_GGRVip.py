# coding=utf-8
# @Time    : 2022/9/28 11:33 上午
# @Author  : Karen
# @File    : test_GGRVip.py

import pytest
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from business.MVP.aggregation.ApiGGRVip import ApiGGRVip
from config.env.domains import Domains


@pytest.mark.MVP
class TestGGRVip(object):
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
        cls.guest = ApiGGRVip(token=cls.guest_token)  # 创建游客实例

    def test_set_vip(self):
        """01）领取1天免费VIP"""
        # 新注册用户 首次进入MVP还未领取MVP
        resp = self.guest.api_ggraggregation_vip_exist('jlgl_introduce')
        assert resp['code'] == 0
        assert resp['data']['exist'] == False
        assert resp['data']['expiredTime'] == 0

        # 点击返回 跳出领取MVP弹窗，点击进入 获得1天MVP
        resp2 = self.guest.api_ggraggregation_vip_set('jlgl_introduce', 'day')
        assert resp2['code'] == 0
        assert resp2['data']['success'] == True
        assert resp2['data']['expiredTime'] == 86400

        # 再次查询是否已领取过VIP，是
        resp3 = self.guest.api_ggraggregation_vip_exist('jlgl_introduce')
        assert resp3['code'] == 0
        assert resp3['data']['exist'] == True
        assert resp3['data']['expiredTime'] == 86399