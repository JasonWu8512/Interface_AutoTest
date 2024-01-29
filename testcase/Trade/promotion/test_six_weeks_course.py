# -*- coding: utf-8 -*-
# @Time: 2021/6/22 7:01 下午
# @Author: ian.zhou
# @File: test_six_weeks_course
# @Software: PyCharm

import time
import pytest
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.common.UserProperty import UserProperty
from business.Trade.promotion.ApiPromotion import ApiPromotion
from business.mysqlQuery import EshopQuery
from testcase.Trade.common import CommodityCommon, OrderCommon

@pytest.mark.Trade
@pytest.mark.promotion
@pytest.mark.TradeCommodity
@pytest.mark.TradeOrder
class TestSixWeeksCourse:
    """优惠中心6周课优惠相关用例"""

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        # 获取管理后台用户token
        a_user = cls.config['eshop']['admin']['user']
        a_pwd = cls.config['eshop']['admin']['pwd']
        a_token = ApiAdminAuth().api_login(username=a_user, password=a_pwd).get('data').get('token')
        # 获取C端用户token
        c_user = cls.config['eshop']['user']
        basic_auth = UserProperty(mobile=c_user).basic_auth
        cls.uid = UserProperty(mobile=c_user).user_id
        cls.c_promotion = ApiPromotion()
        cls.eshop_query = EshopQuery()
        cls.commodity_common = CommodityCommon(a_token=a_token)
        cls.order_common = OrderCommon(c_user=c_user)

    def setup(self):
        """用例开始前删除优惠中心用户学科记录、订单快照表双月课订单避免干扰"""
        self.eshop_query.delete_user_subject(user_no=self.uid)
        self.eshop_query.delete_user_promtion_order_snap(user_no=self.uid)

    """
    subject_type: 
    FORMAL_COURSE:正价课, TRIAL_COURSE:体验课, FORMAL_TEACHING_AIDS:正价课教具, SIX_WEEK_COURSE：双月课
    course_type: 
    ENGLISH:英语, LOGIC:思维, CHINESE:语文
    """

    def test_6weeks_course_discount(self, get_commodity):
        """
        6周课优惠：用户购买6周课商品无优惠
        :return:
        """
        # 验证用户购买6周课商品无优惠
        sgu_no_6week_course = get_commodity['sgu_six_weeks']['ge']['no']
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_6week_course)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        # 断言优惠前价格是否等于优惠后价格，优惠金额为0
        assert origin_price == discount_price
        assert discount_total == 0

    def test_6weeks_course_discount_1(self, get_commodity):
        """
        6周课优惠：用户未购买A学科6周课，购买A学科不享受6周课优惠商品无优惠
        :return:
        """
        # 验证用户未购买A学科6周课，购买A学科不享受6周课优惠商品无优惠
        sgu_no_6week_system = get_commodity['sgu_system']['ge']['no']
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_6week_system)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        # 断言优惠前价格是否等于优惠后价格，优惠金额为0
        assert origin_price == discount_price
        assert discount_total == 0

    def test_6weeks_course_discount_2(self, get_commodity):
        """
        6周课优惠：用户未购买A学科6周课，购买A学科享受6周课优惠商品无优惠
        :return:
        """
        # 配置英语正价课可以享受6周课优惠
        sgu_no_6week_system = get_commodity['sgu_system']['ge']['no']
        self.eshop_query.set_6week_system_course(sgu_no=sgu_no_6week_system)
        # 验证用户未购买A学科6周课，购买A学科享受6周课优惠商品无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_6week_system)
        # 断言前还原配置，避免断言失败导致数据未还原
        self.eshop_query.delete_6week_system_course(sgu_no=sgu_no_6week_system)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        # 断言优惠前价格是否等于优惠后价格，优惠金额为0
        assert origin_price == discount_price
        assert discount_total == 0

    def test_6weeks_course_discount_3(self, get_commodity):
        """
        6周课优惠：购买A学科双月课
        """
        # 创建6周课订单并支付
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_six_weeks']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no)
        self.order_no, self.charge_id = detail[0], detail[1]
        time.sleep(3)
        # 查询用户学科信息
        user_subject_pay = self.eshop_query.query_user_subject(user_no=self.uid)
        # 断言学科信息是否正确
        assert len(user_subject_pay) == 1
        assert user_subject_pay[0]['subject_type'] == 1
        assert user_subject_pay[0]['subject_course_type'] == 4
        # 查询用户orders订单表
        user_order = self.eshop_query.query_user_order(order_no=self.order_no)
        # 查询用户6周课快照表订单
        user_order_snap_pay = self.eshop_query.query_user_order_snap(user_no=self.uid)
        # 断言6周课快照表订单记录是否正确
        assert len(user_order_snap_pay) == 1
        assert user_order_snap_pay[0]['subject_type'] == 1
        assert user_order_snap_pay[0]['subject_course_type'] == 4
        assert user_order_snap_pay[0]['gua_dou_price'] == user_order[0]['gua_dou_price']
        assert user_order_snap_pay[0]['pay_price'] == user_order[0]['pay_price']

        """
        6周课优惠：有A学科6周课订单，购买B学科不享受B学科6周课优惠SGU无优惠
        """
        # 验证有A学科6周课订单，购买B学科不享受B学科6周课优惠SGU无优惠
        sgu_no_6week_system_ma = get_commodity['sgu_system']['ma']['no']
        res_ma_1 = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_6week_system_ma)
        origin_price_ma_1 = res_ma_1['data']['prePromotionPrice']
        discount_price_ma_1 = res_ma_1['data']['postPromotionPrice']
        discount_total_ma_1 = res_ma_1['data']['activityPrice']
        # 断言购买该SGU无优惠
        assert origin_price_ma_1 == discount_price_ma_1
        assert discount_total_ma_1 == 0

        """
        6周课优惠：有A学科6周课订单，购买B学科享受B学科6周课优惠SGU无优惠
        """
        # 配置B学科可以享受6周课优惠SGU
        self.eshop_query.set_6week_system_course(sgu_no=sgu_no_6week_system_ma)
        # 验证有A学科6周课订单，购买B学科享受B学科6周课优惠SGU无优惠
        res_ma_2 = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_6week_system_ma)
        # 断言前还原配置，避免断言失败导致数据未还原
        self.eshop_query.delete_6week_system_course(sgu_no=sgu_no_6week_system_ma)
        origin_price_ma_2 = res_ma_2['data']['prePromotionPrice']
        discount_price_ma_2 = res_ma_2['data']['postPromotionPrice']
        discount_total_ma_2 = res_ma_2['data']['activityPrice']
        # 断言购买该SGU无优惠
        assert origin_price_ma_2 == discount_price_ma_2
        assert discount_total_ma_2 == 0

        """
        6周课优惠：有A学科6周课订单，购买A学科不享受A学科6周课优惠SGU无优惠
        """
        # 验证有A学科6周课订单，购买A学科不享受A学科6周课优惠SGU无优惠
        sgu_no_6week_system = get_commodity['sgu_system']['ge']['no']
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_6week_system)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        # 断言购买该SGU无优惠
        assert origin_price == discount_price
        assert discount_total == 0

        """
        6周课优惠：有A学科6周课订单，购买A学科享受A学科6周课优惠SGU享受A学科6周课优惠
        """
        # 配置A学科SGU可以享受6周课优惠
        self.eshop_query.set_6week_system_course(sgu_no=sgu_no_6week_system)
        # 购买享受A学科6周课优惠的SGU
        detail_system = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no_6week_system)
        self.order_no_system, self.charge_id_system = detail_system[0], detail_system[1]
        time.sleep(3)
        # 删除A学科SGU可以享受A学科6周课优惠配置
        self.eshop_query.delete_6week_system_course(sgu_no=sgu_no_6week_system)
        # 查询用户orders订单表购买使用6周课优惠订单
        user_order_6week_system = self.eshop_query.query_user_order(order_no=self.order_no_system)
        # 断言实付金额+呱豆金额是否是SGU售价减去6周课订单金额
        assert user_order_6week_system[0]['pay_price'] + user_order_6week_system[0]['gua_dou_price'] == \
               user_order_6week_system[0]['price'] - user_order_snap_pay[0]['gua_dou_price'] - \
               user_order_snap_pay[0]['pay_price']
        # 购买使用A学科6周课优惠SGU后查询用户6周课快照表订单
        user_order_snap_system = self.eshop_query.query_user_order_snap(user_no=self.uid)
        # 断言用户的6周课快照表订单relate_order_no是否记录正价课订单号
        assert len(user_order_snap_system) == 1
        assert user_order_snap_system[0]['relate_order_no'] == self.order_no_system

        """
        6周课优惠：用户对使用A学科6周课优惠的订单全部退款
        """
        # 对使用6周课订单优惠的正价课订单进行全部退款
        self.order_common.order_refund_and_remove(order_no=self.order_no_system)
        time.sleep(3)
        # 退款后查询用户6周课快照表订单
        user_order_snap_refund_system = self.eshop_query.query_user_order_snap(user_no=self.uid)
        # 断言用户的6周课快照表订单relate_order_no是否删除
        assert len(user_order_snap_refund_system) == 1
        assert user_order_snap_refund_system[0]['relate_order_no'] == None

        """
        6周课优惠：用户对6周课订单全部退款
        """
        # 对6周课订单进行全部退款
        self.order_common.order_refund_and_remove(order_no=self.order_no)
        time.sleep(3)
        # 退款后查询用户6周课学科记录
        user_subject_refund = self.eshop_query.query_user_subject(user_no=self.uid)
        # 断言6周课学科记录是否删除
        assert len(user_subject_refund) == 0
        # 退款后查询用户6周课快照表订单
        user_order_snap_refund = self.eshop_query.query_user_order_snap(user_no=self.uid)
        # 断言用户的6周课快照表订单是否删除
        assert len(user_order_snap_refund) == 0
