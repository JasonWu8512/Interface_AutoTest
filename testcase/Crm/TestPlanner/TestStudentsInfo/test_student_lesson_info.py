# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/30 9:02 下午
@Author  : Grace
@File    : test_student_lesson_info.py
涉及到的接口：
/api/planner/get_baby_list
 /api/share/get_baby_course_detail--复杂
 /api/planner/get_learning_map_data
  /api/share/get_user_lesson_detail--复杂
"""

import pytest
import random
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.businessQuery import ghsQuery
from business.CrmQuery import CrmJainaQuery
import pytest_check

@pytest.mark.xCrm
class TestStudentInfo(object):
    dm = Domains()
    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.planner = ApiPlanner(cls.session.cookies)
        cls.query = CrmJainaQuery()
        cls.mongo = ghsQuery()

    @pytest.mark.smoke
    def test_get_baby_info(self,student_info):
        print(student_info)
        student = random.choice(self.planner.api_get_students(student_info()).get("data").get("result"))
        gua_id = student["gua_id"]
        baby_list = student["baby_list"]
        '''数据库查询baby的姓名，生日'''
        api_data = self.planner.api_get_baby_list(gua_id).get('data')
        for baby in api_data["baby_list"]["babies"]:
            pytest_check.is_in(baby['bid'],baby_list)
            break


    def teardown_class(cls):
        """当前类结束后默认执行方法"""
        cls.session.logout()
        print(cls.session.cookies)
