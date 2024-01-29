# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/30 9:02 下午
@Author  : Demon
@File    : test_student_base_info.py
涉及到的接口：
get_basic_detail
get_stu_user_devices
"""


import pytest
import random
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.businessQuery import ghsQuery
from business.CrmQuery import CrmJainaQuery
import pytest_check


# @pytest.mark.xCrm
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
        '''学员信息表随机获取一个呱号,取复购信息'''
        cls.students = random.choice(cls.query.query_jaina_info(table='students', time_removed=0))
        cls.guaId = cls.students.get('gua_id') #取呱号
        cls.is_app_rebuy = cls.students.get('is_app_rebuy') #取app复购信息
        cls.is_youzan_kc_rebuy = cls.students.get('is_youzan_kc_rebuy') #取有赞复购信息
        cls.is_youzan_aid_rebuy = cls.students.get('is_youzan_aid_rebuy')  # 取有赞教具复购信息
        print(cls.students)
        '''思维学员信息表，随机获取一个呱号,取复购信息'''
        cls.mathstudents = random.choice(cls.query.query_jaina_info(table='math_students', time_removed=0))
        cls.mathguaId = cls.mathstudents.get('gua_id')  # 取呱号
        print(cls.mathguaId)
        cls.is_math_app_rebuy = cls.mathstudents.get('is_app_rebuy')  # 取app复购信息
        cls.is_math_youzan_aid_rebuy = cls.mathstudents.get('is_youzan_aid_rebuy')  # 取有赞教具复购信息

    @pytest.mark.smoke
    def test_get_basic_info_english_rebuy_info(self):
        '''
        根据呱号学员重新，返回英语复购信息
        '''
        api_data = self.planner.get_basic_detail(self.guaId).get('data')
        if self.is_app_rebuy == 1:
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy'), True)
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_type'), "app复购")
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_content'), "课程")
        elif self.is_youzan_kc_rebuy == 1 and self.is_youzan_aid_rebuy == 1:
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy'), True)
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_type'), "有赞复购")
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_content'), "课程+教具")
        elif self.is_youzan_aid_rebuy == 0 and self.is_youzan_kc_rebuy == 1:
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy'), True)
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_type'), "有赞复购")
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_content'), "课程")
        elif self.is_youzan_aid_rebuy == 1 and self.is_youzan_kc_rebuy == 0:
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy'), True)
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_type'), "有赞复购")
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy_content'), "教具")
        else:
            pytest_check.equal(api_data.get('basic_info').get('user').get('rebuy'), False)

    @pytest.mark.smoke
    def test_get_basic_info_math_rebuy_info(self):
        '''根据呱号学员重新，返回思维复购信息'''
        api_data = self.planner.get_basic_detail(self.mathguaId).get('data')
        if self.is_math_app_rebuy == 1:
            pytest_check.equal(api_data.get('basic_info').get('user').get('math_rebuy'), True)
            pytest_check.equal(api_data.get('basic_info').get('user').get('math_rebuy_type'), "app复购")
            pytest_check.equal(api_data.get('basic_info').get('user').get('math_rebuy_content'), "课程")
        elif self.is_math_youzan_aid_rebuy == 1:
            pytest_check.equal(api_data.get('basic_info').get('user').get('math_rebuy'), True)
            pytest_check.equal(api_data.get('basic_info').get('user').get('math_rebuy_type'), "有赞复购")
            pytest_check.equal(api_data.get('basic_info').get('user').get('math_rebuy_content'), "教具")
        else:
            pytest_check.equal(api_data.get('basic_info').get('user').get('math_rebuy'), False)

    @pytest.mark.reg
    def test_stu_devices(self):
        # 校验学院设备信息
        for stu in self.mongo.get_stu_user_devices():
            print(stu['_id'])
            mongo_using = []
            mon_remove = [_['deviceType'] for _ in stu.get('removedDevices').values()]
            for _ in stu.get('devices').values():
                if _ not in mon_remove:
                    mongo_using.append(_['deviceType'])

            tem = self.planner.get_basic_detail(id_or_phone=stu['_id']).get('data').get('basic_info').get('user_devices')
            api_remove = [_['deviceType'] for _ in tem.get('removed')]
            api_using = [_['deviceType'] for _ in tem.get('using')]
            pytest_check.equal(mon_remove, api_remove) # 已移除设备

            pytest_check.equal(mongo_using, api_using)
            # break

    #@classmethod
    def teardown_class(cls):
        """当前类结束后默认执行方法"""
        cls.session.logout()
        print(cls.session.cookies)