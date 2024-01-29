# -*- coding: utf-8 -*-
"""
@Time    : 2021/05/31
@Author  : Grace
@File    : conftest.py
"""

import pytest


@pytest.fixture(scope='class')
def search_promoter_infos():
    def inner(**kwargs):
        search_info = {
            "promoter_info": "",
            "promoter_level": "",
            "promoter_wechat_id": "",
            "invite_person_count": [],
            "promote_order_count": [],
            "register_time": [],
            "rise_time": [],
            "remark": "",
            "first_buy_count": [],
            "fans_count": [],
            "leader_id": None,
            "period": "",
            "promoter_indentity": "",
            "promoter_tag": "",
            "group_type": None
        }
        search_info.update(**kwargs)
        return search_info
    return inner


@pytest.fixture(scope='class')
def search_promoter_relationship():
    def inner(**kwargs):
        search_info = {
            "promoter_info": "",
            "fens_info": "",
            "order_subject": "",
            "relation_type": "",
            "tag": ""
        }
        search_info.update(**kwargs)
        return search_info
    return inner

@pytest.fixture(scope='class')
def search_promoter_order():
    def inner(**kwargs):
        search_info = {
            "order_info": "",
            "promoter_identity": "",
            "promoter_level": "",
            "create_time": [],
            "revenue_status": "",
            "payment_time": [],
            "subject_category": "",
            "leader_id": "",
            "period": "",
            "relation_type": "",
            "course_type": "",
            "group_type": ""
        }
        search_info.update(**kwargs)
        return search_info
    return inner
@pytest.fixture(scope='class')
def promoter_leader_search_infos():
    def inner(**kwargs):
        search_info = {
            "email": "",
            "name": "",
            "mobile": "",
            "member_assignment_status": ""
        }
        search_info.update(**kwargs)
        return search_info
    return inner
@pytest.fixture(scope='class')
def add_leader_info():
    def inner(**kwargs):
        search_info = {
            "group_type": "",
            "wechat_type": "",
            "work_time_type": "",
            "email": "",
            "mobile": "",
            "name": "",
            "wechat_account": "",
            "wechat_qrcode_image_url": ""
        }
        search_info.update(**kwargs)
        return search_info
    return inner

@pytest.fixture(scope='class')
def search_infos():
    def inner(**kwargs):
        search_info = {
		"email": "",
		"operate_status": "",
		"operation_day": "",
		"sn": ""
        }
        search_info.update(**kwargs)
        return search_info
    return inner

@pytest.fixture(scope='class')
def achievement_search_info():
    def inner(**kwargs):
        search_info = {
			"leader_id": "",
			"operation_date": "",
			"period": "",
			"recruit_type": "",
			"subject_type": ""
		}
        search_info.update(**kwargs)
        return search_info
    return inner