# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/25 10:19 上午
@Author  : Demon
@File    : test_teacher_main_data.py
"""

from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
from utils.date_helper import get_latest_monday

class TestTeacherMainData(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.teacher = ApiTeacher(cls.session.cookies)

    def test_teacher_main_data(self, get_main_subject):
        '''班主任首页数据校验'''
        data = self.teacher.api_get_home_main_data(kpi_term=get_latest_monday()[2:], subject_type=get_main_subject[1])
        print(get_main_subject[1], data)