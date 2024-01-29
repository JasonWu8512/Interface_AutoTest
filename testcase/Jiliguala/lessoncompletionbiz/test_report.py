# -*- coding: utf-8 -*-
# @Time    : 2021/7/28 10:47 上午
# @Author  : jacky_yuan
# @File    : test_report.py

import pytest

from business.Jiliguala.lessoncompletionbiz.ApiYwDayReport import ApiDayReport
from business.Jiliguala.lessoncompletionbiz.ApiYwWeeklyReport import ApiWeeklyReport
from business.Jiliguala.lessoncompletionbiz.ApiGeWeeklyReport import ApiWeeklyReport
from business.businessQuery import usersQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains

@pytest.mark.lessoncompletionbiz
class TestYwReport(object):
    """
    学习报告接口返回信息展示
    """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.user = UserProperty(cls.config['yw_day_report']['user_yw_day_report_id'])  # 配置文件读取语文日报测试账号信息
        cls.bid_yw_day_report = cls.config['yw_day_report']['baby_yw_day_report_id']  # 配置文件读取语文日报测试账号宝贝
        cls.lessonId_yw_day_report = cls.config['yw_day_report']['lesson_yw_day_report_id']  # 配置文件读取语文日报课程
        cls.bid_yw_weekly_report = cls.config['yw_weekly_report']['baby_yw_weekly_report_id']  # 配置文件读取语文周报测试账号宝贝
        cls.weekId_yw_weekly_report = cls.config['yw_weekly_report']['week_yw_weekly_report_id']  # 配置文件读取语文周报课程
        cls.bid_ma_weekly_report = cls.config['ma_weekly_report']['baby_ma_weekly_report_id']  # 配置文件读取思维周报宝贝
        cls.weekId_ma_weekly_report = cls.config['ma_weekly_report']['week_ma_weekly_report_id']  # 配置文件读取思维周报宝贝
        cls.ge_user = UserProperty(cls.config['ge_weekly_report']['user_ge_weekly_report_id'])  # 配置文件读取语文日报测试账号
        cls.uid_ge_weekly_report = cls.config['ge_weekly_report']['uid_ge_weekly_report_id']  # 配置文件读取英语3.0周报测试账号用户
        cls.start_time_ge_weekly_report = cls.config['ge_weekly_report']['week_ge_start_time']  # 配置文件读取英语3.0周报课程周起始时间
        cls.yw_day_report = ApiDayReport(cls.user.basic_auth)
        cls.yw_weekly_report = ApiWeeklyReport(cls.user.basic_auth)
        cls.ma_weekly_report = ApiWeeklyReport(cls.user.basic_auth)
        cls.ge_weekly_report = ApiWeeklyReport(cls.ge_user.basic_auth)


    @classmethod
    def teardown_class(cls):
        pass

    def test_yw_day_report(self):
        """语文日报接口数据"""
        resp = self.yw_day_report.api_day_report(bid=self.bid_yw_day_report, lessonId=self.lessonId_yw_day_report)
        # print(resp)
        # 断言接口返回成功
        assert resp['code'] == 0
        # 断言接口返回数据中星级为3
        assert resp['data']['star'] == 3
        # 断言接口返回数据中标题为K1周一
        assert resp['data']['title'] == 'K1-周一'

    def test_yw_weekly_report(self):
        """语文周报接口数据"""
        resp = self.yw_weekly_report.api_weekly_report(bid=self.bid_yw_weekly_report, weekId=self.weekId_yw_weekly_report)
        # print(resp)
        # 断言接口返回成功
        assert resp['code'] == 0
        # 断言接口返回数据中uid的数据
        assert resp['data']['userId'] == 'ca8b74f8f05e4dc7bcfac757867ee700'
        # 断言接口返回数据中weekTheme的数据
        assert resp['data']['weekTheme'] == '一日之计在于晨'

    def test_ma_weekly_report(self):
        """思维周报接口数据"""
        resp = self.ma_weekly_report.api_weekly_report(bid=self.bid_ma_weekly_report, weekId=self.weekId_ma_weekly_report)
        # print(resp)
        # 断言接口返回成功
        assert resp['code'] == 0
        # 断言接口返回数据中uid的数据
        assert resp['data']['userId'] == 'ca8b74f8f05e4dc7bcfac757867ee700'
        # 断言接口返回数据中weekTheme的数据
        assert resp['data']['weekInfoModule']['reportTitle'] == '思维K1·周报'

    def test_ge_weekly_report(self):
        """英语3.0课程周报接口数据"""
        resp = self.ge_weekly_report.api_weekly_report(uid=self.uid_ge_weekly_report, startTime=self.start_time_ge_weekly_report)
        # print(resp)
        # 断言接口返回成功
        assert resp['code'] == 0
        # 断言接口返回数据中uid的数据
        assert resp['data']['uid'] == '8751910de5a24dea9abd45d676485cf0'
        # 断言接口返回数据中startTime的数据
        assert resp['data']['startTime'] == '2021-06-21'





