# -*- coding: utf-8 -*-
# @Time : 2022/8/24 4:26 下午
# @Author : anna
from time import sleep
import os

import pytest

from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.Jiliguala.pay.ApiShoppingTab import ApiShoppingTab
from business.Jiliguala.systemlesson.ApiHome import ApiHome
from business.Jiliguala.user.ApiUser import ApiUser
from business.businessQuery import usersQuery, pingxxorderQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.systemlesson
class TestHome(object):
    """
        v4/home 首页
    """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # 【代码提交用】获取环境变量
        cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        print(env)
        # 本地调试用
        # cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        pwd = '123456'
        typ = "mobile"
        cls.xApp = cls.config['home']['x-app-params']
        cls.unPurchased = cls.user.get_token(typ=typ, u=cls.config['home']['unPurchased'], p=pwd)  # 未购用户
        cls.ex_user = cls.user.get_token(typ=typ, u=cls.config['home']['ex_user'], p=pwd)  # 已购体验课
        cls.en_user = cls.user.get_token(typ=typ, u=cls.config['home']['en_user'], p=pwd)  # 已购英语正价课
        cls.ma_user = cls.user.get_token(typ=typ, u=cls.config['home']['ma_user'], p=pwd)  # 已购思维正价课
        cls.mix_user = cls.user.get_token(typ=typ, u=cls.config['home']['mix_user'], p=pwd)  # 已购思维/英语体验课+思维/英语正价课
        # cls.diploma_user = cls.user.get_token(typ=typ, u=cls.config['home']['diploma_user'],
        #                                       p=pwd)  # 已购思维/英语体验课+思维/英语正价课
        cls.yt_user = cls.user.get_token(typ=typ, u=cls.config['home']['yt_user'], p=pwd)  # 已购年课体验课
        cls.y_user = cls.user.get_token(typ=typ, u=cls.config['home']['y_user'], p=pwd)  # 已购年课正价课

        # 获取不同用户的第一个宝贝id
        cls.b_unPurchased = cls.config['home']['unPurchased_b']
        cls.b_ex_user = cls.config['home']['ex_user_b']
        cls.b_en_user = cls.config['home']['en_user_b']
        cls.b_ma_user = cls.config['home']['ma_user_b']
        cls.b_mix_user = cls.config['home']['mix_user_b']
        # cls.b_diploma_user = cls.config['home']['diploma_user_b']
        cls.b_yt_user = cls.config['home']['yt_user_b']
        cls.b_y_user = cls.config['home']['y_user_b']

        version = "niuwa/11.12.3 (iPhone; iOS 14.0.1; Scale/2.00)"
        # 实例化接口
        cls.home_unPurchased = ApiHome(cls.unPurchased)
        cls.home_ex = ApiHome(cls.ex_user)
        cls.home_en = ApiHome(cls.en_user, version=version, xApp=cls.xApp)
        cls.home_ma = ApiHome(cls.ma_user)
        cls.home_mix = ApiHome(cls.mix_user, version=version, xApp=cls.xApp)
        cls.home_yt = ApiHome(cls.yt_user, version=version, xApp=cls.xApp)
        cls.home_y = ApiHome(cls.y_user, version=version, xApp=cls.xApp)

        # cls.home_diploma_user = ApiHome(cls.diploma_user, version)

    def test_home_unPurchased(self):
        """
        未购用户，首页标题、顶部资源位、周主题、底部资源位展示无误
        """
        res = self.home_unPurchased.api_get_v4_home(bid=self.b_unPurchased)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言首页标题展示：呱呱爱表达K1
        assert res['data']['roadmap']['info']['ttl'] == '呱呱爱表达'
        assert res['data']['roadmap']['info']['level'] == 'K1'
        # 断言顶部资源位展示无误
        assert res['data']['roadmap']['elements'][0]['tips'][0]['title'] == '了解0元课'
        # 断言周主题展示成：体验营
        assert res['data']['roadmap']['elements'][1]['weekTitle'] == '体验营'
        # 断言底部资源位展示成呱呱阅读
        # assert res['data']['roadmap']['elements'][1]['tips'][0][
        #            'target'] == 'JLGL://album-c?albumid=AlbumCIX001&source=v4_afterclass_recommendation'

    def test_home_exEn(self):
        """
        已购体验课用户，英语tab，首页标题、顶部资源位、周主题、底部资源位展示无误
        """
        res = self.home_ex.api_get_v4_home(bid=self.b_ex_user, subject='GE')
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # # 断言首页标题展示：呱呱爱表达K1
        assert res['data']['roadmap']['info']['ttl'] == '呱呱爱表达'
        assert res['data']['roadmap']['info']['level'] == 'K1'
        # 断言顶部资源位：展示填写地址资源位
        # assert res['data']['roadmap']['elements'][0]['tips'][0]['title'] == '体验课课前准备-填写地址'
        # 断言顶部资源位：专享试听内容
        assert res['data']['roadmap']['elements'][0]['tips'][0][
                   'image'] == 'https://qiniucdn.jiliguala.com/sc/zhuanxiang/shiting.png'
        # 断言周主题展示成：体验营
        assert res['data']['roadmap']['elements'][1]['weekTitle'] == '体验营'
        # 断言底部资源位展示成呱呱阅读
        # assert res['data']['roadmap']['elements'][2]['tips'][0][
        #            'target'] == 'JLGL://album-c?albumid=AlbumCIX001&source=v4_afterclass_recommendation'

    def test_home_exMa(self):
        """
        已购体验课用户，思维tab，首页标题、顶部资源位、周主题、底部资源位展示无误
        """
        res = self.home_ex.api_get_v4_home(bid=self.b_ex_user, subject='MA')
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # # 断言首页标题展示：呱呱爱表达K1
        assert res['data']['roadmap']['info']['ttl'] == '呱呱爱思考'
        assert res['data']['roadmap']['info']['level'] == 'K1'
        # 断言顶部资源位：展示填写地址资源位
        # assert res['data']['roadmap']['elements'][0]['tips'][0]['title'] == '体验课课前准备-填写地址'
        # 断言周主题展示成：体验营
        assert res['data']['roadmap']['elements'][0]['weekTitle'] == '体验营'
        # 断言底部资源位展示成呱呱阅读
        # assert res['data']['roadmap']['elements'][1]['tips'][0][
        #            'target'] == 'JLGL://album-c?albumid=AlbumCIX001&source=v4_afterclass_recommendation'

    def test_home_en(self):
        """
        已购英语正价课用户，首页标题、周主题、底部资源位展示无误
        """
        res = self.home_en.api_get_v4_home(bid=self.b_en_user)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言首页标题展示：呱呱爱表达*
        assert res['data']['roadmap']['info']['ttl'] in '呱呱爱表达(2021)'
        weekTitle = res['data']['roadmap']['elements'][0]['weekTitle']
        print(weekTitle)
        preWeekTitle = "第 1 周 / 共 24 周"
        # 断言顶部资源位
        if weekTitle == preWeekTitle:
            assert res['data']['roadmap']['elements'][0]['tips'][0]['title'] == '正式课课前准备'
            assert res['data']['roadmap']['elements'][0]['tips'][1]['title'] == '引导关注公众号'
            # 断言学习进度第x/共24周
            assert " 共 24 周" in res['data']['roadmap']['elements'][1]['weekTitle']
            # 断言有底部资源位
            assert res['data']['roadmap']['elements'][1]['tips'][0]['title'] == '拓展推荐'
        else:
            print("正价课已开课")
        for element in res['data']['roadmap']['elements']:
            if 'weekTitle' in element and element['weekTitle']:
                title = element['weekTitle']
                print(title)
                assert " 共 24 周" in title

        # # 断言有底部资源位，因时间不断变化，运营位会变成毕业证书，不适用
        # assert '拓展推荐' in str(res)

    def test_home_ma(self):
        """
        已购思维正价课用户，首页标题、顶部资源位、周主题、底部资源位展示无误
        """
        res = self.home_ma.api_get_v4_home(bid=self.b_ma_user, subject='MA')
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言首页标题展示：呱呱爱思考
        assert res['data']['roadmap']['info']['ttl'] == '呱呱爱思考'
        assert res['data']['roadmap']['info']['level'] == 'K1'
        # weekTitle=res['data']['roadmap']['elements']['0']
        # 断言顶部资源位：展示填写地址资源位
        # assert res['data']['roadmap']['elements'][0]['tips'][0]['title'] == '正式课课前准备'
        # assert res['data']['roadmap']['elements'][0]['tips'][1]['title'] == '引导关注公众号'
        # 断言学习进度第x/共24周
        for element in res['data']['roadmap']['elements']:
            if 'weekTitle' in element and element['weekTitle']:
                title = element['weekTitle']
                print(title)
                assert " 共 24 周" in title

        # 断言底部资源位展示成呱呱阅读
        # assert res['data']['roadmap']['elements'][1]['tips'][0][
        #            'target'] == 'JLGL://album-c?albumid=AlbumCIX001&source=v4_afterclass_recommendation'

    def test_home_enMix(self):
        """
        用户已购英语体验课+正价课，英语tab，首页标题、周主题、底部资源位展示无误
        """
        res = self.home_mix.api_get_v4_home(bid=self.b_mix_user, subject='GE')
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # # 断言首页标题展示：呱呱爱表达K1
        assert res['data']['roadmap']['info']['ttl'] == '呱呱爱表达(2021)'
        assert res['data']['roadmap']['info']['level'] == 'K1'
        # 断言顶部资源位：展示填写地址资源位
        # assert res['data']['roadmap']['elements'][0]['tips'][0]['title'] == '正式课课前准备'
        # assert res['data']['roadmap']['elements'][0]['tips'][1]['title'] == '引导关注公众号'
        # 断言顶部资源位：专享试听内容
        # assert res['data']['roadmap']['elements'][1]['tips'][0][
        #            'title'] == '拓展推荐'
        # 断言周主题展示成
        for element in res['data']['roadmap']['elements']:
            if 'weekTitle' in element and element['weekTitle']:
                title = element['weekTitle']
                print(title)
                assert " 共 24 周" in title

        # 断言底部资源位展示成呱呱阅读
        # assert res['data']['roadmap']['elements'][2]['tips'][0][
        #            'target'] == 'JLGL://album-c?albumid=AlbumCIX001&source=v4_afterclass_recommendation'

    def test_home_maMix(self):
        """
        用户已购（英语+思维）体验课+正价课，思维tab，首页标题、顶部资源位（已开课无资源位）、周主题、底部资源位展示无误
        """
        res = self.home_mix.api_get_v4_home(bid=self.b_mix_user, subject='MA')
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言首页标题展示：呱呱爱表达K1
        assert res['data']['roadmap']['info']['ttl'] == '呱呱爱思考'
        assert res['data']['roadmap']['info']['level'] == 'K1'
        # 断言顶部资源位：展示填写地址资源位
        # assert res['data']['roadmap']['elements'][0]['tips'][0]['title'] == '正式课课前准备'
        # assert res['data']['roadmap']['elements'][0]['tips'][1]['title'] == '引导关注公众号'
        # 断言学习进度第x/共24周
        assert " 共 24 周" in res['data']['roadmap']['elements'][0]['weekTitle']
        # 断言底部资源位展示成呱呱阅读
        # assert res['data']['roadmap']['elements'][0]['tips'][0][
        #            'title'] == '拓展推荐'

    def test_home_diploma(self):
        """
        级别全部完课，正常展示毕业证书
        """
        res = self.home_mix.api_get_v4_home(bid=self.b_mix_user, subject='MA')
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言有毕业证书卡片
        assert res['data']['roadmap']['elements'][1]['diploma'][
                   'image'] == 'https://qiniucdn.jiliguala.com/sc/graduationnew/image_graduation_unavailable.png'
        # 断言有学习下一级别按钮
        assert res['data']['roadmap']['elements'][1]['diploma']['guideText'] == '学习下一级别'

    def test_home_y(self):
        """
         用户已购年课正价课，英语tab，首页标题、周主题 展示无误
        """
        res = self.home_y.api_get_v4_home(bid=self.b_y_user)
        print(res)
        # # 断言接口返回成功
        assert res['code'] == 0
        #  断言首页标题展示：呱呱英语体系全年伴学班
        assert res['data']['roadmap']['info']['ttl'] == '呱呱英语体系全年伴学班'
        assert res['data']['roadmap']['info']['level'] == 'Y1'
        assert " 共 48 周" in res['data']['roadmap']['elements'][0]['weekTitle']

    def test_home_yx(self):
        """
         用户已购年课正价课，英语tab，首页标题、周主题 展示无误
        """
        res = self.home_y.api_get_v4_home(bid=self.b_y_user)
        print(res)
        # # 断言接口返回成功
        assert res['code'] == 0
        #  断言首页标题展示：呱呱英语体系全年伴学班
        assert res['data']['roadmap']['info']['ttl'] == '呱呱英语体系全年伴学班'
        assert res['data']['roadmap']['info']['level'] == 'Y1'
        assert " 共 48 周" in res['data']['roadmap']['elements'][0]['weekTitle']