# -*- coding: utf-8 -*-
# @Time : 2021/4/15 5:25 下午
# @Author : Fay
# @File : test_teacher_home.py

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check as check
from utils.date_helper import get_latest_monday, get_any_type_time
import random
from datetime import datetime

@pytest.mark.xCrm
@pytest.mark.reg
class TestTeacherHome(object):
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
        '''获取英语科目实时绩效表'''
        return self.teacher.api_get_realtime_kpi_list()['data']['result']


    def test_perf_broadcast(self, get_kpi_orders):
        '''验证业绩播报'''
        #获取当前转化期英语科目的业绩播报最新一条记录
        data = self.teacher.api_get_home_main_data(kpi_term=get_latest_monday())['data']
        perf_broadcast = data['perf_broadcast'][0] if data['perf_broadcast'] else False
        #判断最新的订单时间和订单金额
        if perf_broadcast:
            order = self.teacher.api_search_app_order(get_kpi_orders(term=get_latest_monday()),
                                                      search_size=1)[0]
            check.equal(perf_broadcast['order_pay_time_raw'], order['order_pay_time'])
            check.equal(eval(perf_broadcast['order_amount']),
                               round(eval(order['price_kpi'])/len(order['kpi_owner']), 2))


    def test_sales_brief(self, get_realtime_kpi_list):
        '''验证销售简报与实时绩效表一致的字段'''
        sales_brief = self.teacher.api_get_home_main_data(kpi_term=get_latest_monday())['data']['sales_brief']
        kpi_total = get_realtime_kpi_list[0]
        check.equal(sales_brief['arpu'], kpi_total['arpu'])
        check.equal(sales_brief['new_leads_amount'], kpi_total['normal_total_amount'])
        check.equal(sales_brief['old_leads_amount'], kpi_total['old_leads_total_amount'])
        check.equal(sales_brief['total_kpi_amount'], kpi_total['total_amount'])


    def test_sales_brief_today_kpi_amount(self, get_kpi_orders, get_adoptions_orders):
        '''验证销售简报今日金额字段'''
        # 获取当前转化期英语科目的销售简报-今日金额
        data = self.teacher.api_get_home_main_data(kpi_term=get_latest_monday())['data']
        today_kpi_amount = eval(data['sales_brief']['today_kpi_amount'])
        today = get_any_type_time(datetime.now(), 'YYYY-MM-DD')
        today_start = get_any_type_time(datetime.now(), 'YYYY-MM-DD 00:00:00')
        #获取当日的站内绩效订单
        app_orders = self.teacher.api_search_app_order(get_kpi_orders(
            term=get_latest_monday(), order_date_range=[today, today]), search_size=1000)['data']['result']
        #获取当日的认领绩效订单
        adopt_orders = self.teacher.api_get_cr_order_adoptions(
            get_adoptions_orders(date_range=[today, today]), search_size=1000)['data']['result']
        app_amount, adopt_amount = 0, 0
        for row in app_orders:
            #累加当日绩效订单金额
            app_amount += eval(row['price_kpi'])
        for row in adopt_orders:
            #累加当日认领订单金额
            if row['order_pay_time_str'] > today_start:
                adopt_amount += eval(row['amount_str'])
        check.equal(today_kpi_amount, app_amount+adopt_amount)


    @pytest.mark.parametrize("pk_type, type_list", [('arpu', 'arpu_list')])
    def test_update_team_pk_goal(self, pk_type, type_list):
        '''验证新增小组PK'''
        dept = random.sample(self.teacher.api_get_pk_rival_options(get_latest_monday(), pk_type)['data'], 2)
        d1, d2, pk_uuid = dept[0]['dept_uuid'], dept[1]['dept_uuid'], ''
        try:
            self.teacher.api_update_team_pk_goal(pk_type, get_latest_monday(), [d1, d2])
            pk_list = self.teacher.api_get_cr_home_pk_list(get_latest_monday())['data']
            for row in pk_list['pk_list_data']['rest_pk_list'][type_list]:
                if row[0]['dept_uuid'] == d1 or row[0]['dept_uuid'] == d2:
                    pk_uuid = row[0]['pk_uuid']
                    continue
            check.not_equal(pk_uuid, '')
        finally:
            self.teacher.api_remove_dept_from_pk_round(d1, pk_uuid)
