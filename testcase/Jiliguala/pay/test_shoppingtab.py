# -*- coding: utf-8 -*-
# @Time : 2022/7/18 1:26 下午
# @Author : anna
from time import sleep

import pytest

from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.Jiliguala.pay.ApiShoppingTab import ApiShoppingTab
from business.Jiliguala.user.ApiUser import ApiUser
from business.businessQuery import usersQuery, pingxxorderQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.ShoppingTab
class TestShoppingTab(object):
    """
       购买tab，针对11.4以上版本
       """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.user_notpaid = UserProperty(cls.config['shoppingtab']['ge_9.9_notpaid'])  # 未购9.9
        cls.user_old_inside = UserProperty(cls.config['shoppingtab']['old_9.9_inside'])  # 已购9.9，宝贝年龄>3岁且在运营期内
        cls.user_young_inside = UserProperty(cls.config['shoppingtab']['young_9.9_inside'])  # 已购9.9，宝贝年龄<3岁且在运营期内
        cls.user_outside = UserProperty(cls.config['shoppingtab']['ge_9.9_outside'])  # 已购9.9且在运营期外
        cls.sixweek_rebuy01 = UserProperty(
            cls.config['shoppingtab']['sixweek01_user_rebuy'])  # 首购双月课用户(S1GE_W1-6_SPU)，复购
        cls.sixweek_rebuy02 = UserProperty(
            cls.config['shoppingtab']['sixweek02_user_rebuy'])  # 首购双月课用户(F2GE_W1-6_SPU)，复购
        cls.original_rebuy = UserProperty(cls.config['shoppingtab']['original_user_rebuy'])  # 首购1.5正价课用户，复购
        cls.original01_rebuy = UserProperty(cls.config['shoppingtab']['original01_user_rebuy'])  # 首购2.5正价课用户，复购
        cls.original_user_refund = UserProperty(cls.config['shoppingtab']['original_user_refund'])  # 首购双月课，后退款
        cls.user_ggr = UserProperty(cls.config['shoppingtab']['ggr_user'])  # 推荐呱呱阅读卡
        cls.user_expand = UserProperty(cls.config['shoppingtab']['expand_user'])  # 推荐趣味拓展
        cls.user_disney = UserProperty(cls.config['shoppingtab']['disney_user'])  # 推荐迪士尼
        cls.user_ma = UserProperty(cls.config['shoppingtab']['ma_9.9_user'])  # 推荐思维9.9
        cls.user_ma_rebuy = UserProperty(cls.config['shoppingtab']['ma_9.9_rebuy'])  # 推荐思维大包

        # 获取不同用户的第一个宝贝id
        cls.notpaid = cls.user_notpaid.babies["_id"]
        cls.old_inside = cls.user_old_inside.babies["_id"]
        cls.young_inside = cls.user_young_inside.babies["_id"]
        cls.outside = cls.user_outside.babies["_id"]
        cls.sixweek01 = cls.sixweek_rebuy01.babies["_id"]
        cls.sixweek02 = cls.sixweek_rebuy02.babies["_id"]
        cls.original = cls.original_rebuy.babies["_id"]
        cls.original01 = cls.original01_rebuy.babies["_id"]
        cls.original_refund = cls.original_user_refund.babies["_id"]
        cls.ggr = cls.user_ggr.babies["_id"]
        cls.expand = cls.user_expand.babies["_id"]
        cls.disney = cls.user_disney.babies["_id"]
        cls.ma = cls.user_ma.babies["_id"]
        cls.ma_rebuy = cls.user_ma_rebuy.babies["_id"]

        cls.shopping_tab_notpaid = ApiShoppingTab(cls.user_notpaid.basic_auth,
                                                  cls.config['version']['ver11.12.3'],
                                                  cls.config['agent']['ios_11.12.3'])
        # auth=cls.user_notpaid.basic_auth
        # print(cls.user_notpaid)
        # print(auth)
        cls.shopping_tab_notpaid = ApiShoppingTab(cls.user_notpaid.basic_auth,
                                                  cls.config['version']['ver11.12.3'],
                                                  cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_old_inside = ApiShoppingTab(cls.user_old_inside.basic_auth,
                                                     cls.config['version']['ver11.12.3'],
                                                     cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_young_inside = ApiShoppingTab(cls.user_young_inside.basic_auth,
                                                       cls.config['version']['ver11.12.3'],
                                                       cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_user_outside = ApiShoppingTab(cls.user_outside.basic_auth,
                                                       cls.config['version']['ver11.12.3'],
                                                       cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_sixweek_rebuy01 = ApiShoppingTab(cls.sixweek_rebuy01.basic_auth,
                                                          cls.config['version']['ver11.12.3'],
                                                          cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_sixweek_rebuy02 = ApiShoppingTab(cls.sixweek_rebuy02.basic_auth,
                                                          cls.config['version']['ver11.12.3'],
                                                          cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_original_rebuy = ApiShoppingTab(cls.original_rebuy.basic_auth,
                                                         cls.config['version']['ver11.12.3'],
                                                         cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_origina01_rebuy = ApiShoppingTab(cls.original01_rebuy.basic_auth,
                                                          cls.config['version']['ver11.12.3'],
                                                          cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_original_refund = ApiShoppingTab(cls.original_user_refund.basic_auth,
                                                          cls.config['version']['ver11.12.3'],
                                                          cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_user_ggr = ApiShoppingTab(cls.user_ggr.basic_auth,
                                                   cls.config['version']['ver11.12.3'],
                                                   cls.config['agent']['ios_11.12.3'], )
        cls.shopping_tab_user_expand = ApiShoppingTab(cls.user_expand.basic_auth,
                                                      cls.config['version']['ver11.12.3'],
                                                      cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_user_disney = ApiShoppingTab(cls.user_disney.basic_auth,
                                                      cls.config['version']['ver11.12.3'],
                                                      cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_ma = ApiShoppingTab(cls.user_ma.basic_auth,
                                             cls.config['version']['ver11.12.3'], cls.config['agent']['ios_11.12.3'])
        cls.shopping_tab_ma_rebuy = ApiShoppingTab(cls.user_ma_rebuy.basic_auth,
                                                   cls.config['version']['ver11.12.3'],
                                                   cls.config['agent']['ios_11.12.3'])

    def test_tab_notpaid(self):
        """未购9.9，推荐9.9"""
        res = self.shopping_tab_notpaid.api_get_shopping_tab(bid=self.notpaid)
        # res = self.shopping_tab_notpaid.api_get_shopping_tab(bid='753f6509426c4e02947202d99af8debc')
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 未购9.9，购买tab推荐9.9
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'K1GETC_SPU'

    # def test_tab_old_inside(self):
    #     """年龄3+，已购9.9，运营期内推荐大包，F1_S1-6_WITHDISCOUNT_SPU"""
    #     res = self.shopping_tab_old_inside.api_get_shopping_tab(bid=self.user_old_inside)
    #     print(res)
    #     # 断言接口返回成功
    #     assert res['code'] == 0
    #     # 未购9.9，购买tab推荐9.9
    #     assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'F1_S1-6_WITHOUTDISCOUNT_SPU'

    def test_tab_young_inside(self):
        """已购9.9，运营期内推荐大包:F1_S1-6_WITHDISCOUNT_SPU"""
        # 先购买英语体验课
        itemId = 'L1TC'
        # 生成随机用户
        user = ApiUser()
        mobile = user.get_mobile()
        print(mobile)
        # 注册新账号
        newUser = user.api_register(mobile)
        # 体验课账号信息
        trial_user = UserProperty(mobile)
        user_id = trial_user.user_id
        # 充瓜豆
        usersQuery().update_users_guadouBalance(uid=user_id, guadouBalance=90000000)
        # 体验课信息授权，实例化类
        # agent = 'niuwa/11.12.3 (iPhone; iOS 14.0.1; Scale/2.00)'
        agent = self.config['agent']['ios_11.12.3']
        trial_pay = ApiSuper(trial_user.basic_auth, agent)
        # 获取新用户bid
        trial_bid = trial_user.babies["_id"]
        res01 = trial_pay.api_post_purchase(trial_bid, itemId, "true", "guadou")
        print(res01)
        oid = res01['data']['oid']
        trial_pay.api_get_order(oid)
        trial_pay.api_post_result(oid)
        sleep(10)
        # 进入购买tab
        # version=111201&platform=5&model=0
        version = self.config['version']['ver11.12.3']
        res = ApiShoppingTab(trial_user.basic_auth, version, agent).api_get_shopping_tab(bid=trial_bid)
        print(res)

        # 断言接口返回成功
        assert res['code'] == 0
        # 已购9.9，运营期内推荐大包
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'F1_S1-6_WITHOUTDISCOUNT_SPU'

    def test_tab_user_outside(self):
        """已购9.9，运营期外，推荐128六周课（S1GE_W1-6_SPU）"""
        res = self.shopping_tab_user_outside.api_get_shopping_tab(bid=self.outside)
        print(res)

        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐的是六周课S1GE_W1-6_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'S1GE_W1-6_SPU'

    def test_tab_six01_rebuy(self):
        """首购双月课用户(S1GE_W1-6_SPU)，推荐剩余大包：S1GE_W7-24_S2_S6_SPU"""
        res = self.shopping_tab_sixweek_rebuy01.api_get_shopping_tab(bid=self.sixweek01)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐的是六周课后大包：S1GE_W7-24_S2_S6_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'S1GE_W7-24_S2_S6_SPU'

    def test_tab_six02_rebuy(self):
        """首购双月课用户(F2GE_W1-6_SPU)，推荐剩余大包：F2GE_W7-24_S1_S6_SPU"""
        res = self.shopping_tab_sixweek_rebuy02.api_get_shopping_tab(bid=self.sixweek02)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐的是六周课后大包：F2GE_W7-24_S2_S6_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'F2GE_W7-24_S1_S6_SPU'

    def test_tab_original_rebuy(self):
        """首购1.5 L1XX后复购，推荐后续课程：L2XX_L2XX_L3XX_SP"""
        res = self.shopping_tab_original_rebuy.api_get_shopping_tab(bid=self.original)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐的1.5接下来的级别，L2XX_L2XX_L3XX_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'L2XX_L2XX_L3XX_SPU'

    def test_tab_original01_rebuy(self):
        """首购2.5 k1GE后复购，推荐后续课程：K2GE_SPU"""
        res = self.shopping_tab_origina01_rebuy.api_get_shopping_tab(bid=self.original01)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐的2.5接下来的级别，K2GE_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'K2GE_SPU'

    def test_tab_original_refund(self):
        """首购双月课后退款，继续推荐9.9"""
        res = self.shopping_tab_original_refund.api_get_shopping_tab(bid=self.original_refund)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐9.9，K1GETC_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'K1GETC_SPU'

    def test_tab_math(self):
        """购买英语9.9运营期后，推荐思维9.9"""
        res = self.shopping_tab_ma.api_get_shopping_tab(bid=self.ma)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐思维9.9，K3MATC_99_SPU
        assert res['data']['lessonList'][0]['lessonDetails'][1]['commodityNo'] == 'K3MAFC_0_APP_SPU'

    def test_tab_mathBag(self):
        """购买思维9.9后，推荐思维大包"""
        res = self.shopping_tab_ma_rebuy.api_get_shopping_tab(bid=self.ma_rebuy)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言推荐思维大包，K1GETC_SPU
        assert res['data']['lessonList'][2]['lessonDetails'][0]['commodityNo'] == 'K1MA_K6MA_SPU'

    def test_tab_ggr(self):
        """已购9.9且符合条件，趣味拓展tab推荐内容：GGRVIP_Purchase_01_SPU、AlbumCIX001_SPU、BundleCDS001_SPU"""
        res = self.shopping_tab_user_ggr.api_get_shopping_tab(bid=self.ggr)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        print(res)
        # 断言趣味拓展tab，第一个推荐的是呱呱阅读卡
        assert res['data']['lessonList'][3]['lessonDetails'][0]['commodityNo'] == 'GGRVIP_Purchase_SPU'

        # 断言趣味拓展tab，第二个推荐的是趣味拓展课
        assert res['data']['lessonList'][3]['lessonDetails'][1]['commodityNo'] == 'AlbumCIX001_SPU'

        # 断言趣味拓展tab，第三个推荐的是趣味拓展课
        assert res['data']['lessonList'][3]['lessonDetails'][2]['commodityNo'] == 'BundleCDS001_SPU'

    def test_tab_kx(self):
        """已购9.9且符合条件，科学百科tab推荐内容：B_BKanimal_SPU"""
        res = self.shopping_tab_user_ggr.api_get_shopping_tab(bid=self.ggr)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言科学百科tab，推荐趣味百科
        assert res['data']['lessonList'][4]['lessonDetails'][0]['commodityNo'] == 'B_BKanimal_SPU'

    def test_tab_gx(self):
        """已购9.9且符合条件，国学素养tab推荐内容：AGXcity_SPU"""
        res = self.shopping_tab_user_ggr.api_get_shopping_tab(bid=self.ggr)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言国学素养tab，推荐国学素养
        assert res['data']['lessonList'][5]['lessonDetails'][0]['commodityNo'] == 'AGXcity_SPU'
