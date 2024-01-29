# coding=utf-8
# @Time    : 2022/7/18 6:16 下午
# @Author  : Karen
# @File    : test_goldenTouch.py


import pytest
from business.goldenTouch.systemlesson.ApiGoldenTouch import ApiGoldenTouch
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

        cls.notBuy_user = ApiGoldenTouch(token=UserProperty(cls.config['goldenTouch']['notBuy_user']).basic_auth) # 13888888885 未购买用户
        cls.st99_user = ApiGoldenTouch(token=UserProperty(cls.config['goldenTouch']['st99_user']).basic_auth) # 18600000000 已购实体9.9用户


    def test_ST99User_stRoadmap_v2(self):
        """01 已购实体9.9用户请求路线图"""
        resp = self.st99_user.api_goldentouch_roadmap_v2('da48ab2c2f174debbb0046e923f007ac', '08c9cca9547744c7b2a61921152485e3')
        assert resp['code'] == 0
        assert resp['data']['levels'][0]['name'] == '体验营'
        assert resp['data']['weeks'][0]['weekName'] == '体验周'


    def test_ST99User_K1Roadmap_v2(self):
        """02 已购用户请求K1路线图"""
        resp = self.st99_user.api_goldentouch_roadmap_v2('da48ab2c2f174debbb0046e923f007ac', '08c9cca9547744c7b2a61921152485e3')
        assert resp['code'] == 0
        assert resp['data']['levels'][1]['name'] == 'K1'
        assert resp['data']['weeks'][1]['weekName'] == '第1周'


    def test_ST99User_user_stLession(self):
        """03 已购用户访问体验课课程详情页（已开课）"""
        resp = self.st99_user.api_goldentouch_lesson('da48ab2c2f174debbb0046e923f007ac', '08c9cca9547744c7b2a61921152485e3', 'bf9d926c9ba84254b28adf8fe8819dc0')
        assert resp['code'] == 0
        assert resp['data']['subLessons'][0]['name'] == '词汇和绘本' # 子课程名称
        assert resp['data']['subLessons'][0]['gameType'] == 'video'  # 子课程类型


    def test_ST99User_user_K1Lession(self):
        """04 已购用户访问K1课程详情页"""
        resp = self.st99_user.api_goldentouch_lesson('da48ab2c2f174debbb0046e923f007ac', '08c9cca9547744c7b2a61921152485e3', 'ba77c39d8b57467798862dda52a9e0b3' )
        assert resp['code'] == 0
        assert resp['data']['subLessons'][0]['name'] == '热身挑战' # 子课程名称
        assert resp['data']['subLessons'][0]['gameType'] == 'video'  # 子课程类型


    def test_ST99User_STvideo(self):
        """05 已购用户访问体验课子课程视频"""
        resp = self.st99_user.api_goldentouch_video('STYY990101NEW') #体验课第一节课的子课程
        assert resp['code'] == 0
        assert resp['data'] != None


    def test_ST99User_K1video(self):
        """06 已购用户访问K1子课程视频"""
        resp = self.st99_user.api_goldentouch_video('STYYK1W101') #K1第一节课的子课程
        assert resp['code'] == 0
        assert resp['data'] != None


    def test_ST99User_K1video_progress(self):
        """07 体验课第一节子课程完课上报"""
        resp = self.st99_user.api_goldentouch_progress('STYYK1W101', 'b49732e316d34c5c90db0fbab5f77d47', '08c9cca9547744c7b2a61921152485e3')
        assert resp['code'] == 0
        assert resp['data'] == 'success'
