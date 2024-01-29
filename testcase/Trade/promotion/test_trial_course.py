# -*- coding: utf-8 -*-
# @Time: 2021/6/22 7:00 下午
# @Author: ian.zhou
# @File: test_trial_course
# @Software: PyCharm
import time
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiRedeem import ApiRedeem
from business.Trade.eshopClient.ApiRedeem import ApiRedeem as c_ApiRedeem
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.Trade.promotion.ApiPromotion import ApiPromotion
from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from business.businessQuery import pingxxorderQuery
from testcase.Trade.common import OrderCommon
from business.common.UserProperty import UserProperty
from business.mysqlQuery import EshopQuery
import pytest


@pytest.mark.Trade
@pytest.mark.promotion
@pytest.mark.TradeCommodity
@pytest.mark.TradeOrder
@pytest.mark.TradeRedeem
class TestTrialCourse:
    """优惠中心体验课优惠相关用例"""

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
        cls.eshop_admin_commodity = ApiCommodity(token=a_token)
        cls.c_eshop_redeem = c_ApiRedeem(token=basic_auth)
        cls.c_eshop_orders = ApiNewOrders(token=basic_auth)
        cls.pingxxorder_query = pingxxorderQuery()
        cls.eshop_query = EshopQuery()
        cls.order_common = OrderCommon(c_user=c_user)
        cls.c_promotion = ApiPromotion()

    def setup(self):
        """用例开始前删除用户学科记录、避免干扰"""
        self.eshop_query.delete_user_subject(user_no=self.uid)

    def order_remove_by_uid(self):
        """
        删除用户下的所有订单，包括eshop_order 和pingXX_order
        """
        self.pingxxorder_query.delete_many_pingxxorder(uid=self.uid)
        self.eshop_query.delete_order_by_user_no(user_no=self.uid)

    """
    subject_type: 
    ENGLISH:英语, LOGIC:思维, CHINESE:语文
    course_type: 
    FORMAL_COURSE:正价课, TRIAL_COURSE:体验课, FORMAL_TEACHING_AIDS:正价课教具, SIX_WEEK_COURSE：双月课
    """

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['TRIAL_COURSE'])
    def test_trial_course_discount_1(self, get_commodity, subject_type, course_type):
        """
        用户依次购买A、B学科体验课，依次记录A、B学科为用户体验课第一、第二学科
        用户A学科体验课全部退款，删除A学科体验课记录
        """
        """体验课必须是新用户才能购买，执行之前删除该用户下的所有课程"""
        self.order_remove_by_uid()
        # 记录用户购买体验课顺序
        if subject_type == 'ENGLISH':
            flag_A = 'ge'
            flag_B = 'ma'
        else:
            flag_A = 'ma'
            flag_B = 'ge'
        sgu_no_A = get_commodity['sgu_trial'][flag_A]['no']
        sgu_no_B = get_commodity['sgu_trial'][flag_B]['no']
        # 用户依次使用兑换码兑换不同的体验课
        sgu_id_A = self.eshop_admin_commodity.api_get_sxu_list(commodityNo=sgu_no_A, sxuType=2)['data']['content'][0]['id']
        sgu_id_B = self.eshop_admin_commodity.api_get_sxu_list(commodityNo=sgu_no_B, sxuType=2)['data']['content'][0]['id']
        # 生成A、B课程兑换码
        redeem_code_A = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id_A, num=1)['data']['detailList']
        redeem_code_B = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id_B, num=1)['data']['detailList']
        # 依此兑换A、B学科体验课
        res_A = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code_A[0], needAddress=True)
        time.sleep(5)
        res_B = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code_B[0], needAddress=True)
        # 间隔几秒再查询，以防查不到数据
        time.sleep(3)
        # 查询用户学科信息
        res_1 = self.eshop_query.query_user_subject(self.uid)
        # 将A学科进行退款
        self.order_common.order_refund_and_remove(order_no=res_A['data']['orderNo'])
        time.sleep(3)
        # 退款后查询用户学科
        res_2 = self.eshop_query.query_user_subject(self.uid)
        self.order_common.order_refund_and_remove(order_no=res_B['data']['orderNo'])
        assert res_1[0]['subject_course_type'] == 2
        assert res_1[1]['subject_course_type'] == 2
        assert len(res_2) == 1
        if subject_type == 'ENGLISH':
            assert res_1[0]['subject_type'] == 1
            assert res_1[1]['subject_type'] == 2
            assert res_2[0]['subject_type'] == 2
        else:
            assert res_1[0]['subject_type'] == 2
            assert res_1[1]['subject_type'] == 1
            assert res_2[0]['subject_type'] == 1

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['TRIAL_COURSE'])
    def test_trial_course_discount_2(self, get_commodity, subject_type, course_type):
        """
        用户未拥有任何课程，购买A科目体验课无优惠
        """
        # 获取体验课信息
        if subject_type == 'ENGLISH':
            sgu_no = get_commodity['sgu_trial']['ge']['no']
        else:
            sgu_no = get_commodity['sgu_trial']['ma']['no']

        # 购买体验课无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert origin_price == discount_price
        assert discount_total == 0

    @pytest.mark.parametrize("course_type", ['TRIAL_COURSE'])
    def test_trial_course_discount_3(self, get_commodity, course_type):
        """
        用户未拥有任何课程，购买A+B科目联报体验课无优惠¥15.9
        """
        # 获取体验课信息
        sgu_no = get_commodity['sgu_trial']['ge_ma']['no']
        # 购买体验课无优惠
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert origin_price == discount_price
        assert discount_total == 0

    @pytest.mark.parametrize("subject_type", ['ENGLISH', 'LOGIC'])
    @pytest.mark.parametrize("course_type", ['TRIAL_COURSE', 'FORMAL_COURSE', 'SIX_WEEK_COURSE'])
    def test_trial_course_discount_4(self, get_commodity, subject_type, course_type):
        """
        用户只拥有A学科体验课/正价课/双月课，购买B学科体验课¥6
        """
        # 手动添加用户拥有课程记录
        subject_seq = [{'subjectType': subject_type, 'subjectCourseType': course_type, 'price': 0}]
        self.c_promotion.api_user_subject_seq_operation(userNo=self.uid, subjectSeqList=subject_seq)
        # 获取体验课信息
        if subject_type == 'ENGLISH':
            sgu_no = get_commodity['sgu_trial']['ma']['no']
        else:
            sgu_no = get_commodity['sgu_trial']['ge']['no']
        # 购买另一学科的体验课
        res = self.c_promotion.api_promotion_calculate(userNo=self.uid, commodityNo=sgu_no)
        origin_price = res['data']['prePromotionPrice']
        discount_price = res['data']['postPromotionPrice']
        discount_total = res['data']['activityPrice']
        assert discount_price == 600.0
        assert discount_total == 390.0
