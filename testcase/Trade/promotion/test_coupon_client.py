#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/21 2:30 下午
# @Author : liang_li
# @Site : 
# @File : test_coupon_client.py
# @Software: PyCharm

import time
import random
import pytest
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.common.UserProperty import UserProperty
from business.Trade.promotion.ApiPromotion import ApiPromotion
from business.mysqlQuery import EshopQuery
from testcase.Trade.common import CommodityCommon, OrderCommon
from business.Trade.promotion.ApiCouponAdmin import ApiCouponAdmin
from utils.format.format import dateToTimeStamp
from business.Trade.promotion.ApiCouponClient import ApiCouponClient

@pytest.mark.Trade
@pytest.mark.promotion
@pytest.mark.TradeCommodity
@pytest.mark.TradeOrder
class TestSixWeeksCourse:
    """优惠中心-C端优惠券相关用例"""

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
        cls.coupon_admin = ApiCouponAdmin(token=a_token)
        cls.order_common = OrderCommon(c_user=c_user)
        cls.c_coupon = ApiCouponClient()

    def setup(self):
        """用例开始前删除优惠中心用户优惠券避免干扰"""
        self.eshop_query.delete_user_coupon(user_no=self.uid)

    @pytest.fixture(scope='class')
    def create_coupon_min(self, get_commodity):
        """新增一个小额优惠券"""
        # 生成四位随机字符串
        intro_set = [chr(i) for i in range(97, 123)]
        intro_value = "".join(random.sample(intro_set, 4))
        # 将生成的随机字符串与活动命名拼接成intro参数
        intro = f'优惠券自动化测试{intro_value}'
        # 新增优惠券
        sgu_no = [get_commodity['sgu_system']['ge']['no'], get_commodity['sgu_system']['ma']['no']]
        self.coupon_admin.api_create_edit_coupon(couponName=intro, describes=intro, maxNum=20,
                                                 startTime=dateToTimeStamp(), endTime=dateToTimeStamp(day=1),
                                                 reward=600, strategyCondition=10, refIds=sgu_no, redirectUrl=intro)
        # 查询新增的优惠券
        res = self.eshop_query.query_coupon(redirect_url=intro)
        return res

    @pytest.fixture(scope='class')
    def create_coupon_max(self, get_commodity):
        """新增一个大额优惠券"""
        # 生成四位随机字符串
        intro_set = [chr(i) for i in range(97, 123)]
        intro_value = "".join(random.sample(intro_set, 4))
        # 将生成的随机字符串与活动命名拼接成intro参数
        intro = f'优惠券自动化测试{intro_value}'
        # 新增优惠券
        sgu_no = [get_commodity['sgu_system']['ge']['no'], get_commodity['sgu_system']['ma']['no']]
        self.coupon_admin.api_create_edit_coupon(couponName=intro, describes=intro, maxNum=20,
                                                 startTime=dateToTimeStamp(), endTime=dateToTimeStamp(day=1),
                                                 reward=900, strategyCondition=10, refIds=sgu_no, redirectUrl=intro)
        # 查询新增的优惠券
        res = self.eshop_query.query_coupon(redirect_url=intro)
        return res

    def test_coupon_discount_1(self, get_commodity):
        """
        优惠券：用户无优惠券时购买生成了优惠券的商品不可以使用优惠券
        """
        # 获取sgu_no
        sgu_no_ge = get_commodity['sgu_system']['ge']['no']
        # 调用优惠中心算价接口算价
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_ge)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        coupon_price = res['data']['couponPrice']
        # 断言优惠前价格是否等于优惠后价格，优惠金额为0
        assert origin_price == discount_price
        assert discount_total == 0
        assert coupon_price == 0

    def test_coupon_discount_2(self, create_coupon_min):
        """
        优惠券：给用户发放超量的优惠券，发放失败
        :return:
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        grant_user_coupon = self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=21)
        # 查询用户优惠券记录
        user_coupon = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 断言调用发放优惠券接口是否成功
        assert grant_user_coupon['status'] == 500
        assert grant_user_coupon['message'] == "909:优惠券剩余发放量不足!"
        assert len(user_coupon) == 0

    def test_coupon_discount_3(self, create_coupon_min):
        """
        优惠券：给用户发放下架的优惠券，发放失败
        :return:
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 下架优惠券
        self.coupon_admin.api_modify_coupon_status(couponId=coupon_id, isEnable=0)
        # 给用户发放优惠券
        grant_user_coupon = self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 上架优惠券，避免干扰后续用例
        self.coupon_admin.api_modify_coupon_status(couponId=coupon_id, isEnable=1)
        # 查询用户优惠券记录
        user_coupon = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 断言调用发放优惠券接口是否成功
        assert grant_user_coupon['status'] == 500
        assert grant_user_coupon['message'] == "910:该优惠券不可用!"
        assert len(user_coupon) == 0

    def test_coupon_discount_4(self, create_coupon_min):
        """
        优惠券：给用户发放优惠券，发放成功
        :return:
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        grant_user_coupon = self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 查询用户优惠券记录
        user_coupon = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 删除用户优惠券
        self.eshop_query.delete_user_coupon(user_no=self.uid)
        # 断言调用发放优惠券接口是否成功
        assert grant_user_coupon['code'] == 0
        assert len(user_coupon) == 1
        assert user_coupon[0]['status'] == 0

    def test_coupon_discount_5(self, get_commodity, create_coupon_min):
        """
        优惠券：用户拥有优惠券后购买不能使用该优惠券商品
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 获取不享受优惠的commodityNo
        sgu_no_ge = get_commodity['sgu_six_weeks']['ge']['no']
        # 调用优惠中心算价接口算价
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_ge)
        # 删除用户优惠券
        self.eshop_query.delete_user_coupon(user_no=self.uid)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        coupon_price = res['data']['couponPrice']
        # 断言优惠前价格是否等于优惠后价格，优惠金额为0
        assert origin_price == discount_price
        assert discount_total == 0
        assert coupon_price == 0

    def test_coupon_discount_6(self, get_commodity, create_coupon_min):
        """
        优惠券：已过期优惠券不能使用
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 查询用户优惠券记录
        user_coupon = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 更新优惠券过期时间等于开始时间
        end_at = user_coupon[0]['start_at']
        coupon_no = user_coupon[0]['coupon_no']
        sql = f'update coupon_grant set end_at ="{end_at}" where coupon_no ="{coupon_no}"'
        self.eshop_query.excute_eshop_promotion(sql)
        # 获取享受优惠券优惠的商品
        sgu_no_ge = get_commodity['sgu_system']['ge']['no']
        # 调用优惠中心算价接口算价
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_ge)
        # 删除用户优惠券
        self.eshop_query.delete_user_coupon(user_no=self.uid)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        coupon_price = res['data']['couponPrice']
        # 断言优惠前价格是否等于优惠后价格，优惠金额为0
        assert origin_price == discount_price
        assert discount_total == 0
        assert coupon_price == 0

    def test_coupon_discount_7(self, create_coupon_min):
        """
        优惠券：调用锁券接口锁券
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        print(coupon_id)
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 查询用户优惠券coupon_no
        res = self.c_coupon.api_coupon_user_query(userNo=self.uid)
        coupon_no = res['data'][0]['couponNo']
        # 调用锁券接口锁券
        self.c_coupon.api_coupon_user_lock(userNo=self.uid, couponNo=coupon_no, bizNo=self.uid)
        # 锁券后查询用户优惠券表
        user_grant = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 删除用户优惠券
        self.eshop_query.delete_user_coupon(user_no=self.uid)
        # 断言优惠券状态是否为已锁定
        assert user_grant[0]['status'] == 1

    def test_coupon_discount_8(self, create_coupon_min):
        """
        优惠券：调用解锁券接口解锁优惠券
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 查询用户优惠券coupon_no
        res = self.c_coupon.api_coupon_user_query(userNo=self.uid)
        coupon_no = res['data'][0]['couponNo']
        # 调用锁券接口锁券
        self.c_coupon.api_coupon_user_lock(userNo=self.uid, couponNo=coupon_no, bizNo=self.uid)
        # 调用解锁券接口解锁券
        self.c_coupon.api_coupon_user_unlock(userNo=self.uid, couponNo=coupon_no, bizNo=self.uid)
        # 解锁券后查询用户优惠券表
        user_grant = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 删除用户优惠券
        self.eshop_query.delete_user_coupon(user_no=self.uid)
        # 断言优惠券状态是否为已解锁
        assert user_grant[0]['status'] == 0

    def test_coupon_discount_9(self, create_coupon_min):
        """
        优惠券：调用核销券接口核销优惠券
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 查询用户优惠券coupon_no
        res = self.c_coupon.api_coupon_user_query(userNo=self.uid)
        coupon_no = res['data'][0]['couponNo']
        # 调用锁券接口锁券
        self.c_coupon.api_coupon_user_lock(userNo=self.uid, couponNo=coupon_no, bizNo=self.uid)
        # 调用核销券接口核销券
        self.c_coupon.api_coupon_user_verify(userNo=self.uid, couponNo=coupon_no, bizNo=self.uid)
        # 核销券后查询用户优惠券表
        user_grant = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 删除用户优惠券
        self.eshop_query.delete_user_coupon(user_no=self.uid)
        # 断言优惠券状态是否为已解锁
        assert user_grant[0]['status'] == 2

    def test_coupon_discount_10(self, get_commodity, create_coupon_min):
        """
        优惠券：用户拥有优惠券后购买可以使用该优惠券商品，支付成功
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 查询优惠券的金额
        coupon_strategy = self.eshop_query.query_coupon_strategy(coupon_id=coupon_id)
        coupon_reward = int(coupon_strategy[0]['reward'])
        # 获取享受优惠券优惠的商品
        sgu_no_ge = get_commodity['sgu_system']['ge']['no']
        # 调用优惠中心算价接口算价
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_ge)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        coupon_price = res['data']['couponPrice']
        # 断言优惠前价格是否等于优惠后价格
        assert coupon_price == coupon_reward
        assert origin_price == discount_price + coupon_price
        assert discount_total == 0
        # 使用优惠券下单并支付
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_system']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no)
        self.order_no, self.charge_id = detail[0], detail[1]
        time.sleep(3)
        # 使用优惠券下单支付后查询用户优惠券表
        user_grant = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 断言优惠券状态是否为已核销
        assert user_grant[0]['status'] == 2
        # 查询用户orders订单表
        user_order = self.eshop_query.query_user_order(order_no=self.order_no)
        # 对订单进行全部退款
        self.order_common.order_refund_and_remove(order_no=self.order_no)
        time.sleep(3)
        # 断言用户使用优惠券后支付价格是否正确
        assert user_order[0]['state'] == 2
        assert discount_price == user_order[0]['gua_dou_price'] + user_order[0]['pay_price']
        assert coupon_price == user_order[0]['discount']

    def test_coupon_discount_11(self, get_commodity, create_coupon_min):
        """
        优惠券：用户拥有一张优惠券使用后再下单无可用优惠券
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 获取享受优惠券优惠的商品
        sgu_no_ge = get_commodity['sgu_system']['ge']['no']
        # 使用优惠券下单并支付
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_system']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no)
        self.order_no, self.charge_id = detail[0], detail[1]
        time.sleep(4)
        # 调用优惠中心算价接口算价
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_ge)
        # 对订单进行全部退款
        self.order_common.order_refund_and_remove(order_no=self.order_no)
        time.sleep(3)
        # 断言优惠前价格是否等于优惠后价格
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        coupon_price = res['data']['couponPrice']
        assert coupon_price == 0
        assert origin_price == discount_price
        assert discount_total == 0

    def test_coupon_discount_12(self, get_commodity, create_coupon_min):
        """
        优惠券：退款后不返还用户优惠券
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 获取享受优惠券优惠的商品
        sgu_no_ge = get_commodity['sgu_system']['ge']['no']
        # 使用优惠券下单并支付
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_system']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no)
        self.order_no, self.charge_id = detail[0], detail[1]
        time.sleep(3)
        # 对订单进行全部退款
        self.order_common.order_refund_and_remove(order_no=self.order_no)
        time.sleep(3)
        # 退款后查询用户优惠券表
        user_grant = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 断言优惠券状态是否仍为已核销
        assert user_grant[0]['status'] == 2

    def test_coupon_discount_13(self, get_commodity, create_coupon_min):
        """
        优惠券：对使用优惠券的订单进行退款后，再次购买该商品无可使用优惠券
        """
        # 获取优惠券id
        coupon_id = create_coupon_min[0]['id']
        # 给用户发放优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=coupon_id, grantNum=1)
        # 获取享受优惠券优惠的商品
        sgu_no_ge = get_commodity['sgu_system']['ge']['no']
        # 使用优惠券下单并支付
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_system']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no)
        self.order_no, self.charge_id = detail[0], detail[1]
        time.sleep(3)
        # 对订单进行全部退款
        self.order_common.order_refund_and_remove(order_no=self.order_no)
        time.sleep(3)
        # 对使用优惠券订单进行退款后，调用优惠中心算价接口算价
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_ge)
        # 断言优惠前价格是否等于优惠后价格
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        coupon_price = res['data']['couponPrice']
        assert coupon_price == 0
        assert origin_price == discount_price
        assert discount_total == 0

    def test_coupon_discount_14(self, get_commodity, create_coupon_min, create_coupon_max):
        """
        优惠券：用户拥有两张作用域相同，金额不同优惠券，使用优惠券时优先选用大额优惠券
        """
        # 获取小额优惠券id
        min_coupon_id = create_coupon_min[0]['id']
        # 给用户发放小额优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=min_coupon_id, grantNum=1)
        # 获取大额优惠券id
        max_coupon_id = create_coupon_max[0]['id']
        # 给用户发放大额优惠券
        self.c_coupon.api_coupon_grant(userNo=self.uid, couponId=max_coupon_id, grantNum=1)
        # 查询小额优惠券的金额\优惠券编码
        min_coupon_strategy = self.eshop_query.query_coupon_strategy(coupon_id=min_coupon_id)
        min_coupon_reward = int(min_coupon_strategy[0]['reward'])
        # 查询大额优惠券的金额\优惠券编码
        max_coupon_strategy = self.eshop_query.query_coupon_strategy(coupon_id=max_coupon_id)
        max_coupon_reward = int(max_coupon_strategy[0]['reward'])
        # 获取享受优惠券优惠的商品
        sgu_no_ge = get_commodity['sgu_system']['ge']['no']
        # 调用优惠中心算价接口算价
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no_ge)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        coupon_price = res['data']['couponPrice']
        # 断言给用户是否使用的大额优惠券
        assert coupon_price == max_coupon_reward
        assert origin_price == discount_price + coupon_price
        assert discount_total == 0
        # 使用优惠券下单并支付
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_system']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no)
        self.order_no, self.charge_id = detail[0], detail[1]
        time.sleep(3)
        # 使用优惠券下单支付后查询用户优惠券表
        user_grant_max = self.eshop_query.query_user_coupon(user_no=self.uid)
        # 断言优惠券状态是否正确
        if user_grant_max[0]['coupon_id'] == max_coupon_id:
            assert user_grant_max[0]['status'] == 2
            assert user_grant_max[1]['status'] == 0
        else:
            assert user_grant_max[0]['status'] == 0
            assert user_grant_max[1]['status'] == 2
        # 查询用户orders订单表
        user_order = self.eshop_query.query_user_order(order_no=self.order_no)
        # 对订单进行全部退款
        self.order_common.order_refund_and_remove(order_no=self.order_no)
        time.sleep(3)
        # 断言用户使用优惠券后支付价格是否正确
        assert user_order[0]['state'] == 2
        assert discount_price == user_order[0]['gua_dou_price'] + user_order[0]['pay_price']
        assert coupon_price == user_order[0]['discount']
        """
        用例执行完成后根据coupon_id删除优惠券批次
        """
        self.eshop_query.delete_coupon(coupon_id=min_coupon_id)
        self.eshop_query.delete_coupon(coupon_id=max_coupon_id)
