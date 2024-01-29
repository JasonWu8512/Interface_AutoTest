# -*- coding: utf-8 -*-
# @Time : 2021/7/15 1:26 下午
# @Author : wanjun

import pytest

from business.Jiliguala.pay.ApiShoppingTab import ApiShoppingTab
from business.businessQuery import usersQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.pay
class TestShoppingTab6WeeksFirstBuy:
    """
       双月课新机转购买tab商品展示--首购，针对11.4以上版本
       """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.user_first_buy = UserProperty(cls.config['six_weeks']['six_weeks_user_first_buy'])  # 配置文件读取首购测试账号
        cls.user_re_buy = UserProperty(cls.config['six_weeks']['six_weeks_user_re_buy'])    # 配置文件读取复购测试账号
        cls.user_refunded = UserProperty(cls.config['six_weeks']['six_weeks_user_refunded'])    # 配置文件读取退款测试账号
        cls.bid_first_buy = cls.user_first_buy.babies["_id"]  # 获取用户首个宝贝id
        cls.bid_re_buy = cls.user_re_buy.babies["_id"]  # 获取用户首个宝贝id
        cls.bid_user_refunded = cls.user_refunded.babies["_id"]  # 获取用户首个宝贝id
        cls.shopping_tab_user_first_buy = ApiShoppingTab(cls.user_first_buy.basic_auth, cls.config['version']['ver11.6'],
                                                         cls.config['agent']['ios_11.6'])
        cls.shopping_tab_user_re_buy = ApiShoppingTab(cls.user_re_buy.basic_auth, cls.config['version']['ver11.6'],
                                                      cls.config['agent']['ios_11.6'])
        cls.shopping_tab_user_refunded = ApiShoppingTab(cls.user_refunded.basic_auth, cls.config['version']['ver11.6'],
                                                        cls.config['agent']['ios_11.6'])

    @classmethod
    def teardown_class(cls):
        pass

    def test_tab_f2ge_first_buy(self):
        """首购-新机转（双月课）用户商品展示"""
        res = self.shopping_tab_user_first_buy.api_get_shopping_tab(bid=self.bid_first_buy)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言双月课新机转首购用户购买tab第一个商品为F2GE_W1-6_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'F2GE_W1-6_SPU'
        # 断言双月课新机转首购用户购买tab第二个商品为F2GE_S6GE_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][1]['commodityNo'] == 'F2GE_S6GE_SPU'

    def test_tab_f2ge_re_buy(self):
        """复购-新机转（双月课）用户商品展示"""
        res = self.shopping_tab_user_re_buy.api_get_shopping_tab(bid=self.bid_re_buy)

        # 断言接口返回成功
        assert res['code'] == 0
        # 断言双月课新机转复购用户购买tab第一个商品为F2GE_W7-24_S1_S6_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'F2GE_W7-24_S1_S6_SPU'

    def test_tab_f2ge_refunded(self):
        """退款-新机转（双月课）用户商品展示"""
        res = self.shopping_tab_user_refunded.api_get_shopping_tab(bid=self.bid_user_refunded)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言双月课新机转首购用户购买tab第一个商品为F2GE_W1-6_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'F2GE_W1-6_SPU'
        # 断言双月课新机转首购用户购买tab第二个商品为F2GE_S6GE_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][1]['commodityNo'] == 'F2GE_S6GE_SPU'


