# -*- coding: utf-8 -*-
# @Time : 2021/4/14 5:39 下午
# @Author : Fay
# @File : test_teacher_app_order.py

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check as check
import re
from utils.date_helper import get_any_time_stamp

@pytest.mark.xCrm
@pytest.mark.reg
class TestTeacherAppOrders(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.teacher = ApiTeacher(cls.session.cookies)


    def test_order_kpi_amount(self, get_kpi_orders):
        '''验证站内绩效订单的绩效金额'''
        result = self.teacher.api_search_app_order(get_kpi_orders())['data']['result']
        for row in result:
            if row['order_status_raw'] in ['refunded', 'refunding']:
                kpi_amount = sum(list(map(eval, [row['refund_amount'], row['refund_guadou']])),
                                 row['subject_discount_cent'])
            else:
                kpi_amount = sum(list(map(eval, [row['price_final'], row['guadou_amount'], '-' + row['refund_amount'],
                                                 '-' + row['refund_guadou']])), row['subject_discount_cent']/100)
            check.equal(row['price_kpi_cent'], kpi_amount * 100)


    def test_order_kpi_type(self, get_kpi_orders, get_old_order_itemid):
        '''验证站内绩效订单不同绩效类型的绩效规则'''
        result = self.teacher.api_search_app_order(get_kpi_orders())['data']['result']
        for row in result:
            #每个期次的绩效订单统计结束时间为跑率结束时间+5min
            end_time = row['repromotion_end_time'] + 300
            if row['is_old_leads_order']:
                # 老用户绩效订单item_id为指定商品，订单时间在绩效期次后
                check.greater(row['order_pay_time'], end_time)
                check.is_in(row['product_item_id'], get_old_order_itemid)
            else:
                #未更新过期次、期次延后、期次提前
                if row['kpi_term'] == row['cr_term']:
                    start_time = row['order_99_pay_time']
                elif row['kpi_term'] > row['cr_term']:
                    start_time = get_any_time_stamp(row['kpi_term'])
                else:
                    start_time = 0
                #当期绩效订单支付时间在绩效期次内，且item_id符合正则
                check.greater_equal(row['order_pay_time'], start_time)
                check.greater_equal(end_time, row['order_pay_time'])
                res = re.search(r"(L[0-9]+T[0-9]+)|(^YS.*K[0-9]+)|(BCJ)|(L[0-9]+XX)|(T[1-9])|(K[1-9])|(S[1-9])|(F[1-9])",
                                row['product_item_id'])
                check.is_true(res)


    #@pytest.mark.parametrize("subject_type", ['english', 'math'])
    def order_kpi_infos(self, get_kpi_orders, get_student_infos, subject_type):
        '''验证站内绩效订单的绩效期次和绩效归属（更新绩效字段会触发站内订单es更新）'''
        #暂时去掉这条case，因为站内绩效订单绩效归属逻辑和学员信息表不一致
        result = self.teacher.api_search_app_order(get_kpi_orders(subject_type=subject_type))['data']['result']
        for row in result:
            student = self.teacher.api_get_students(get_student_infos(stu_info=row['gua_id'],
                                                                      subject_type=subject_type))['data']['result'][0]
            check.equal(row['kpi_term'], student['kpi_term'])
            if result['is_old_leads_order']:
                check.equal(row[''])
            else:
                pass


    def test_refunded_order(self, get_kpi_orders):
        '''验证全额退款的站内绩效订单支付时间'''
        result = self.teacher.api_search_app_order(get_kpi_orders(order_status="已退款"))['data']['result']
        for row in result:
            diff_time = row['refund_time']-row['order_pay_time']
            check.greater(diff_time, 7*24*60*6)