# -*- coding: utf-8 -*-
# @Time : 2023/11/6 上午11:14
# @Author : Saber
# @File : test_report.py


import pytest
import pytest_check as check

from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3
from business.Jiligaga.app.ApiLogin import Login
from business.Jiligaga.app.ApiRoadmapExperienceLessonTake import ApiRoadmapExperienceLessonTake
from business.Jiligaga.app.ApiLearnReport import ApiLearnReport
from config.env.domains import Domains


@pytest.mark.GagaReg
class TestApiReport(object):
    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.ApiLearnReport = ApiLearnReport()

    def test_report_experience(self):
        """
        人转校验体验营第一节课，课后报告
        """

        resp = self.ApiLearnReport.api_learn_report_experience(bid=self.gaga_app["bidsaber"],
                                                               lessonId=self.gaga_app["lessonId01"])
        print(resp)
        # 获取体验营课后报告lesson校验
        lessonX = resp.get('data').get('lessonX')
        print(lessonX)
        # 校验一下是否是体验营的课后报告
        check.equal(lessonX, 'EXPERIENCE_LESSON_1')

    def test_report_lesson(self):
        """
        正价课第一节课，课后报告，人转
        """

        resp = self.ApiLearnReport.api_learn_report(bid=self.gaga_app["bidsaber"],
                                                               lessonId=self.gaga_app["lessonId"])

        type = resp.get('data').get('type')
        print(type)
        # 校验一下是否是正价课的课后报告
        check.equal(type, 'lesson')
