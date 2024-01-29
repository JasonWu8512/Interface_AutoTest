# -*- coding: utf-8 -*-
# @Time : 2022/7/18 1:26 下午
# @Author : anna

import pytest

from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.ShoppingTab
class TestLessonBuy(object):
    """
    购买详情页
    """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        agent = cls.config['agent']['ios_11.12.3']
        cls.trial = UserProperty(cls.config['shoppingtab']['ge_9.9_notpaid'])  # 体验课
        cls.enBag = UserProperty(cls.config['shoppingtab']['old_9.9_inside'])  # 大包课
        cls.formal_03 = UserProperty(cls.config['shoppingtab']['ge_9.9_outside'])  # 3.0课程
        cls.formal_01 = UserProperty(cls.config['shoppingtab']['original_user_rebuy'])  # 1.5课
        cls.formal_02 = UserProperty(cls.config['shoppingtab']['original01_user_rebuy'])  # 2.5正价课
        cls.ggr = UserProperty(cls.config['shoppingtab']['ggr_user'])  # 呱呱阅读卡
        cls.expand = UserProperty(cls.config['shoppingtab']['expand_user'])  # 推荐趣味拓展
        cls.disney = UserProperty(cls.config['shoppingtab']['disney_user'])  # 推荐迪士尼
        cls.ma = UserProperty(cls.config['shoppingtab']['ma_9.9_user'])  # 思维9.9
        cls.maBag = UserProperty(cls.config['shoppingtab']['ma_9.9_rebuy'])  # 思维大包

        # 体验课
        cls.buy_trial = ApiSuper(cls.trial.basic_auth, agent)
        # 英语大包课
        cls.buy_enBag = ApiSuper(cls.enBag.basic_auth, agent)
        cls.buy_formal_03 = ApiSuper(cls.formal_03.basic_auth, agent)
        cls.buy_formal_01 = ApiSuper(cls.formal_01.basic_auth, agent)
        cls.buy_formal_02 = ApiSuper(cls.formal_02.basic_auth, agent)
        cls.buy_ggr = ApiSuper(cls.ggr.basic_auth, agent)
        cls.buy_expand = ApiSuper(cls.expand.basic_auth, agent)
        cls.buy_disney = ApiSuper(cls.disney.basic_auth, agent)
        cls.buy_ma = ApiSuper(cls.ma.basic_auth, agent)
        cls.buy_maBag = ApiSuper(cls.maBag.basic_auth, agent)
        cls.source = "shopping_tab"

    def test_buy_trial(self):
        """体验课购买详情页"""
        res = self.buy_trial.api_get_lessonbuy(self.source, "K1GETC")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言接口返回体验课spuid：L1TC
        assert res['data']['display_items'][0]['_id'] == 'L1TC'

    def test_buy_enBag(self):
        """英语大包课购买详情页"""
        res = self.buy_maBag.api_get_lessonbuy(self.source, "F1_S1-6_WITHDISCOUNT")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：F1_S1-6_WITHDISCOUNT
        assert res['data']['display_items'][0]['_id'] == 'F1_S1-6_WITHDISCOUNT'

    def test_buy_formal_03(self):
        """3.0课程购买详情页"""
        res = self.buy_formal_03.api_get_lessonbuy(self.source, "S1GE_W1-6")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：S1GE_W1-6
        assert res['data']['display_items'][0]['_id'] == 'S1GE_W1-6'

    def test_buy_formal_01(self):
        """1.5课程详情页"""
        res = self.buy_formal_01.api_get_lessonbuy(self.source, "L2XX_L2XX_L3XX")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：L2XX_L2XX_L3XX
        assert res['data']['display_items'][1]['_id'] == 'L2XX_L3XX'

    def test_buy_formal_02(self):
        """2.5课程详情页"""
        res = self.buy_formal_02.api_get_lessonbuy(self.source, "K2GE")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：K2GE
        assert res['data']['display_items'][0]['_id'] == 'K2GE'

    def test_buy_ggr(self):
        """呱呱阅读购买页"""
        res = self.buy_ggr.api_get_lessonbuy(self.source, "GGRVIP_Purchase_01")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：GGRVIP_Purchase_01
        assert res['data']['display_items'][0]['_id'] == 'GGRVIP_1YearPurchase_01_SGU'

    def test_buy_expand(self):
        """趣味拓展"""
        res = self.buy_expand.api_get_lessonbuy(self.source, "AlbumCIX001")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：AlbumCIX001
        assert res['data']['display_items'][0]['_id'] == 'AlbumCIX001'

    def test_buy_disney(self):
        """迪士尼课"""
        res = self.buy_disney.api_get_lessonbuy(self.source, "BundleCDS001")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：BundleCDS001
        assert res['data']['display_items'][0]['_id'] == 'BundleCDS001'

    def test_buy_ma(self):
        """思维体验课"""
        res = self.buy_ma.api_get_lessonbuy(self.source, "K3MATC_99")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：K3MATC_99
        assert res['data']['display_items'][0]['_id'] == 'K3MATC_99'

    def test_buy_maBag(self):
        """思维大包课"""
        res = self.buy_maBag.api_get_lessonbuy(self.source, "K1MA_K6MA")
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言详情页展示的spu是：K1MA_K6MA
        assert res['data']['display_items'][0]['_id'] == 'K1MA_K6MA'
