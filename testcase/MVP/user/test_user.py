# coding=utf-8
# @Time    : 2022/9/20 4:52 下午
# @Author  : Karen
# @File    : test_user.py


import pytest
from business.MVP.user.ApiUser import ApiUser
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from config.env.domains import Domains


@pytest.mark.MVP
class TestUser(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = g().get_guest_token()  # 创建游客并获取token
        ApiBaby(token=cls.guest_token).api_put_baby() # 创建宝贝
        cls.guest = ApiUser(token=cls.guest_token)  # 创建游客实例


    def test_user_info(self):
        """01）获取用户信息"""
        resp = self.guest.api_user_info()
        assert resp['code'] == 0
        assert resp['data']['typ'] == 'guest'
        assert resp['data']['guaid'] != None
        assert resp['data']['curBid'] != None


    def test_user_corrections(self):
        """02）使用纠音、查询用户剩余的免费纠音次数"""

        # 新注册用户  有2次免费纠音机会
        resp = self.guest.api_corrections_times()
        assert resp['code'] == 0
        assert resp['data']['isVIP'] == False
        assert resp['data']['times'] == 2

        # 进行一次纠音，还剩一次机会
        bid = self.guest.api_user_info()['data']['curBid']
        resp1 = self.guest.api_correct_record(bid)
        print(resp1)

        resp2 = self.guest.api_corrections_times()
        assert resp2['data']['times'] == 1


    def test_record_setting(self):
        """03）录音评分设置"""
        resp = self.guest.api_record_setting()
        assert resp['code'] == 0
        assert resp['data']['scoreStandard'] == 'general'
