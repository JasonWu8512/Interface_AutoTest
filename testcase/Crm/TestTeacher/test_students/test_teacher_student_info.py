# -*- coding: utf-8 -*-
# @Time : 2021/4/1 3:08 下午
# @Author : Fay
# @File : test_teacher_student_info.py

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
from business.CrmQuery import CrmThrallQuery
import pytest_check as check
from utils.date_helper import get_any_type_time, get_diff_days, get_off_set_time, get_latest_monday
import random

@pytest.mark.xCrm
@pytest.mark.reg
class TestTeacherStudentInfo(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.teacher = ApiTeacher(cls.session.cookies)
        cls.query = CrmThrallQuery()
        # leadsbind_url: http://10.100.128.2:8192
        # leadsbind_url: http://10.100.113.73:8192

    def get_kpi_owner(self, res):
        '''获取学员的所有类型的班主任(没有则为空)'''
        if res['kpi_owner_normal_cnt'] == 1:
            kpi_owner_normal = [res['kpi_owner_normal'][0]['kpi_cr_wechat_ref_id']]
        elif res['kpi_owner_normal_cnt'] == 2:
            kpi_owner_normal = [res['kpi_owner_normal'][0]['kpi_cr_wechat_ref_id'],
                                res['kpi_owner_normal'][1]['kpi_cr_wechat_ref_id']]
        else:
            kpi_owner_normal = []

        if res['kpi_owner_week1_cnt'] == 1:
            kpi_owner_week1 = [res['kpi_owner_week1'][0]['kpi_cr_wechat_ref_id']]
        elif res['kpi_owner_week1_cnt'] == 2:
            kpi_owner_week1 = [res['kpi_owner_week1'][0]['kpi_cr_wechat_ref_id'],
                                res['kpi_owner_week1'][1]['kpi_cr_wechat_ref_id']]
        else:
            kpi_owner_week1 = []
        kpi_owner_week2 = [res['kpi_owner_week2'][0]['kpi_cr_wechat_ref_id']] \
            if res['kpi_owner_week2_cnt'] == 1 and res['service_mode'] == "twice_transfer" else []
        kpi_owner_post_term = [res['kpi_owner_post_term'][0]['kpi_cr_wechat_ref_id']] \
            if res['kpi_owner_post_term_cnt'] == 1 else []
        return [kpi_owner_normal, kpi_owner_week1, kpi_owner_week2, kpi_owner_post_term]


    def test_kpi_amount(self, get_student_infos):
        '''验证学员转化金额'''
        api_request = self.teacher.api_get_students(get_student_infos(has_kpi_amount=True))['data']['result']
        api_data = random.sample(api_request, 1)[0]
        api_kpi_amount = api_data['normal_kpi_total_amount_cent'] + api_data['old_leads_kpi_total_amount_cent']
        mysql_data = self.query.query_table_info(gua_id=api_data['gua_id'])[0]
        mysql_kpi_amount = mysql_data['cr_app_order_amount_cent'] + mysql_data['adopt_order_amount_cent'] + \
                           mysql_data['old_leads_app_order_amount_cent'] + mysql_data['old_leads_adopt_order_amount_cent']
        check.equal(api_kpi_amount, mysql_kpi_amount)


    def test_service_term_days(self, get_student_infos):
        '''验证学员运营天数'''
        result = self.teacher.api_get_students(get_student_infos())['data']['result']
        for row in result:
            if row['kpi_term'] and row['repromotion_end_time']:
                kpi_term = get_any_type_time(row['kpi_term'], 'YYYY-MM-DD 00:00:00')
                repromotion_end_time = row['repromotion_end_time']
                check.equal(get_diff_days(kpi_term, repromotion_end_time) + 1, row['service_term_days'])


    def test_recommender_is_buy(self, get_student_infos):
        '''验证已购转介绍学员'''
        result = self.teacher.api_get_students(get_student_infos(custom_label="已购转介绍"))['data']['result']
        for row in result:
            check.is_not(row['recommender_gua_id'], '-')
            check.equal(row['is_recommender_paidxx'], 1)
            check.is_in('已购转介绍', row['custom_label'])


    def test_recommender_not_buy(self, get_student_infos):
        '''验证未购转介绍学员'''
        result = self.teacher.api_get_students(get_student_infos(custom_label="未购转介绍"))['data']['result']
        for row in result:
            check.is_not(row['recommender_gua_id'], '-')
            check.equal(row['is_combine_subject'], 1)
            check.is_in('未购转介绍', row['custom_label'])


    def test_is_combine_subject(self, get_student_infos):
        '''验证双科联报学员'''
        result = self.teacher.api_get_students(get_student_infos(custom_label="双科联报"))['data']['result']
        for row in result:
            check.equal(row['is_combine_subject'], 1)
            check.is_in('双科联报', row['custom_label'])


    def test_is_fc(self, get_student_infos):
        '''验证0元课学员'''
        result = self.teacher.api_get_students(get_student_infos(custom_label="0元课"))['data']['result']
        for row in result:
            check.equal(row['is_fc'], 1)
            check.is_in('0元课', row['custom_label'])

    def test_is_paid_english_xx(self, get_student_infos):
        '''验证英语正价课学员'''
        result = self.teacher.api_get_students(get_student_infos(custom_label="英语正价课"))['data']['result']
        for row in result:
            check.equal(row['is_paid_english_xx'], 1)
            check.equal(row['is_paid_math_xx'], 0)
            check.is_in('英语正价课', row['custom_label'])


    def test_is_paid_math_xx(self, get_student_infos):
        '''验证思维正价课学员'''
        result = self.teacher.api_get_students(get_student_infos(custom_label="思维正价课"))['data']['result']
        for row in result:
            check.equal(row['is_paid_math_xx'], 1)
            check.equal(row['is_paid_english_xx'], 0)
            check.is_in('思维正价课', row['custom_label'])


    def test_update_real_add_teacher(self, get_student_infos):
        '''验证上传好友操作'''
        result = self.teacher.api_get_students(get_student_infos(is_real_add_teacher=False))['data']['result']
        gua_id = random.sample(result, 1)[0]['gua_id']
        res = self.teacher.api_update_real_add_teacher([gua_id])
        #验证匹配成功且更新了学员信息表es
        student = self.teacher.api_get_students(get_student_infos(stu_info=gua_id))['data']['result'][0]
        check.is_in(gua_id, res['data']['matched'])
        check.equal(student['is_real_add_teacher'], 1)


    @pytest.mark.parametrize("match_method, identifiers", [('guaid', '123123'), ('tel_number', '15615615615')])
    def test_update_real_add_teacher_fail(self, match_method, identifiers):
        '''验证不存在的呱号/手机号进行上传好友失败操作'''
        res = self.teacher.api_update_real_add_teacher(match_method=match_method, identifiers=[identifiers])
        check.is_in(identifiers, res['data']['unmatched'])


    def test_update_student_kpi_term(self, get_student_infos, get_update_dicts):
        '''验证更新绩效期次'''
        result = self.teacher.api_get_students(get_student_infos())['data']['result']
        ran = random.sample(result, 1)[0]
        gua_id, term = ran['gua_id'], ran['kpi_term']
        change_term = get_off_set_time(ran['kpi_term'], random.choice([-7, 7]))
        #验证更新成功且更新了学员表es
        try:
            self.teacher.api_update_student_kpi_owner_v2([gua_id], get_update_dicts(kpi_term=change_term))
            student = self.teacher.api_get_students(get_student_infos(stu_info=gua_id))['data']['result'][0]
            check.equal(student['kpi_term'], change_term)
        finally:
            self.teacher.api_update_student_kpi_owner_v2([gua_id], get_update_dicts(kpi_term=term))


    def test_update_student_kpi_owner_normal(self, get_student_infos, get_update_dicts):
        '''验证更新普通班主任和期外班主任'''
        result = self.teacher.api_get_students(get_student_infos())['data']['result']
        ran = random.sample(result, 1)[0]
        gua_id = ran['gua_id']
        owners = self.get_kpi_owner(ran)
        print(gua_id)
        change_owner = [random.sample(self.teacher.api_get_cr_wechat_id_list_v2()['data']['normal'], 1)
                        [0]['wechat_list'][0]]
        try:
            self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                         get_update_dicts(kpi_cr_ref_id_normal=change_owner,
                                                                          kpi_cr_ref_id_post_term=change_owner))
            student = self.teacher.api_get_students(get_student_infos(stu_info=gua_id))['data']['result'][0]
            check.equal(student['kpi_owner_normal'][0]['kpi_cr_wechat_ref_id'], change_owner[0])
            check.equal(student['kpi_owner_post_term'][0]['kpi_cr_wechat_ref_id'], change_owner[0])
        finally:
            if ran['service_mode'] == "normal":
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_normal=owners[0],
                                                                              kpi_cr_ref_id_post_term=owners[3]))
            else:
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_week1=owners[1],
                                                                              kpi_cr_ref_id_post_term=owners[3]))
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_week2=owners[2]))


    def test_update_students_kpi_owner_week12(self, get_student_infos, get_update_dicts):
        '''验证更新一二转班主任和期外班主任'''
        result = self.teacher.api_get_students(get_student_infos())['data']['result']
        ran = random.sample(result, 1)[0]
        gua_id = ran['gua_id']
        owners = self.get_kpi_owner(ran)
        change_owner_week1 = [random.sample(self.teacher.api_get_cr_wechat_id_list_v2()['data']['week1'], 1)
                              [0]['wechat_list'][0]]
        change_owner_week2 = [random.sample(self.teacher.api_get_cr_wechat_id_list_v2()['data']['week2'], 1)
                              [0]['wechat_list'][0]]
        try:
            self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                         get_update_dicts(kpi_cr_ref_id_week1=change_owner_week1,
                                                                          kpi_cr_ref_id_post_term=change_owner_week1))
            student = self.teacher.api_get_students(get_student_infos(stu_info=gua_id))['data']['result'][0]
            check.equal(student['kpi_owner_week1'][0]['kpi_cr_wechat_ref_id'], change_owner_week1[0])
            check.equal(student['kpi_owner_post_term'][0]['kpi_cr_wechat_ref_id'], change_owner_week1[0])
            #学员如果是normal运营模式，不能直接修改二转班主任，必须先更新一转班主任，故这里分开更新和校验
            self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                         get_update_dicts(kpi_cr_ref_id_week2=change_owner_week2))
            student = self.teacher.api_get_students(get_student_infos(stu_info=gua_id))['data']['result'][0]
            check.equal(student['kpi_owner_week2'][0]['kpi_cr_wechat_ref_id'], change_owner_week2[0])
        finally:
            if ran['service_mode'] == "normal":
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_normal=owners[0],
                                                                              kpi_cr_ref_id_post_term=owners[3]))
            else:
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_week1=owners[1],
                                                                              kpi_cr_ref_id_week2=owners[2],
                                                                              kpi_cr_ref_id_post_term=owners[3]))


    def test_update_student_kpi_owner_week2_error(self, get_student_infos, get_update_dicts):
        '''验证没有一转班主任的学员更新二转班主任'''
        result = self.teacher.api_get_students(get_student_infos())['data']['result']
        ran = random.sample(result, 1)[0]
        gua_id = ran['gua_id']
        owners = self.get_kpi_owner(ran)
        change_owner_normal = [random.sample(self.teacher.api_get_cr_wechat_id_list_v2()['data']['normal'], 1)
                               [0]['wechat_list'][0]]
        change_owner_week2 = [random.sample(self.teacher.api_get_cr_wechat_id_list_v2()['data']['week2'], 1)
                              [0]['wechat_list'][0]]
        try:
            self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                         get_update_dicts(kpi_cr_ref_id_normal=change_owner_normal,
                                                                          kpi_cr_ref_id_post_term=change_owner_normal))
            res = self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                               get_update_dicts(kpi_cr_ref_id_week2=change_owner_week2))
            error_list = res['data']['error_list']
            check.equal(error_list[0]['error_guaids'][0], gua_id)
            check.equal(error_list[0]['error_msg'], "普通运营模式的学员不可直接更新二转班主任。请先设置一转班主任")
        finally:
            if ran['service_mode'] == "normal":
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_normal=owners[0],
                                                                              kpi_cr_ref_id_post_term=owners[3]))
            else:
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_week1=owners[1],
                                                                              kpi_cr_ref_id_post_term=owners[3]))
                self.teacher.api_update_student_kpi_owner_v2([gua_id],
                                                             get_update_dicts(kpi_cr_ref_id_week2=owners[2]))


    @pytest.mark.parametrize("gua_id", ['123123'])
    def test_update_student_kpi_fail(self, gua_id, get_update_dicts):
        '''验证输入不存在的呱号更新绩效归属失败（修改绩效期次为例）'''
        error = self.teacher.api_update_student_kpi_owner_v2(
            [gua_id], get_update_dicts(kpi_term=get_latest_monday()))['data']['error_list'][0]
        check.is_in(gua_id, error['error_guaids'])
        check.equal(error['error_msg'], '呱号不存在或未更新到学员表')


    def test_update_student_service_term_days(self, get_student_infos):
        '''验证更新运营天数'''
        result = self.teacher.api_get_students(get_student_infos())['data']['result']
        ran = random.sample(result, 1)[0]
        gua_id, days, change_days = ran['gua_id'], ran['service_term_days'], random.choice([7, 14, 21])
        try:
            self.teacher.api_update_student_service_term_days([gua_id], change_days)
            student = self.teacher.api_get_students(get_student_infos(stu_info=gua_id))['data']['result'][0]
            check.equal(student['service_term_days'], change_days)
        finally:
            self.teacher.api_update_student_service_term_days([gua_id], days)


    @pytest.mark.parametrize("gua_id, days", [('123123', 7)])
    def test_update_student_service_term_days_fail(self, gua_id, days):
        '''验证输入不存在的呱号更新运营天数失败'''
        error = self.teacher.api_update_student_service_term_days([gua_id], days)['data']['error_list'][0]
        check.is_in(gua_id, error['error_guaids'])
        check.equal(error['error_msg'], '呱号不存在或未更新到学员表')


    def test_update_assign_dummy(self):
        '''验证分配到假人的学员重新分配班主任'''

