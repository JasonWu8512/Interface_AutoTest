# coding=utf-8
# @Time    : 2022/9/29 1:52 下午
# @Author  : Karen
# @File    : test_vip.py


import pytest
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from business.MVP.vip.ApiVip import ApiVip
from business.MVP.aggregation.ApiGGRVip import ApiGGRVip
from config.env.domains import Domains
import datetime

@pytest.mark.MVP
class TestVip(object):
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
        cls.guest = ApiVip(token=cls.guest_token)  # 创建游客实例

    def test_vip_status(self):
        """01)查询vip状态"""
        # 新注册游客，vip状态为false
        resp = self.guest.api_get_vip()
        assert resp['code'] == 0
        assert resp['data']['vip'] == False
        assert resp['data']['paid'] == False

        # 领取免费VIP，状态变为true
        ApiGGRVip(token=self.guest_token).api_ggraggregation_vip_set('jlgl_introduce','day')
        resp2 = self.guest.api_get_vip()
        assert resp2['code'] == 0
        assert resp2['data']['vip'] == True
        assert resp2['data']['paid'] == False
        assert resp2['data']['isLifetime'] == False
        assert resp2['data']['expires'][:10] == str(datetime.datetime.today())[:10]