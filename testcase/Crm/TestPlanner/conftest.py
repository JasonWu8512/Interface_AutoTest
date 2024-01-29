# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 4:42 下午
@Author  : Demon
@File    : conftest.py
"""

import pytest


@pytest.fixture()
def get_rebuy_channels():
    return ['app商城', '有赞商城', 'e-shop', '天猫商城']

@pytest.fixture()
def get_wechat_types():
    return ['A', 'B', 'C', '/']

@pytest.fixture()
def get_is_rebuy_targets():
    return ['是', '否', '全部']

@pytest.fixture()
def get_done_lesson_types():
    return ['正常', '异常', '未开始', '全部']

@pytest.fixture()
def get_rebuy_content():
    return ['课程', '教具', '课程+教具', '全部']


@pytest.fixture(scope='class')
def student_info():
    def inner(*args, **kwargs):
        print(args, kwargs)
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

@pytest.fixture(scope='class')
def order_search_info():
    def inner(*args, **kwargs):
        print(args, kwargs)
        param = {
            "stu_info": "",
            "order_id": "",
            "ghs_info": {},
            "period": "",
            "pay_time_start": "",
            "pay_time_end": "",
            "is_in_kpi": "",
            "order_status": "",
            "subject_type": ""
        }
        param.update(kwargs)
        return param
    return inner

@pytest.fixture(scope='class')
def order_infos():
    def inner(*args, **kwargs):
        print(args, kwargs)
        param = {
                "kpi_cr_email": "",
                "kpi_dept_uuid": "",
                "stu_info": "",
                "term": [],
                "order_id": "",
                "order_date_range": [],
                "order_status": "",
                "subject_type": ""
            }
        param.update(kwargs)
        return param
    return inner

@pytest.fixture(scope='class')
def ghs_wechat_infos():
    def inner(*args, **kwargs):
        print(args, kwargs)
        param = {
                "email_address": "",
                "wechat_nick": '',
                "wechat": '',
                "wechat_type": "A",
                "wechat_weights": 1,
                "wechat_code": "https://qiniucdn.jiliguala.com/dev/upload/613b77fe833a4aea98803d13bda9d3e4_20210430041313.jpeg",
                "wechat_account_id": ''
            }
        param.update(kwargs)
        return param
    return inner

if __name__ == '__main__':
    import datetime
    import calendar
    from dateutil.parser import parse
    diff = parse(datetime.datetime.now().strftime('%Y-%m-%d')) - parse('2020-12-10')
    print(student_info)