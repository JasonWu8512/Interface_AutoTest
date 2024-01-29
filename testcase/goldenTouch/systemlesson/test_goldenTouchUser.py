# coding=utf-8
# @Time    : 2022/7/18 6:16 下午
# @Author  : Karen
# @File    : test_goldenTouchUser.py


import pytest
from business.goldenTouch.systemlesson.ApiGoldenTouchUser import ApiGoldenTouchUser
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

        cls.notBuy_user = ApiGoldenTouchUser(token=UserProperty(cls.config['goldenTouch']['notBuy_user']).basic_auth) # 13888888885 未购买用户
        cls.st99_user = ApiGoldenTouchUser(token=UserProperty(cls.config['goldenTouch']['st99_user']).basic_auth) # 18600000000 已购实体9.9用户


    def test_ST99User_myAssistant(self):
        """01 已购实体9.9用户添加启蒙顾问"""
        resp = self.st99_user.api_goldentouch_user_myAssistant()
        assert resp['code'] == 0
        assert resp['data']['hasAssistant'] == True
        assert resp['data']['date'] != None


    def test_notBuyUser_myAssistant(self):
        """02 未购买用户添加启蒙顾问"""
        resp = self.notBuy_user.api_goldentouch_user_myAssistant()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['hasAssistant'] == False


    def test_ST99User_awardStatus(self):
        """03 已购用户（未达到提现条件）查询提现状态"""
        resp = self.st99_user.api_goldentouch_user_awardStatus()
        assert resp['code'] == 0
        assert resp['data']['showAwardEntrance'] == True
        assert resp['data']['orderAmount'] == 990.00
        assert resp['data']['awarded'] == False
        assert resp['data']['errorMessage'] == 1


    def test_notBuyUser_awardStatus(self):
        """04 未购用户查询提现状态"""
        resp = self.notBuy_user.api_goldentouch_user_awardStatus()
        assert resp['code'] == 0
        assert resp['data']['showAwardEntrance'] == False


    def test_notBuyUser_possessed(self):
        """05 未购买用户：是否拥有课程，前端用来判断是让他购买还是进路线图"""
        resp = self.notBuy_user.api_goldentouch_possessed()
        assert resp['code'] == 0
        assert resp['data'] == 'NONE'


    def test_st99User_possessed(self):
        """06 已购买用户：是否拥有课程，前端用来判断是让他购买还是进路线图"""
        resp = self.st99_user.api_goldentouch_possessed()
        assert resp['code'] == 0
        assert resp['data'] == 'da48ab2c2f174debbb0046e923f007ac'
