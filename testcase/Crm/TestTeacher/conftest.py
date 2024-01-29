# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/25 10:13 上午
@Author  : Demon
@File    : conftest.py
"""

import pytest
import time

@pytest.fixture(scope='session')
def get_main_subject():
    subjects = {1: 'english', 2: 'math'}
    return subjects

@pytest.fixture()
def get_channels():
    return ['H5', '小程序', 'APP', '天猫', '拼多多', 'H5投放', '京东', '转介绍-钻石商城', '拼团', '推广人', '阿里口碑']

@pytest.fixture()
def get_old_order_itemid():
        return ['BST_DS_T1_2_K1_6_01','BST_DS_K1_6_01','BST_DS_T2_K1_6_SJ_01','BST_DS_K2_6_SJ_01','BST_DS_K1_3_01'
                ,'BST_DS_T1_2_01','BST_DS_K1_2_01','BST_DS_K3_4_01','BST_T1_T2_SJ_01','BST_T1_K2_SJ_01','BST_K1_K2_SJ_01'
                ,'BZR_GE_ST_T1_K6_DS_EB02','BZR_GE_ST_K1_K6_DS_EB02','BZR_GE_ST_K3_K6_DS_EB02','BZR_GE_ST_T1_T2_CG_02'
                ,'BZR_GE_ST_K1_K2_CG_02','BZR_GE_ST_K3_K4_CG_02','BZR_GE_KC_T1_CG_02','BZR_GE_KC_K1_CG_02'
                ,'BZR_GE_KC_K3_CG_02','SST_K1_6_02','SST_K1_2_02','SST_K3_6_02','SST_K3_6_04','BZR_MA_ST_K3_K4_CG_02'
                ,'BZR_MA_ST_K5_K6_CG_02','BZR_MA_ST_K5_K6_YS_02','BZR_MA_ST_K1_K2_CG_02','BZR_MA_CST_K1_K6_CG_02'
                ,'BZR_MA_CST_K3_K6_CG_02','BZR_MA_CST_CG_02','BZR_MA_ST_K1_K6_CG_2','BZR_MA_ST_K3_K6_CG_2'
                ,'BZR_MA_ST_K1_K2_CG_2','BZR_MA_ST_K3_K4_CG_2','BZR_MA_ST_K5_K6_CG_2','BZR_MA_ST_K1_K2_SJ_2'
                ,'BZR_MA_ST_K3_K6_SJ_2','BZR_MA_ST_K5_K6_SJ_2','BZR_MA_CST_K1_K6_CG_2','BZR_MA_CST_K3_K6_CG_2'
                ,'BZR_MA_CST_2','BZR_MA_ST_K1_K2_SJ_4','BZR_MA_ST_K3_K6_SJ_4','BZR_MA_ST_K5_K6_SJ_4'
                ,'BZR_MA_KC_K1_K6_CG_02','BZR_MA_KC_K3_K6_CG_02','BZR_MA_KC_K5_K6_CG_02','BZR_MA_KC_K1_K2_SJ_02'
                ,'BZR_MA_KC_K3_K4_SJ_02','BZR_MA_KC_K1_K4_SJ_02','BZR_MA_CST_K1_K6_SJ_02','BZR_MA_CST_K3_K6_SJ_02'
                ,'BZR_MA_CST_K5_K6_SJ_02','BZR_GE_KC_T1_K6_CG_2','BZR_GE_KC_K1_K6_CG_2','BZR_GE_CST_T1_K6_CG_2'
                ,'BZR_GE_CST_K1_K6_CG_2','BZR_GE_KC_T2_K6_SJ_2','BZR_GE_KC_K2_K6_SJ_2','BZR_GE_KC_K1_K6_SJ_4'
                ,'BZR_GE_KC_K2_K6_SJ_4','BZR_GE_KC_T1_T2_SJ_2','BZR_GE_ST_T1_K6_CG_2','BZR_GE_ST_K1_K6_CG_2'
                ,'BZR_GE_ST_T2_K6_SJ_4','BZR_GE_ST_K2_K6_SJ_4','BZR_GE_ST_T1_T2_SJ_3','BZR_GE_ST_K1_K2_SJ_2'
                ,'BZR_GE_ST_T1_K2_SJ_2','BZR_GE_ST_T2_K6_SJ_2','BZR_GE_ST_K2_K6_SJ_2','BZR_GE_ST_K1_K6_SJ_2'
                ,'BZR_GE_ST_K3_K6_SJ_2','BZR_GE_ST_K5_K6_SJ_2','BZR_GE_ST_T1_K6_CG_EB2','BZR_GE_ST_K1_K6_CG_EB2'
                ,'BZR_GE_KC_T2_CG_2','BZR_GE_KC_K1_CG_2','BZR_GE_ST_F1_S6_CG_2','BZR_GE_ST_S1_S6_CG_2'
                ,'BZR_GE_ST_F2_W7-24_S6_SJ_2','BZR_GE_ST_S1_W7-24_S6_SJ_2','BZR_GE_ST_F1_F2_SJ_2','BZR_GE_ST_S1_S2_SJ_2'
                ,'BZR_GE_ST_F1_S2_SJ_2','BZR_GE_ST_F2_S6_SJ_2','BZR_GE_ST_S2_S6_SJ_2','BZR_GE_ST_S1_S6_SJ_2'
                ,'BZR_GE_ST_S3_S6_SJ_2','BZR_GE_ST_S5_S6_SJ_2','BZR_GE_ST_F1_S6_CG_EB2','BZR_GE_ST_S1_S6_CG_EB2'
                ,'BZR_GE_ST_F2_W1-6_CG_2','BZR_GE_ST_S1_W1-6_CG_2','BZR_ZB_CST_BCJ2','BZR_GE_KC_F1_S6_CG_2'
                ,'BZR_GE_KC_S1_S6_CG_2','BZR_GE_CST_F1_S6_SJ_2','BZR_GE_CST_S1_S6_SJ_2','BZR_GE_KC_F2_S6_SJ_2'
                ,'BZR_GE_KC_S2_S6_SJ_2','BZR_GE_KC_F2_W7-24_S6_SJ_2','BZR_GE_KC_S1_W7-24_S6_SJ_2','BZR_GE_KC_F1_F2_SJ_2'
                ,'BST_T2_K1_6_03','BKC_T2_K1_6_03','BST_K1_6_02','BKC_K1_6_02','BKC_T1_02','BKC_K1_02','BKC_K3_02'
                ,'BST_T1_SJ_02','BST_T1_2_K1_6_02','BST_K1_6_03','BST_K3_6_02','BST_T1_2_02','BST_K1_2_02','BST_K3_4_02'
                ,'BZR_GE_KC_F2_W1-6_CG_2','BZR_GE_KC_S1_W1-6_CG_2','BZR_MA_KC_K1_K2_CG_EB02','BZR_MA_KC_K3_K4_CG_EB02'
				,'BZR_MA_KC_K5_K6_CG_EB02','BZR_MA_ST_K3_K4_SJ_2']

@pytest.fixture(scope='class')
def get_student_infos():
    def payload(**kwargs):
        student_infos = {
            "kpi_cr_email": "",
            "kpi_cr_email_type": "",
            "kpi_dept_uuid": "",
            "kpi_dept_uuid_type": "",
            "stu_info": "",
            "kpi_term": [],
            "order_id": "",
            "ty_lesson_finish_cnt": [],
            "ty_lesson_finish_cnt_type": "",
            "attendance_num_list": [],
            "is_in_wechat_group": None,
            "is_real_add_teacher": None,
            "is_valid_receiver": None,
            "has_recommender": None,
            "custom_label": "",
            "has_kpi_amount": None,
            "subject_type": "english",
            "order_date_range": [],
            "student_tab": "all",
            "is_fc": None
        }
        student_infos.update(**kwargs)
        return student_infos
    return payload

@pytest.fixture(scope='class')
def get_kpi_orders():
    def payload(**kwargs):
        order_infos = {
            "kpi_cr_email": "",
            "kpi_dept_uuid": "",
            "stu_info": "",
            "term": [],
            "order_id": "",
            "order_date_range": [],
            "order_status": "",
            "subject_type": "english"
        }
        order_infos.update(**kwargs)
        return order_infos
    return payload

@pytest.fixture(scope='class')
def get_adoptions_orders():
    def payload(**kwargs):
        order_infos = {
            "adoption_status": "APPROVED",
            "cr_info": {},
            "date_range": [],
            "gua_id": "",
            "order_id": "",
            "subject_type": "english"
        }
        order_infos.update(**kwargs)
        return order_infos
    return payload

@pytest.fixture(scope='class')
def get_teacher_infos():
    def payload(**kwargs):
        search_info = {
            "account_wechat_alias": "",
            "cr_info": {
                "dept_uuid": "",
                "email": ""
            },
            "subject_type": "english",
            "tid": ""
        }
        search_info.update(**kwargs)
        return search_info
    return payload

@pytest.fixture(scope='class')
def get_audit_dict():
    def payload(**kwargs):
        search_info = {
            "order_id": "",
            "approval": True,
            "gua_id": "",
            "subject_type": "english",
            "adoption_type": "ELSE",
            "amount_cent": 1000,
            "audit_comment": "测试审核/修改认领订单",
            "order_pay_time": ""
        }
        search_info.update(**kwargs)
        return search_info
    return payload

@pytest.fixture(scope='class')
def get_raw_push():
    def payload(**kwargs):
        raw_push = {
            "subject_type": "english",
            "uid": "",
            "oid": "AutoTest",
            "opensource": "",
            "itemid": "H5_XX_Sample",
            "lessonIdList": ["K1GETC", "K1MATC"],
            "initiator_uid": "",
            "is_initiator_paidxx": False,
            "bind_status": "pre",
            "assignType": "normal",
            "is_combined_subject": False,
            "pts": int(time.time()*1000),
            "lesson_start_at_same_time": False,
            "marketingChannelCode": ""
        }
        raw_push.update(**kwargs)
        return raw_push
    return payload

@pytest.fixture(scope='class')
def get_update_dicts():
    def payload(**kwargs):
        update_dicts = {
            "kpi_cr_ref_id_normal": [],
            "kpi_cr_ref_id_post_term": [],
            "kpi_cr_ref_id_week1": [],
            "kpi_cr_ref_id_week2": [],
            "kpi_term": ""
        }
        update_dicts.update(**kwargs)
        return update_dicts
    return payload