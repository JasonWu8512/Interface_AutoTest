# -*- coding: utf-8 -*-
# @Time: 2021/6/22 7:00 下午
# @Author: ian.zhou
# @File: test_system_course
# @Software: PyCharm


from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiRedeem import ApiRedeem
from business.Trade.eshopClient.ApiRedeem import ApiRedeem as c_ApiRedeem
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.Trade.promotion.ApiPromotion import ApiPromotion
from testcase.Trade.common import OrderCommon
from business.common.UserProperty import UserProperty
from business.mysqlQuery import EshopQuery
import pytest
import math
import time


@pytest.mark.Trade
@pytest.mark.promotion
@pytest.mark.TradeCommodity
@pytest.mark.TradeOrder
@pytest.mark.TradeRedeem
class TestSystemCourse:
    """优惠中心正价课优惠相关用例"""
    order_no = None
    charge_id = None

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
        cls.eshop_admin_redeem = ApiRedeem(token=a_token)
        cls.c_eshop_redeem = c_ApiRedeem(token=basic_auth)
        cls.c_eshop_orders = ApiNewOrders(token=basic_auth)
        cls.eshop_query = EshopQuery()
        cls.order_common = OrderCommon(c_user=c_user)
        cls.c_promotion = ApiPromotion()

    def setup(self):
        """用例开始前删除用户科目顺序记录、避免干扰"""
        self.eshop_query.delete_user_subject(user_no=self.uid)

    """
    course_type: 
    FORMAL_COURSE:正价课, TRIAL_COURSE:体验课, FORMAL_TEACHING_AIDS:正价课教具, SIX_WEEK_COURSE：双月课
    subject_type: 
    ENGLISH:英语, LOGIC:思维, CHINESE:语文
    """

    def test_subject_seq_record_1(self, get_commodity):
        """
        科目记录：购买不同科目正价课，应正确记录用户科目顺序
        :return:
        """
        # 获取对应科目正价课商品信息
        spu_no = get_commodity['spu']['no']
        sgu_no_ge, sgu_no_ma = get_commodity['sgu_system']['ge']['no'], get_commodity['sgu_system']['ma']['no']
        # 购买英语正价课商品
        order_no_ge = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no_ge)[0]
        time.sleep(5)
        # 购买思维正价课商品
        order_no_ma = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no_ma)[0]
        time.sleep(5)
        res = self.eshop_query.query_user_subject(user_no=self.uid)
        # 后置订单退款、删除
        self.order_common.order_refund_and_remove(order_no=order_no_ge)
        self.order_common.order_refund_and_remove(order_no=order_no_ma)
        # 验证用户科目顺序正确记录
        assert len(res) == 2
        assert res[0]['subject_type'] == 1
        assert res[0]['subject_course_type'] == 1
        assert res[1]['subject_type'] == 2
        assert res[1]['subject_course_type'] == 1

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    def test_subject_seq_record_2(self, get_commodity, subject_type):
        """
        科目记录：多次购买同科目正价课，对应科目记录不更新，相关订单未全部退款，科目记录不删除
        :param subject_type: 科目
        :return:
        """
        # 获取对应科目正价课商品信息
        sgu_id, subject_enum = get_commodity['sgu_system']['ge']['id'], 1
        if subject_type == 'LOGIC':
            sgu_id, subject_enum = get_commodity['sgu_system']['ma']['id'], 2
        # 生成兑换码
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id, num=2)['data']['detailList']
        # 兑换正价课
        order_no_1 = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[0])['data']['orderNo']
        time.sleep(5)
        res = self.eshop_query.query_user_subject(user_no=self.uid)
        create_time = res[0]['create_at']
        # 再次兑换该科目正价课
        order_no_2 = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[1])['data']['orderNo']
        time.sleep(5)
        # 验证用户科目记录未更新
        res = self.eshop_query.query_user_subject(user_no=self.uid)
        assert len(res) == 1
        assert res[0]['subject_type'] == subject_enum
        assert res[0]['subject_course_type'] == 1
        assert res[0]['create_at'] == create_time
        # 退掉一笔该正价课的订单
        self.order_common.order_refund_and_remove(order_no=order_no_1)
        res_1 = self.eshop_query.query_user_subject(user_no=self.uid)
        # 退掉另一笔正价课订单
        self.order_common.order_refund_and_remove(order_no=order_no_2)
        res_2 = self.eshop_query.query_user_subject(user_no=self.uid)
        # 验证未全部退款用户科目顺序记录不删除
        assert len(res_1) == 1
        assert res_1[0]['subject_type'] == subject_enum
        assert res_1[0]['subject_course_type'] == 1
        assert res_1[0]['create_at'] == create_time
        # 验证全部退款用户科目顺序记录正确删除
        assert len(res_2) == 0

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['FORMAL_COURSE'])
    def test_system_course_discount_1(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：未拥有任何课程，购买某一科目正价课无优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 获取对应科目正价课商品信息
        sgu_no = get_commodity['sgu_system']['ge']['no']
        if subject_type == 'LOGIC':
            sgu_no = get_commodity['sgu_system']['ma']['no']
        # 验证购买第一学科正价课无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert origin_price == discount_price
        assert discount_total == 0

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['FORMAL_COURSE', 'TRIAL_COURSE', 'SIX_WEEK_COURSE'])
    def test_system_course_discount_2(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：拥有某一科目正价课/体验课/双月课，继续购买该科目正价课无优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 手动添加用户已购科目记录
        subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0}]
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 获取对应科目正价课商品信息
        sgu_no = get_commodity['sgu_system']['ge']['no']
        if subject_type == 'LOGIC':
            sgu_no = get_commodity['sgu_system']['ma']['no']
        # 验证购买该科目正价课无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert origin_price == discount_price
        assert discount_total == 0

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['TRIAL_COURSE', 'SIX_WEEK_COURSE'])
    def test_system_course_discount_3(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：拥有某一科目体验课/双月课，继续购买另一科目正价课无优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 手动添加用户已购科目记录
        subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0}]
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 获取对应科目正价课商品信息
        sgu_no = get_commodity['sgu_system']['ma']['no']
        if subject_type == 'LOGIC':
            sgu_no = get_commodity['sgu_system']['ge']['no']
        # 验证购买该科目正价课无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert origin_price == discount_price
        assert discount_total == 0

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['FORMAL_COURSE'])
    def test_system_course_discount_4(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：拥有某一科目正价课，购买另一科目正价课应享受92折优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 手动添加用户已购科目记录
        subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0}]
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 获取对应科目正价课商品信息
        sgu_no = get_commodity['sgu_system']['ma']['no']
        if subject_type == 'LOGIC':
            sgu_no = get_commodity['sgu_system']['ge']['no']
        # 验证购买该科目正价课应享受92折优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        discount_detail_1_price = res['data']['activityPackagePromotionCalculateResultRespList'][0][
            'activityPromotionCalculateResultRespList'][0]['totalPromotionPrice']
        discount_detail_1_description = res['data']['activityPackagePromotionCalculateResultRespList'][0][
            'activityPromotionCalculateResultRespList'][0]['description']
        assert discount_total == math.ceil(origin_price/100*0.08)*100
        assert origin_price - discount_total == discount_price
        assert discount_detail_1_price == discount_total
        assert discount_detail_1_description == '购第2科优惠抵扣'

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['FORMAL_COURSE'])
    def test_system_course_discount_5(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：拥有两个科目正价课，购买第二科目正价课应享受92折优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 手动添加用户已购科目记录，获取对应科目正价课商品信息
        if subject_type == 'ENGLISH':
            subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0},
                           {'subjectType': 'LOGIC', 'subjectCourseType': course_type, 'price': 0}]
            sgu_no = get_commodity['sgu_system']['ma']['no']
        else:
            subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0},
                           {'subjectType': 'ENGLISH', 'subjectCourseType': course_type, 'price': 0}]
            sgu_no = get_commodity['sgu_system']['ge']['no']
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 验证购买该科目正价课应享受92折优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        discount_detail_1_price = res['data']['activityPackagePromotionCalculateResultRespList'][0][
            'activityPromotionCalculateResultRespList'][0]['totalPromotionPrice']
        discount_detail_1_description = res['data']['activityPackagePromotionCalculateResultRespList'][0][
            'activityPromotionCalculateResultRespList'][0]['description']
        assert discount_total == math.ceil(origin_price/100*0.08)*100
        assert origin_price - discount_total == discount_price
        assert discount_detail_1_price == discount_total
        assert discount_detail_1_description == '购第2科优惠抵扣'

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['FORMAL_COURSE'])
    def test_system_course_discount_6(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：拥有某个科目正价课，购买另一科目正价课黑名单商品无优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 手动添加用户已购科目记录
        subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0}]
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 获取对应科目正价课商品信息
        sgu_no = get_commodity['sgu_system']['ma']['no']
        if subject_type == 'LOGIC':
            sgu_no = get_commodity['sgu_system']['ge']['no']
        # 将SGU设置为黑名单
        self.eshop_query.set_system_course_blacklist(sgu_no=sgu_no)
        # 验证购买该科目正价课黑名单商品应无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        # 断言前还原黑名单设置，避免断言失败数据未还原
        self.eshop_query.delete_system_course_blacklist(sgu_no=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert origin_price == discount_price
        assert discount_total == 0

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['FORMAL_COURSE'])
    def test_system_course_discount_7(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：拥有某个科目正价课，购买另一科目教具商品无优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 手动添加用户已购科目记录
        subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0}]
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 获取对应科目教具商品信息
        sgu_no = get_commodity['sgu_phy']['ma']['no']
        if subject_type == 'LOGIC':
            sgu_no = get_commodity['sgu_phy']['ge']['no']
        # 验证购买该科目教具商品应无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert origin_price == discount_price
        assert discount_total == 0

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['FORMAL_COURSE'])
    def test_system_course_discount_8(self, get_commodity, subject_type, course_type):
        """
        拓科优惠：拥有两个科目正价课，购买第二科目教具商品应享受92折优惠
        :param subject_type: 科目
        :param course_type: 课程类型
        :return:
        """
        # 手动添加用户已购科目记录，获取对应科目正价课商品信息
        if subject_type == 'ENGLISH':
            subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0},
                           {'subjectType': 'LOGIC', 'subjectCourseType': course_type, 'price': 0}]
            sgu_no = get_commodity['sgu_phy']['ma']['no']
        else:
            subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0},
                           {'subjectType': 'ENGLISH', 'subjectCourseType': course_type, 'price': 0}]
            sgu_no = get_commodity['sgu_phy']['ge']['no']
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 验证购买该科目正价课应享受92折优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        discount_detail_1_price = res['data']['activityPackagePromotionCalculateResultRespList'][0][
            'activityPromotionCalculateResultRespList'][0]['totalPromotionPrice']
        discount_detail_1_description = res['data']['activityPackagePromotionCalculateResultRespList'][0][
            'activityPromotionCalculateResultRespList'][0]['description']
        assert discount_total == math.ceil(origin_price/100*0.08)*100
        assert origin_price - discount_total == discount_price
        assert discount_detail_1_price == discount_total
        assert discount_detail_1_description == '购第2科优惠抵扣'










