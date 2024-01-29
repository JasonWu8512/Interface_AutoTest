# -*- coding: utf-8 -*-
# @Time : 2021/4/30 10:52 上午
# @Author : Fay
# @File : test_teacher_schedule.py

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check as check
import random
from datetime import datetime
from business.CrmQuery import CrmThrallQuery
from utils.date_helper import get_any_type_time, get_week, get_off_set_time

@pytest.mark.xCrm
@pytest.mark.reg
class TestTeacherSchedule(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.teacher = ApiTeacher(cls.session.cookies)
        cls.query = CrmThrallQuery()


    def get_vaild_TID(self, search_info, type='奇数班次', day=get_week(get_any_type_time(datetime.now(), 'YYYY-MM-DD'))[2]):
        '''获取可参与排班的TID'''
        #获取有效的参数配置
        setting = self.teacher.api_get_settings_v2()['data']['data']
        status_setting, worktime_setting = [], []
        week = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六", 7: "周日"}
        for x in setting['奇偶周']:
            if x['name'] == type:
               valid_group = [val['dept_uuid'] for val in x['value']]
        for y in setting['状态']['valid']:
            if y['content'] == '可排班':
                status_setting.append(y['id'])
        for z in setting['班次']['valid']:
            if week[day] in z['content']:
                worktime_setting.append(z['id'])
        #过滤出参数配置符合条件的TID（状态为'在排班'，班次包含选定日期，奇偶周包含所在组，TID是否排班为'是'）
        data = self.teacher.api_get_teacher_id_wechat_list_v2(search_info, search_size=10000)['data']
        tid_dict = dict(zip('ABCD', [[], [], [], []]))
        for row in data['teacher_list']:
            if row['wechatList']:
                if row['teacherStatus']['setting_uuid'] in status_setting:
                    if row['teacherWorkTime']['setting_uuid'] in worktime_setting:
                        if row['dept_uuid'] in valid_group:
                            for rows in row['wechatList']:
                                if rows['wechatInSchedule'] == 1:
                                    tid_dict[rows['wechatType']].append(rows['id'])
        return tid_dict

    def get_schedule_list(self, days, subject_type="english"):
        '''获取某天在排班的TID'''
        dataA = self.teacher.api_get_cr_schedule_v2(days, 'A', subject_type)['data']
        dataB = self.teacher.api_get_cr_schedule_v2(days, 'B', subject_type)['data']
        dataC = self.teacher.api_get_cr_schedule_v2(days, 'C', subject_type)['data']
        dataD = self.teacher.api_get_cr_schedule_v2(days, 'D', subject_type)['data']
        scheduleA = [row['id'] for row in dataA['schedule_info']['schedule_list']]
        scheduleB = [row['id'] for row in dataB['schedule_info']['schedule_list']]
        scheduleC = [row['id'] for row in dataC['schedule_info']['schedule_list']]
        scheduleD = [row['id'] for row in dataD['schedule_info']['schedule_list']]
        return dict(zip('ABCD', [scheduleA, scheduleB, scheduleC, scheduleD]))


    @pytest.mark.parametrize("subject_type", ['english', 'math'])
    def test_auto_generate_cr_schedule_v2(self, get_teacher_infos, subject_type):
        '''验证一键排班是否正确'''
        tomorrow = get_off_set_time(days=1, fmt='YYYY-MM-DD')
        schedule = self.get_schedule_list(tomorrow, subject_type)
        valid_tid = self.get_vaild_TID(get_teacher_infos(subject_type=subject_type), day=get_week(tomorrow)[2])
        try:
            self.teacher.api_auto_generate_cr_schedule_v2([tomorrow], subject_type)
            schedule2 = self.get_schedule_list(tomorrow, subject_type)
            for row in valid_tid:
                check.equal(len(valid_tid[row]), len(schedule2[row]))
                for rows in valid_tid[row]:
                    check.is_in(rows, schedule2[row])
        finally:
            for row in schedule:
                self.teacher.api_update_cr_schedule_v2(tomorrow, schedule[row], row, subject_type)
            schedule3 = self.get_schedule_list(tomorrow, subject_type)
            check.equal(schedule, schedule3)


    def test_get_cr_schedule_v2(self, get_teacher_infos):
        '''验证排班表信息'''
        today = get_any_type_time(datetime.now(), 'YYYY-MM-DD')
        res = self.teacher.api_get_cr_schedule_v2(today, 'A')
        data = res['data']
        newest_term = self.teacher.api_get_all_schedule_term_list(is_current_transfer=False)['data']['current']
        schedule = self.get_schedule_list(today)
        tid = random.sample(schedule['A'], 1)[0]
        term_student_cnt = self.query.query_table_info(table='crleadstermsummary', term=newest_term, cr_ref_id=tid)[0]['leads_total_count']
        tid_infos = self.teacher.api_get_teacher_id_wechat_list_v2(get_teacher_infos())
        #验证对应的接人期，不同微信号下的排班人数，当期接人量，TID信息
        check.equal(data['term'], newest_term)
        for row in schedule:
            check.equal(data['schedule_info']['schedule_count'][row], len(schedule[row]))
        for row in data['schedule_info']['schedule_list']:
            if row['id'] == tid:
                check.equal(row['term_student_cnt'], term_student_cnt)
