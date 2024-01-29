# -*- coding: utf-8 -*-
# @Time : 2021/5/21 3:56 下午
# @Author : Fay
# @File : test_teacher_adopt_order.py

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check as check
import random
from faker import Faker
from utils.date_helper import get_off_set_time


class TestTeacherAdoptOrder(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.teacher = ApiTeacher(cls.session.cookies)
        #定义认领信息
        cls.orderid = 'T'+str(Faker().random_number(17))
        cls.paytime = get_off_set_time(fmt="YYYY-MM-DD HH:MM:SS")


    @pytest.fixture(scope='class')
    def guaid(self, get_student_infos):
        """获取一个可认领的英语学科的呱号"""
        result = self.teacher.api_get_students(get_student_infos())['data']['result']
        return random.sample(result, 1)[0]['gua_id']


    def get_order(self, get_adoptions_orders):
        """获取认领订单信息"""
        res = self.teacher.api_get_cr_order_adoptions(get_adoptions_orders(order_id=self.orderid, adoption_status=None))
        return res


    @pytest.fixture(scope='class', autouse=True)
    def create_adopt_order(self, guaid):
        """创建一个认领订单,并返回该认领订单信息"""
        self.teacher.api_create_cr_order_adoption(self.orderid, guaid, self.paytime)


    def test_create_cr_order_adoption(self, get_adoptions_orders):
        """验证创建站外认领订单"""
        data = self.get_order(get_adoptions_orders)['data']
        check.equal(data['total_count'], 1)
        check.equal(data['result'][0]['adoption_status'], "TO_BE_AUDIT")


    def test_audit_cr_order_adoption(self, get_adoptions_orders, get_audit_dict, guaid):
        """验证审核认领订单"""
        order = self.get_order(get_adoptions_orders)['data']['result'][0]
        adoption_uuid = order['adoption_uuid']
        audit_dict = get_audit_dict(order_id=self.orderid,
                                    gua_id=guaid,
                                    order_pay_time=self.paytime)
        try:
            """审核通过"""
            self.teacher.api_audit_cr_order_adoption(adoption_uuid, audit_dict)
            approved_order = self.get_order(get_adoptions_orders)['data']['result'][0]
            check.equal(approved_order['adoption_status'], "APPROVED")
        finally:
            """审核不通过"""
            audit_dict.update(approval=False)
            self.teacher.api_audit_cr_order_adoption(adoption_uuid, audit_dict)
            declined_order = self.get_order(get_adoptions_orders)['data']['result'][0]
            check.equal(declined_order['adoption_status'], "DECLINED")

