'''
@Author : degg_wang
@Date : 2022/8/23
@File : test_Lesson1
'''

import pytest
from config.env.domains import Domains

import pytest_check as check
from pytest_check import check_func

from config.env.domains import Domains
from business.Eduplatform.ApiEduplatform import ApiLesson


@pytest.mark.Eduplatform
@pytest.mark.reg
class TestLesson(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['eduplatform_url'])
        cls.apilesson = ApiLesson

    def testcase1_getBabyLessonInfo(self):
        '''
        获取该bid该lesson的完课情况

        :param bid: baby id
        :param lessonId: lessonId 课程id
        '''
        resp = self.apilesson.ApiLesson.api_get_baby_lesson_info(self, bid='123', lessonId='123')
        check.equal(resp["code"], 0)
        print(resp)

    # def testcase1_getBabyLessonInfoListV2(self):
    #     '''
    #     获取该bid该lesson的完课情况
    #
    #     :param bid: baby id
    #     :param lessonId: lessonId 课程id
    #     '''
    #     resp = self.apilesson.(levelId='F1GE',bid='123',paidCurrent99='true',uid='12345')
    #     print(resp)
