# -*- coding: utf-8 -*-
# @Time : 2021/6/28 3:52 下午
# @Author : Fay
# @File : test_teacher_leads_bind.py
import time

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check as check
from business.CrmQuery import CrmThrallQuery, CrmJainaQuery, CrmLeadsAssignQuery
from faker import Faker
from utils.date_helper import get_week, get_off_set_time



@pytest.mark.xCrm
@pytest.mark.reg
class TestTeacherLeadsBind(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.teacher = ApiTeacher(cls.session.cookies)
        cls.thrall_query = CrmThrallQuery()
        cls.jaina_query = CrmJainaQuery()
        cls.leads_query = CrmLeadsAssignQuery()

    @pytest.fixture(scope='class', autouse=True)
    def get_uid(self):
        """获取一个user_id"""
        return Faker().md5()

    @pytest.fixture(scope='class', autouse=True)
    def get_ghs_uid(self):
        """获取一个购买过正价课(拥有规划师)的user_id"""
        sql = self.jaina_query.query_jaina_info('ghs_user', end_time=0)
        if sql:
            return sql[0]['user_id']
        else:
            return Faker().md5()

    def reset_leads_bind(self, uid):
        """将分配记录清除，以便uid重复利用"""
        self.thrall_query.delete_leadsbind(uid)
        self.leads_query.delete_leadsbind(uid)

    def assert_wechat_type(self, res, wechat_type):
        """验证分配的TID是否为对应的微信号类型"""
        tid = res['data']['cr_ref_id']
        if tid != 'T1665' and tid != 'T064':
            sql = self.leads_query.query_table_info('cr_wechat_info', cr_wechat_reference_id=tid)[0]
            cr_wechat_type = sql['cr_wechat_type']
        else:
            sql = {"cr_wechat_type": "兜底号"}
            print("请检查排班是否正常！")
        check.equal(cr_wechat_type, wechat_type)

    def assert_leads_channel(self, uid, channel_type, subject_type="english", assign_type="normal"):
        "验证分配的渠道是否为对应的渠道等级"
        sql = self.leads_query.query_table_info('crleadsbindv2', user_id=uid, subject_type=subject_type,
                                                assign_type=assign_type)
        if sql:
            biz_channel = sql[0]['biz_channel']
        else:
            biz_channel = '数据异常'
        check.equal(biz_channel, channel_type)

    def assert_wechat_id(self, res, wechat_id):
        """验证分配的班主任TID是否正确"""
        tid = res['data']['cr_ref_id']
        if tid == 'T1665' and tid == 'T064':
            tid = "兜底号"
            print("请检查排班是否正常！")
        check.equal(tid, wechat_id)

    def assert_assign_term(self, res, assign_term):
        """验证分配的期次是否正确"""
        term = res['data']['term']
        check.equal(term, assign_term)

    @pytest.mark.parametrize("marketingChannelCode, is_combined_subject, lesson_start_at_same_time",
                             [("tgr_noground", True, True), ("tgr_noground", True, False),
                              ("tgr_noground", False, False), ("refer", True, True),
                              ("refer", True, False), ("refer", False, False)])
    def test_english_leads_assign_wechat_I(self, get_uid, get_raw_push, marketingChannelCode, is_combined_subject,
                                           lesson_start_at_same_time):
        """英语分配至微信号I【转推流量】"""
        try:
            # 转推渠道定向分配
            pts = int(time.time()*1000) if int(time.time()*1000)>=1626969600000 else 1626969600000
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid,
                                                                lesson_start_at_same_time=lesson_start_at_same_time,
                                                                is_combined_subject=is_combined_subject,
                                                                marketingChannelCode=marketingChannelCode,
                                                                pts=pts))
            print(res)
            self.assert_wechat_type(res, 'I')
        finally:
            self.reset_leads_bind(get_uid)


    @pytest.mark.parametrize("marketingChannelCode", ["nostandard_ground"])
    def test_english_leads_assign_wechat_H(self, get_uid, get_raw_push, marketingChannelCode):
        """英语分配至微信号H【地推流量】"""
        try:
            # 地推渠道定向分配
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid,
                                                                marketingChannelCode=marketingChannelCode))
            print(res)
            self.assert_wechat_type(res, 'H')
            check.is_in('D', res['data']['term'])
        finally:
            self.reset_leads_bind(get_uid)


    def test_english_leads_assign_wechat_G(self, get_uid):
        """英语分配至微信号G【0元课/接口不同】"""
        pass


    @pytest.mark.parametrize("marketingChannelCode, opensource", [("nostandard_cpa_", ""),
                                                                  ("nostandard_ecommerce_jdplus", ""),
                                                                  ("", "CPA"), ("", "JdPlus"), ("", "")])
    def test_english_leads_assign_wechat_E(self, get_uid, get_raw_push, marketingChannelCode, opensource):
        """英语分配至微信号E【AB实验同时开课】"""
        try:
            #联报同时开课
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, lesson_start_at_same_time=True,
                                                                is_combined_subject=True,
                                                                marketingChannelCode=marketingChannelCode,
                                                                opensource=opensource))
            print(res)
            self.assert_wechat_type(res, 'E')
        finally:
            self.reset_leads_bind(get_uid)


    @pytest.mark.parametrize("opensource, marketingChannelCode, lesson_start_at_same_time",
                             [("JdPlus", "", False), ("CPA-", "", False),
                              ("", "nostandard_cpa_", False), ("", "nostandard_ecommerce_jdplus", False),
                              ("", "nostandard_shortvideo_", True), ("", "nostandard_livestream_", True),
                              ("", "nostandard_live_", True), ("", "live-kuaishou-", True), ("", "live-douyin-", True),
                              ("", "nostandard_shortvideo_", False), ("", "nostandard_livestream_", False),
                              ("", "nostandard_live_", False), ("", "live-kuaishou-", False),
                              ("", "live-douyin-", False), ("", "tgr_ground_", True), ("", "tgr_ground_", False)])
    def test_english_leads_assign_wechat_D(self, get_uid, get_raw_push, opensource,
                                           marketingChannelCode, lesson_start_at_same_time):
        """英语分配至微信号D【低质渠道定向】"""
        try:
            #opensource和marketingChannelCode定向低质渠道
            is_combined_subject = True if lesson_start_at_same_time else False
            pts = int(time.time()*1000) if int(time.time()*1000)>=1626969600000 else 1626969600000
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, opensource=opensource,
                                                                marketingChannelCode=marketingChannelCode,
                                                                is_combined_subject=is_combined_subject,
                                                                lesson_start_at_same_time=lesson_start_at_same_time,
                                                                pts=pts))
            print(res)
            self.assert_wechat_type(res, 'D')
        finally:
            self.reset_leads_bind(get_uid)


    def test_english_leads_assign_wechat_A(self, get_uid, get_raw_push):
        """英语分配至微信号A【K1】"""
        try:
            #非联报同时开课且非定向低质渠道
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid))
            print(res)
            self.assert_wechat_type(res, 'A')
        finally:
            self.reset_leads_bind(get_uid)


    @pytest.mark.parametrize("is_combined_subject, marketingChannelCode, lesson_start_at_same_time",
                             [(True, "nostandard_ecommerce_jdplus", True),
                              (False, "nostandard_ecommerce_jdplus", False)])
    def test_math_leads_assign_wechat_F(self, get_uid, get_raw_push, is_combined_subject, marketingChannelCode,
                                        lesson_start_at_same_time):
        """思维分配至微信号F【京东定向】"""
        try:
            #marketingChannelCode为京东特殊流量，K1MATC
            res = self.teacher.api_leads_assign_v3(get_raw_push(subject_type="math", uid=get_uid,
                                                                marketingChannelCode=marketingChannelCode,
                                                                is_combined_subject=is_combined_subject,
                                                                lesson_start_at_same_time=lesson_start_at_same_time))
            print(res)
            self.assert_wechat_type(res, 'F')
        finally:
            self.reset_leads_bind(get_uid)


    def test_math_leads_assign_wechat_E(self, get_uid, get_raw_push):
        """思维分配至微信号E【AB实验同时开课】"""
        try:
            #联报同时开课，K1MATC
            res = self.teacher.api_leads_assign_v3(get_raw_push(subject_type="math", uid=get_uid,
                                                                lesson_start_at_same_time=True,
                                                                is_combined_subject=True))
            print(res)
            self.assert_wechat_type(res, 'E')
        finally:
            self.reset_leads_bind(get_uid)



    def test_math_leads_assign_wechat_D(self, get_uid, get_raw_push):
        """思维分配至微信号D【联报】"""
        try:
            #思维K1联报定向分配
            res = self.teacher.api_leads_assign_v3(get_raw_push(subject_type="math", uid=get_uid,
                                                                is_combined_subject=True))
            print(res)
            self.assert_wechat_type(res, 'D')
        finally:
            self.reset_leads_bind(get_uid)



    @pytest.mark.parametrize("marketingChannelCode, lesson_start_at_same_time, is_combined_subject",
                             [("nostandard_cpa_", False, True), ("", True, True),
                              ("", False, True), ("", False, False)])
    def test_math_leads_assign_wechat_C(self, get_uid, get_raw_push, marketingChannelCode,
                                        lesson_start_at_same_time, is_combined_subject):
        """思维分配至微信号C【K5】"""
        try:
            #K5MATC
            res = self.teacher.api_leads_assign_v3(get_raw_push(subject_type="math", uid=get_uid,
                                                                lessonIdList=["K5MATC", "K1GETC"],
                                                                marketingChannelCode=marketingChannelCode,
                                                                lesson_start_at_same_time=lesson_start_at_same_time,
                                                                is_combined_subject=is_combined_subject))
            print(res)
            self.assert_wechat_type(res, 'C')
        finally:
            self.reset_leads_bind(get_uid)


    @pytest.mark.parametrize("marketingChannelCode, lesson_start_at_same_time, is_combined_subject",
                             [("nostandard_cpa_", False, True), ("", True, True),
                              ("", False, True), ("", False, False)])
    def test_math_leads_assign_wechat_B(self, get_uid, get_raw_push, marketingChannelCode,
                                        lesson_start_at_same_time, is_combined_subject):
        """思维分配至微信号B【K3】"""
        try:
            #K3MATC
            res = self.teacher.api_leads_assign_v3(get_raw_push(subject_type="math", uid=get_uid,
                                                                lessonIdList=["K3MATC", "K1GETC"],
                                                                marketingChannelCode=marketingChannelCode,
                                                                lesson_start_at_same_time=lesson_start_at_same_time,
                                                                is_combined_subject=is_combined_subject))
            print(res)
            self.assert_wechat_type(res, 'B')
        finally:
            self.reset_leads_bind(get_uid)


    def test_math_leads_assign_wechat_A(self, get_uid, get_raw_push):
        """思维分配至微信号A【K1】"""
        try:
            #非京东非联报，K1MATC
            res = self.teacher.api_leads_assign_v3(get_raw_push(subject_type="math", uid=get_uid,
                                                                lessonIdList=["K1MATC"]))
            print(res)
            self.assert_wechat_type(res, 'A')
        finally:
            self.reset_leads_bind(get_uid)


    @pytest.mark.parametrize("itemid, opensource, initiator_uid, is_initiator_paidxx",
                             [("L1TC", "", "", False), ("H5_XX_Sample", "kol-", "", False),
                              ("H5_XX_Sample", "", "123456", True), ("H5_Cashback", "", "123456", True),
                              ("H5_Sample_Pintuan", "", "123456", True),
                              ("H5_Sample_DiamondActivity", "", "123456", True)])
    def test_english_leads_assign_chanel_A(self, get_uid, get_raw_push, itemid, opensource, initiator_uid,
                                           is_initiator_paidxx):
        """英语渠道划分为A"""
        try:
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, opensource=opensource,
                                                                itemid=itemid,
                                                                initiator_uid=initiator_uid,
                                                                is_initiator_paidxx=is_initiator_paidxx))
            print(res)
            self.assert_leads_channel(get_uid, 'A')
        finally:
            self.reset_leads_bind(get_uid)


    @pytest.mark.parametrize("itemid, opensource, initiator_uid, is_initiator_paidxx",
                             [("H5_XX_Sample_XCX", "", "", False), ("H5_Sample_tmall", "", "", False),
                              ("H5_Sample_Pdd", "", "", False), ("H5_Sample_Jd", "", "", False),
                              ("H5_Sample_Kbei", "", "", False), ("H5_XX_Sample", "", "", False),
                              ("TEST_OTHER", "", "", False)])
    def test_english_leads_assign_chanel_B(self, get_uid, get_raw_push, itemid, opensource, initiator_uid,
                                           is_initiator_paidxx):
        """英语渠道划分为B"""
        try:
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, opensource=opensource,
                                                                itemid=itemid,
                                                                initiator_uid=initiator_uid,
                                                                is_initiator_paidxx=is_initiator_paidxx))
            print(res)
            self.assert_leads_channel(get_uid, 'B')
        finally:
            self.reset_leads_bind(get_uid)


    @pytest.mark.parametrize("itemid, opensource, initiator_uid, is_initiator_paidxx",
                             [("H5_XX_Sample", "JLGL-study", "", ""), ("H5_Sample_OutsideH5", "", "", False),
                              ("H5_XX_Sample", "", "123456", False)])
    def test_english_leads_assign_chanel_C(self, get_uid, get_raw_push, itemid, opensource, initiator_uid,
                                           is_initiator_paidxx):
        """英语渠道划分为C"""
        try:
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, opensource=opensource,
                                                                itemid=itemid,
                                                                initiator_uid=initiator_uid,
                                                                is_initiator_paidxx=is_initiator_paidxx))
            print(res)
            self.assert_leads_channel(get_uid, 'C')
        finally:
            self.reset_leads_bind(get_uid)


    def test_math_leads_assign_chanel_S(self, get_ghs_uid, get_raw_push):
        """思维渠道划分为S"""
        try:
            # 防止获取到的规划师学员有思维的9.9分配记录
            self.reset_leads_bind(get_ghs_uid)
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_ghs_uid, subject_type="math"))
            print(res)
            self.assert_leads_channel(get_ghs_uid, 'S', "math")
        finally:
            self.reset_leads_bind(get_ghs_uid)


    def test_math_leads_assign_chanel_A(self, get_ghs_uid, get_raw_push):
        """思维渠道划分为A"""
        try:
            # 防止获取到的规划师学员有思维的9.9分配记录
            self.reset_leads_bind(get_ghs_uid)
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_ghs_uid, subject_type="math",
                                                                itemid="H5_Sample_Pintuan"))
            print(res)
            self.assert_leads_channel(get_ghs_uid, 'A', "math")
        finally:
            self.reset_leads_bind(get_ghs_uid)


    def test_math_leads_assign_chanel_B_buy_99(self, get_uid, get_raw_push):
        """思维渠道划分为B【买过英语9.9，没有买过英语正价课】"""
        try:
            self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid))
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, subject_type="math"))
            print(res)
            self.assert_leads_channel(get_uid, 'B', "math")
        finally:
            self.reset_leads_bind(get_uid)


    def test_math_leads_assign_chanel_B_not_buy(self, get_uid, get_raw_push):
        """思维渠道划分为B【没有买过英语9.9和正价课】"""
        try:
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, subject_type="math"))
            print(res)
            self.assert_leads_channel(get_uid, 'B', "math")
        finally:
            self.reset_leads_bind(get_uid)


    def test_math_leads_assign_chanel_C(self, get_uid, get_raw_push):
        """思维渠道划分为C"""
        try:
            self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid))
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, subject_type="math",
                                                                itemid="H5_Sample_Pintuan"))
            print(res)
            self.assert_leads_channel(get_uid, 'C', "math")
        finally:
            self.reset_leads_bind(get_uid)


    def test_english_assign_type(self, get_uid, get_raw_push):
        """测试英语流量分层"""
        try:
            res_dummy = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, assignType="dummy"))
            self.assert_wechat_id(res_dummy, 'T1914')
            self.assert_leads_channel(get_uid, 'C', assign_type='dummy')
            summary_dummy = self.leads_query.query_table_info("crleadstermsummary",
                                                        term=res_dummy['data']['term'],
                                                        cr_ref_id="T1914")[0]
            print(res_dummy)
            res_active = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, assignType="active"))
            check.not_equal(res_active, 'T1914')
            self.assert_leads_channel(get_uid, 'B', assign_type='active')
            summary_active = self.leads_query.query_table_info("crleadstermsummary",
                                                        term=res_active['data']['term'],
                                                        cr_ref_id="T1914")[0]
            print(res_active)
            check.equal(summary_dummy['leads_total_count']-1, summary_active['leads_total_count'])
            check.equal(summary_dummy['leads_biz_C_count']-1, summary_active['leads_biz_C_count'])
        finally:
            self.reset_leads_bind(get_uid)


    def test_math_assign_type(self, get_uid, get_raw_push):
        """测试思维流量分层"""
        try:
            res_dummy = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, assignType="dummy", subject_type="math"))
            self.assert_wechat_id(res_dummy, 'T1915')
            self.assert_leads_channel(get_uid, 'C', 'math', 'dummy')
            summary_dummy = self.leads_query.query_table_info("crleadstermsummary",
                                                        term=res_dummy['data']['term'],
                                                        cr_ref_id="T1915")[0]
            print(res_dummy)
            res_active = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, assignType="active", subject_type="math"))
            check.not_equal(res_active, 'T1915')
            self.assert_leads_channel(get_uid, 'B', 'math', 'active')
            summary_active = self.leads_query.query_table_info("crleadstermsummary",
                                                         term=res_active['data']['term'],
                                                         cr_ref_id="T1915")[0]
            print(res_active)
            check.equal(summary_dummy['leads_total_count'] - 1, summary_active['leads_total_count'])
            check.equal(summary_dummy['leads_biz_C_count'] - 1, summary_active['leads_biz_C_count'])
        finally:
            self.reset_leads_bind(get_uid)


    def test_leads_week_term(self, get_uid, get_raw_push):
        """测试正常分配周期次【周一～周四下周，周五～周日下下周】"""
        try:
            week = get_week(get_off_set_time())[2]
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid))
            if week <= 4:
                term = get_off_set_time(days=7-week+1)
            else:
                term = get_off_set_time(days=7+(7-week+1))
            self.assert_assign_term(res, term)
        finally:
            self.reset_leads_bind(get_uid)


    def test_leads_day_term(self, get_uid, get_raw_push):
        """测试正常分配日期次【T+2】"""
        try:
            term = f'D{get_off_set_time(days=2)}'
            res = self.teacher.api_leads_assign_v3(get_raw_push(uid=get_uid, marketingChannelCode='nostandard_ground'))
            self.assert_assign_term(res, term)
        finally:
            self.reset_leads_bind(get_uid)