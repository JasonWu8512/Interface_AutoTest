'''
学员信息表模块
tion
'''
import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.businessQuery import ghsQuery
from business.CrmQuery import CrmJainaQuery

import pytest_check
import random


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
        cls.query = CrmJainaQuery()  # mysql
        cls.mongo = ghsQuery()  # mg

    def test_students_data(self):
        """学员信息表全部学员列表"""
        mg_students = random.choice(self.query.query_jaina_info(table='students'))
        student_infos = {
            'ghs_info': {
                'group': mg_students['ghs_group'],
                'email': mg_students['ghs_email'],
            },
            "stu_info": ''
        }
        api_students = self.planner.api_get_students(student_infos).get('data').get('result')
        list_data = []
        for i in api_students:
            gua_id = i.get('gua_id')
            list_data.append(gua_id)
        gua_ids = random.choice(list_data)  # 随机获取一个guaid
        sql_data = self.query.query_jaina_info(table='students', gua_id=gua_ids)  # 拼接sql语句
        return sql_data
