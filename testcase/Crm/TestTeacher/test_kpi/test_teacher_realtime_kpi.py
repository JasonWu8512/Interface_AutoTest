# -*- coding: utf-8 -*-
# @Time : 2021/4/14 5:54 下午
# @Author : Fay
# @File : test_teacher_realtime_kpi.py

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check as check
from utils.date_helper import get_latest_monday, get_any_time_stamp


@pytest.mark.xCrm
@pytest.mark.reg
class TestTeacherRealtimeKpi(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.teacher = ApiTeacher(cls.session.cookies)


    @pytest.fixture(scope='class')
    def get_realtime_kpi_list(self):
        '''获取实时绩效表'''
        return self.teacher.api_get_realtime_kpi_list()['data']['result']


    def test_total_student_cnt(self, get_student_infos, get_realtime_kpi_list):
        '''验证汇总的分配人数'''
        count = self.teacher.api_get_students(get_student_infos(kpi_term=get_latest_monday()))['data']['total_count']
        check.equal(eval(get_realtime_kpi_list[0]['total_student_cnt']), count)


    def test_normal_app_order_amount(self, get_realtime_kpi_list, get_kpi_orders):
        '''验证汇总的当期用户站内绩效金额'''
        # 从站内绩效订单获取当期所有订单（不可能超过10000）
        orders = self.teacher.api_search_app_order(get_kpi_orders(term=get_latest_monday()), search_size=10000)
        normal_app_order_amount = 0
        for row in orders['data']['result']:
            # 累加当期绩效订单金额
            if not row['is_old_leads_order']:
                normal_app_order_amount += eval(row['price_kpi'])
        check.equal(eval(get_realtime_kpi_list[0]['normal_app_order_amount']), normal_app_order_amount)


    def test_normal_app_order_cnt(self, get_realtime_kpi_list, get_kpi_orders):
        '''验证汇总的当期用户站内订单数'''
        # 从站内绩效订单获取当期所有订单（不可能超过10000）
        orders = self.teacher.api_search_app_order(get_kpi_orders(term=get_latest_monday()), search_size=10000)
        normal_app_order_cnt = 0
        for row in orders['data']['result']:
            # 累加当期绩效订单数
            if not row['is_old_leads_order']:
                normal_app_order_cnt += 1
        check.equal(eval(get_realtime_kpi_list[0]['normal_app_order_cnt']), normal_app_order_cnt)


    def test_normal_adopt_order_amount(self, get_realtime_kpi_list, get_adoptions_orders):
        '''验证汇总的当期用户认领订单金额'''
        orders = self.teacher.api_get_cr_order_adoptions(get_adoptions_orders(), search_size=1000)
        normal_adopt_order_amount = 0
        for row in orders['data']['result']:
            # 累加当期认领订单金额
            if not row['is_old_leads_order'] and row['kpi_term'] == get_latest_monday():
                normal_adopt_order_amount += eval(row['amount_str'])
        check.equal(eval(get_realtime_kpi_list[0]['normal_adopt_order_amount']), normal_adopt_order_amount)


    def test_normal_adopt_order_cnt(self, get_realtime_kpi_list, get_adoptions_orders):
        '''验证汇总的当期用户认领订单数'''
        orders = self.teacher.api_get_cr_order_adoptions(get_adoptions_orders(), search_size=1000)
        normal_adopt_order_cnt = 0
        for row in orders['data']['result']:
            # 累加当期认领订单数
            if not row['is_old_leads_order'] and row['kpi_term'] == get_latest_monday():
                normal_adopt_order_cnt += 1
        check.equal(eval(get_realtime_kpi_list[0]['normal_adopt_order_cnt']), normal_adopt_order_cnt)


    def test_old_leads_app_order_amount(self, get_realtime_kpi_list, get_kpi_orders):
        '''验证汇总的老用户站内订单金额'''
        # 从站内绩效订单获取当期所有订单（不可能超过10000）
        orders = self.teacher.api_search_app_order(get_kpi_orders(term=get_latest_monday()), search_size=10000)
        old_leads_app_order_amount = 0
        for row in orders['data']['result']:
            # 累加老用户绩效订单金额
            if row['is_old_leads_order']:
                old_leads_app_order_amount += eval(row['price_kpi'])
        check.equal(eval(get_realtime_kpi_list[0]['old_leads_app_order_amount']), old_leads_app_order_amount)


    def test_old_leads_app_order_cnt(self, get_realtime_kpi_list, get_kpi_orders):
        '''验证汇总的老用户站内订单数'''
        # 从站内绩效订单获取当期所有订单（不可能超过10000）
        orders = self.teacher.api_search_app_order(get_kpi_orders(term=get_latest_monday()), search_size=1000)
        old_leads_app_order_cnt = 0
        for row in orders['data']['result']:
            # 累加当期绩效订单数
            if row['is_old_leads_order']:
                old_leads_app_order_cnt += 1
        check.equal(eval(get_realtime_kpi_list[0]['old_leads_app_order_cnt']), old_leads_app_order_cnt)


    def test_old_leads_adopt_order_amount(self, get_realtime_kpi_list, get_adoptions_orders):
        '''验证汇总的老用户认领订单金额'''
        orders = self.teacher.api_get_cr_order_adoptions(get_adoptions_orders(), search_size=1000)
        old_leads_adopt_order_amount = 0
        for row in orders['data']['result']:
            # 累加当期认领订单金额
            if row['is_old_leads_order'] and row['order_pay_time'] >= get_any_time_stamp(get_latest_monday())*1000:
                old_leads_adopt_order_amount += eval(row['amount_str'])
        check.equal(eval(get_realtime_kpi_list[0]['old_leads_adopt_order_amount']), old_leads_adopt_order_amount)


    def test_old_leads_adopt_order_cnt(self, get_realtime_kpi_list, get_adoptions_orders):
        '''验证汇总的老用户认领订单数'''
        orders = self.teacher.api_get_cr_order_adoptions(get_adoptions_orders(), search_size=1000)
        old_leads_adopt_order_cnt = 0
        for row in orders['data']['result']:
            # 累加当期认领订单金额
            if row['is_old_leads_order'] and row['order_pay_time'] >= get_any_time_stamp(get_latest_monday())*1000:
                old_leads_adopt_order_cnt += 1
        check.equal(eval(get_realtime_kpi_list[0]['old_leads_adopt_order_cnt']), old_leads_adopt_order_cnt)


    def test_normal_total_amount(self, get_realtime_kpi_list):
        '''验证当期用户绩效=当期用户站内绩效金额+当期用户认领订单金额'''
        for row in get_realtime_kpi_list:
            # 当期用户绩效
            normal_total_amount = eval(row['normal_total_amount'])
            # 当期用户站内绩效金额
            normal_app_order_amount = eval(row['normal_app_order_amount'])
            # 当期用户认领订单金额
            normal_adopt_order_amount = eval(row['normal_adopt_order_amount'])
            check.equal(normal_total_amount, normal_app_order_amount + normal_adopt_order_amount)


    def test_normal_total_order_cnt(self, get_realtime_kpi_list):
        '''验证当期用户订单数=当期用户站内订单数+当期用户认领订单数'''
        for row in get_realtime_kpi_list:
            # 当期用户订单数
            normal_total_order_cnt = eval(row['normal_total_order_cnt'])
            # 当期用户站内订单数
            normal_app_order_cnt = eval(row['normal_app_order_cnt'])
            # 当期用户认领订单数
            normal_adopt_order_cnt = eval(row['normal_adopt_order_cnt'])
            check.equal(normal_total_order_cnt, normal_app_order_cnt + normal_adopt_order_cnt)


    def test_old_leads_total_amount(self, get_realtime_kpi_list):
        '''验证老用户绩效=老用户站内订单金额+老用户认领订单金额'''
        for row in get_realtime_kpi_list:
            # 老用户绩效
            old_leads_total_amount = eval(row['old_leads_total_amount'])
            # 老用户站内订单金额
            old_leads_app_order_amount = eval(row['old_leads_app_order_amount'])
            # 老用户认领订单金额
            old_leads_adopt_order_amount = eval(row['old_leads_adopt_order_amount'])
            check.equal(old_leads_total_amount, old_leads_app_order_amount + old_leads_adopt_order_amount)


    def test_old_leads_order_cnt(self, get_realtime_kpi_list):
        '''验证老用户订单数=老用户站内订单数+老用户认领订单数'''
        for row in get_realtime_kpi_list:
            # 老用户订单数
            old_leads_order_cnt = eval(row['old_leads_order_cnt'])
            # 老用户站内订单数
            old_leads_app_order_cnt = eval(row['old_leads_app_order_cnt'])
            # 老用户认领订单数
            old_leads_adopt_order_cnt = eval(row['old_leads_adopt_order_cnt'])
            check.equal(old_leads_order_cnt, old_leads_app_order_cnt + old_leads_adopt_order_cnt)


    def test_total_amount(self, get_realtime_kpi_list):
        '''验证总绩效金额=当期用户绩效+老用户绩效'''
        for row in get_realtime_kpi_list:
            # 总绩效金额
            total_amount = eval(row['total_amount'])
            # 当期用户绩效
            normal_total_amount = eval(row['normal_total_amount'])
            # 老用户绩效
            old_leads_total_amount = eval(row['old_leads_total_amount'])
            check.equal(total_amount, normal_total_amount + old_leads_total_amount)


    def test_arpu(self, get_realtime_kpi_list):
        '''验证APRU=当期用户绩效/分配人数'''
        for row in get_realtime_kpi_list:
            # ARPU
            arpu = eval(row['arpu'])
            # 当期用户绩效
            normal_total_amount = eval(row['normal_total_amount'])
            # 分配人数
            total_student_cnt = eval(row['total_student_cnt'])
            if not total_student_cnt:
                check.equal(arpu, 0)
            else:
                check.equal(arpu, round(normal_total_amount / total_student_cnt, 2))


    def test_normal_transfer_rate(self, get_realtime_kpi_list):
        '''验证转化率=转化人数/分配人数'''
        for row in get_realtime_kpi_list:
            # 转化率
            normal_transfer_rate = eval(row['normal_transfer_rate'].replace('%', ''))
            # 转化人数
            normal_transfer_cnt = eval(row['normal_transfer_cnt'])
            # 分配人数
            total_student_cnt = eval(row['total_student_cnt'])
            if not total_student_cnt:
                check.equal(normal_transfer_rate, 0)
            else:
                check.equal(normal_transfer_rate, round(normal_transfer_cnt / total_student_cnt * 100, 2))


    def test_normal_transfer_amount_avg(self, get_realtime_kpi_list):
        '''验证客单价=当期用户绩效/转化人数'''
        for row in get_realtime_kpi_list:
            # 客单价
            normal_transfer_amount_avg = eval(row['normal_transfer_amount_avg'])
            # 当期用户绩效
            normal_total_amount = eval(row['normal_total_amount'])
            # 转化人数
            normal_transfer_cnt = eval(row['normal_transfer_cnt'])
            if not normal_transfer_cnt:
                check.equal(normal_transfer_amount_avg, 0)
            else:
                check.equal(normal_transfer_amount_avg, round(normal_total_amount / normal_transfer_cnt, 2))


