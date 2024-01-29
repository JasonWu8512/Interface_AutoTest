# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 4:25 下午
@Author  : Demon
@File    : test_planner_students_info.py
"""


import pytest
from config.env.domains import Domains
from utils.format.format import get_file_absolute_path
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.Crm.ApiShare.ApiShare import ApiShare
import pytest_check
from utils.date_helper import get_any_type_time
from dateutil.parser import parse
import datetime
from utils.date_helper import diff_weeks, get_diff_days
from utils.date_helper import get_off_set_time

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
        cls.share = ApiShare(cls.session.cookies)

    @pytest.fixture(scope='class')
    def get_students_config(self, **kwargs):
        def inner(*args, **kwargs):
            param = {
                "ghs_info": {},
                "stu_info": "",
                "period": [],
                "wechat_type": "",
                "lesson_status": "",
                "is_add_ghs_flag": None,
                "is_has_lesson": "",
                "is_finish_aim_user": "",
                "buy_days": "",
                "lesson_complete": [None, None],
                "rebuy_status": "",
                "rebuy_content": "",
                "is_refund": "",
                "total_check_times": [None, None],
                "referral_num": [None, None],
                "is_referral": "",
                "user_flag": "",
                "student_tab": "all",
                "rebuy_channel": []
            }
            param.update(kwargs)
            return param

        return inner

    # @pytest.mark.reg
    def test_is_buy_days(self, get_students_config):
        """已购买天数校验"""
        data = self.planner.api_get_students(get_students_config(), sorts=[["gmk_first_buy_date", "desc"]]).get('data')
        for row in data.get('result'):
            apidate = get_any_type_time(row['gmk_first_buy_date'], fmt='YYYY-MM-DD')
            # diff = parse(datetime.datetime.now().strftime('%Y-%m-%d')) - parse(apidate)
            diff = get_diff_days(apidate)
            # print(parse(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            pytest_check.equal(diff + 1, row['has_buy_days'])

    # @pytest.mark.reg
    def test_is_buy_weeks(self, get_students_config):
        """已购买周校验:做验证"""
        data = self.planner.api_get_students(get_students_config(), sorts=[["gmk_first_buy_date", "desc"]]).get('data')
        for row in data.get('result'):
            first_buy = get_any_type_time(row['gmk_first_buy_date'], fmt='YYYY-MM-DD')
            wke = diff_weeks(start_time=first_buy)
            pytest_check.equal(f'week {wke}', row['has_buy_weeks'])

    # @pytest.mark.reg
    def test_not_study_days(self, get_students_config):
        """连续未学天数校验"""
        data = self.planner.api_get_students(get_students_config(), sorts=[["gmk_first_buy_date", "desc"]]).get('data')
        for row in data.get('result'):
            recent_check_time = row.get('recent_check_time')
            if recent_check_time:
                apidate = get_any_type_time(recent_check_time, fmt='YYYY-MM-DD')
                diff = parse(datetime.datetime.now().strftime('%Y-%m-%d')) - parse(apidate)
                pytest_check.equal(diff.days, row['not_check_days'])

    # @pytest.mark.reg
    def test_rebuy_channel(self, get_students_config, get_rebuy_channels):
        """复购渠道校验"""
        data = self.planner.api_get_students(get_students_config(), sorts=[["gmk_first_buy_date", "desc"]]).get('data')
        for row in data.get('result'):
            if row['rebuy_channel']:
                pytest_check.is_in(row.get('rebuy_channel'), get_rebuy_channels)

    # @pytest.mark.reg
    def test_wechat_type(self, get_students_config, get_wechat_types):
        """微信类型校验"""
        data = self.planner.api_get_students(get_students_config(), sorts=[["gmk_first_buy_date", "desc"]]).get('data')
        for row in data.get('result'):
            if row['wechat_type']:
                pytest_check.is_in(row.get('wechat_type'), get_wechat_types)

    # @pytest.mark.reg
    @pytest.mark.parametrize('filepath', [(get_file_absolute_path('kb37.jpeg'))])
    def test_create_comment_success(self, get_students_config, filepath):
        """备注新增成功
        1.校验文本内容，包含特殊字符
        2.校验图片信息（图片blob对象）
        """
        # 查询学员信息
        conf = get_students_config()
        data = self.planner.api_get_students(conf, sorts=[["gmk_first_buy_date", "desc"]]).get('data')
        # print(data)
        for student in data['result']:
            print(student)
            # if student['tel_number'] == user_phone:
            comment = get_off_set_time(fmt='YYYY-MM-DD HH:mm:SS') + 'commented by myself, !@#$%^&*()[]{}【】「」'
            # pytest_check.equal(student['gua_id'], '59832577')

            file_url = self.share.api_upload_file(file_path=filepath).get('data')
            self.share.api_create_student_comment(
                uid=student['user_id'],
                own=student['head_comment']['commenter_account_uuid'],
                comment=comment,
                pictures=[file_url]
            )
            comm = self.share.api_get_student_comments(
                own=student['head_comment']['commenter_account_uuid'], uid=student['user_id']
            )
            # print(comm)
            pytest_check.equal(comm.get('data')[0]['comment_content'], comment) # comm[0] 最近一次评论
            pytest_check.equal(comm.get('data')[0]['pictures'][0], file_url)
            break

    @classmethod
    def teardown_class(cls):
        """当前类结束后默认执行方法"""
        cls.session.logout()
        # print(cls.session.get_cookie)
