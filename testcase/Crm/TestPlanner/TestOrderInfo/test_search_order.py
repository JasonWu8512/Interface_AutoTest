# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/18 4:25 下午
@Author  : Grace
@File    : test_search_order.py
接口：
api/share/search_order
api/teacher/search_order
api/planner/search_app_order_v2
"""

import pytest
from config.env.domains import Domains, ROOT_PATH
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiShare.ApiShare import ApiShare
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.CrmQuery import CrmAllianceQuery
from business.CrmQuery import CrmJainaQuery
from testcase.Crm.TestPlanner import conftest
import random


@pytest.mark.xCrm
class TestSearchOrder(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        print(cls.config)
        cls.user = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.share = ApiShare(cls.user.cookies)
        cls.planner = ApiPlanner(cls.user.cookies)
        cls.teacher = ApiTeacher(cls.user.cookies)
        cls.query_alliance = CrmAllianceQuery()
        cls.query_jaina = CrmJainaQuery()
        '''学员信息表查询可用学员'''
        cls.student_list = cls.query_jaina.query_jaina_info(table='students', time_removed=0)
        print(cls.student_list)
        cls.user_list = []
        for user in cls.student_list:
            cls.user_list.append(user.get('user_id'))
        print(cls.user_list)

        '''随机获取一个订单号eshop 订单'''
        cls.students = random.choice(cls.query_alliance.query_alliance_info(table='app_order', time_removed=0,
                                                                            platform='eshop',
                                                                            order_status=['paid', 'refunded'],
                                                                            uid=cls.user_list))

        print(cls.students)
        cls.amount = str(cls.students.get('amount') / 100).split(".")[0]
        cls.orderStatus = cls.students.get('order_status')
        cls.order_id = cls.students.get('order_id')
        cls.uid = cls.students.get('uid')
        print(cls.uid)
        uid_all = cls.query_alliance.query_alliance_info(table='app_order', time_removed=0, platform='eshop',
                                                         uid=cls.uid)
        cls.rows = len(uid_all)

    @pytest.mark.smoke
    def test_search_order_by_gua_id(self,student_info):
        """
        @Author  : Grace
        1：通过uid查询app订单api/share/search_order
        """
        # student_info = self.planner.get_basic_detail(id_or_phone=uid).get(
        #     'data')
        # gua_id = student_info['basic_info']['user']['guaid']
        # print(gua_id)
        '''获取学员的呱id'''
        student_info = self.planner.api_get_students(student_info(stu_info=self.uid)).get(
            'data')
        gua_id = student_info['result'][0]['gua_id']
        '''根据该用户的订单数判断返回验证信息'''
        if self.rows == 1:
            resp = self.share.api_search_order(user_info=gua_id)
            pytest_check.equal(resp['data']['result']['App'][0]['order_status_row'], self.orderStatus)
            pytest_check.equal(resp['data']['result']['App'][0]['user_id'], self.uid)
            pytest_check.equal(resp['data']['result']['App'][0]['platform'], 'eshop')
            pytest_check.equal((resp['data']['result']['App'][0]['price_raw']).split(".")[0], self.amount)
        else:
            resp = self.share.api_search_order(user_info=self.uid)
            pytest_check.equal(resp['data']['total_count'], self.rows)

    @pytest.mark.smoke
    def test_teacher_search_order_by_gua_id(self, student_info):
        """
        @Author  : Grace
        2：通过uid号查询app订单api/teacher/search_order
        """

        '''获取学员的呱id'''
        student_info = self.planner.api_get_students(student_info(stu_info=self.uid)).get(
            'data')
        gua_id = student_info['result'][0]['gua_id']
        '''根据该用户的订单数判断返回验证信息'''
        if self.rows == 1:
            resp = self.teacher.api_search_order(user_info=gua_id)
            pytest_check.equal(resp['data']['result']['App'][0]['order_status_row'], self.orderStatus)
            pytest_check.equal(resp['data']['result']['App'][0]['user_id'], self.uid)
            pytest_check.equal(resp['data']['result']['App'][0]['platform'], 'eshop')
            pytest_check.equal((resp['data']['result']['App'][0]['price_raw']).split(".")[0], self.amount)
        else:
            resp = self.teacher.api_search_order(user_info=self.uid)
            pytest_check.equal(resp['data']['total_count'], self.rows)

    @pytest.mark.smoke
    def test_search_order_by_mobile(self,student_info):
        """
        @Author  : Grace
        1：通过手机号查询app订单api/share/search_order
        """
        '''根据uid获取学员手机号'''
        student_info = self.planner.api_get_students(student_info(stu_info=self.uid)).get(
            'data')
        mobile = student_info['result'][0]['tel_number']

        if self.rows == 1:
            resp = self.share.api_search_order(user_info=mobile)
            pytest_check.equal(resp['data']['result']['App'][0]['order_status_row'], self.orderStatus)
            pytest_check.equal(resp['data']['result']['App'][0]['user_id'], self.uid)
            pytest_check.equal(resp['data']['result']['App'][0]['platform'], 'eshop')
            pytest_check.equal((resp['data']['result']['App'][0]['price_raw']).split(".")[0], self.amount)
        else:
            resp = self.share.api_search_order(user_info=mobile)
            pytest_check.equal(resp['data']['total_count'], self.rows)

    @pytest.mark.smoke
    def test_teacher_search_order_by_mobile(self, student_info):
        """
        @Author  : Grace
        2：通过手机号查询app订单api/teacher/search_order
        """
        '''根据uid获取学员手机号'''
        student_info = self.planner.api_get_students(student_info(stu_info=self.uid)).get(
            'data')
        mobile = student_info['result'][0]['tel_number']
        if self.rows == 1:
            resp = self.teacher.api_search_order(user_info=mobile)
            pytest_check.equal(resp['data']['result']['App'][0]['order_status_row'], self.orderStatus)
            pytest_check.equal(resp['data']['result']['App'][0]['user_id'], self.uid)
            pytest_check.equal(resp['data']['result']['App'][0]['platform'], 'eshop')
            pytest_check.equal((resp['data']['result']['App'][0]['price_raw']).split(".")[0], self.amount)
        else:
            resp = self.teacher.api_search_order(user_info=mobile)
            pytest_check.equal(resp['data']['total_count'], self.rows)

    @pytest.mark.smoke
    def test_search_order_by_orderId(self):
        """
        @Author  : Grace
        1：根据订单号查询app订单api/share/search_order
        """
        resp = self.share.api_search_order(order_id=self.order_id)
        pytest_check.equal(resp['data']['result']['App'][0]['order_status_raw'], self.orderStatus)
        pytest_check.equal(resp['data']['result']['App'][0]['user_id'], self.uid)
        pytest_check.equal(resp['data']['result']['App'][0]['platform'], 'eshop')
        pytest_check.equal((resp['data']['result']['App'][0]['price_final']).split(".")[0], self.amount)

    @pytest.mark.smoke
    def test_teacher_search_order_by_orderId(self):
        """
        @Author  : Grace
        2：通过订单号查询app订单api/teacher/search_order
        """
        resp = self.teacher.api_search_order(order_id=self.order_id)
        pytest_check.equal(resp['data']['result']['App'][0]['order_status_raw'], self.orderStatus)
        pytest_check.equal(resp['data']['result']['App'][0]['user_id'], self.uid)
        pytest_check.equal(resp['data']['result']['App'][0]['platform'], 'eshop')
        pytest_check.equal((resp['data']['result']['App'][0]['price_final']).split(".")[0], self.amount)

    @pytest.mark.smoke
    def test_search_app_order_by_orderId(self,order_search_info):
        """
        @Author  : Grace
        1：根据订单号查询app订单 api/planner/search_app_order_v2
        """
        '''随机获取一个订单号app订单'''
        result = random.choice(self.planner.api_search_app_order_v2(order_search_info()).get('data').get('result'))
        order_id = result['order_id']
        '''数据库获取订单数据'''
        order = self.query_alliance.query_alliance_info(table='app_order', order_id=order_id)
        print(order)
        orderStatus = order[0].get('order_status')
        uid = order[0].get('uid')
        amount = str(order[0].get('amount') / 100).split(".")[0]
        resp = self.planner.api_search_app_order_v2(order_search_info(order_id=order_id))
        pytest_check.equal(resp['data']['result'][0]['order_status_raw'], orderStatus)
        pytest_check.equal(resp['data']['result'][0]['user_id'], uid)
        # pytest_check.equal(resp['data']['result'][0]['platform'], 'eshop')
        pytest_check.equal((resp['data']['result'][0]['price_final']).split(".")[0], amount)

    # @classmethod
    def teardown_class(cls):
        """当前类结束后默认执行方法"""
        cls.user.logout()
        print(cls.user.cookies)
