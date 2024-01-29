# coding=utf-8
# @Time    : 2022/7/18 6:17 下午
# @Author  : Karen
# @File    : test_goldenTouchWithdraw.py


import pytest
from business.goldenTouch.systemlesson.ApiGoldenTouchWithdraw import ApiGoldenTouchWithdraw
from config.env.domains import Domains
from business.common.UserProperty import UserProperty


@pytest.mark.goldenTouch
class TestGoldenToucn(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path('fat')
        # 设置域名host
        cls.dm.set_domain(cls.config['url'])

        cls.notBuy_user = ApiGoldenTouchWithdraw(token=UserProperty(cls.config['goldenTouch']['notBuy_user']).basic_auth) # 13888888885 未购买用户
        cls.st99_user = ApiGoldenTouchWithdraw(token=UserProperty(cls.config['goldenTouch']['st99_user']).basic_auth) # 18600000000 已购实体9.9用户


    def test_ST99User_withdraw(self):
        """01 已购实体9.9用户（未达到提现条件）发起提现"""
        resp = self.st99_user.api_goldentouch_withdraw()
        assert resp['code'] == 1001
        assert resp['msg'] == '您暂不符合提现条件'


    def test_notBuyUser_withdraw(self):
        """02 未购买9.9用户（未达到提现条件）发起提现"""
        resp = self.notBuy_user.api_goldentouch_withdraw()
        assert resp['code'] == 1001
        assert resp['msg'] == '用户不存在'


    def test_ST99User_withdrawDetail(self):
        """03 已购实体9.9用户（未达到提现条件）查询提现明细"""
        resp = self.st99_user.api_goldentouch_queryWithdrawDetail('f8a9d22cf0b54bac96499032ef4fd6a6')
        assert resp['code'] == 0
        assert resp['data'][0]['flagStatus'] == 'expired'


    def test_notBuyUser_withdrawDetail(self):
        """04 未购买9.9用户（未达到提现条件）查询提现明细"""
        resp = self.notBuy_user.api_goldentouch_queryWithdrawDetail('8414cd50499746d0973221d42aae9c05')
        assert resp['code'] == 1001
        assert resp['msg'] == '用户不存在'
