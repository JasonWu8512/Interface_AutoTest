'''
@Author : degg_wang
@Date : 2022/9/8
@File : test_Study
'''

import pytest
import pytest_check as check
from pytest_check import check_func

from config.env.domains import Domains
from business.Eduplatform.ApiEduplatform_hw import ApiStudyReport


@pytest.mark.Eduplatform_hw
@pytest.mark.reg
class TestStudy(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path()
        Domains.set_domain(cls.config['hw_eduplatform_url'])
        # cls.account= cls.config["hw_eduplatform_account"]
        cls.apistudyreport = ApiStudyReport

    def testcase1_getBabyStudyReport(self):
        '''
        获取该bid该lesson的学习报告-uid必参校验

        :param bid: baby id
        :param lessonId: lessonId 课程id
        :param uid:用户id

        :return:
            param uid not be null
        '''
        resp = self.apistudyreport.ApiStudyReport.api_get_baby_study_report(self, uid="", bid="123", lessonId="456")
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param uid not be null")

        # print(resp)
    def testcase2_getBabyStudyReport(self):
        '''
        获取该bid该lesson的学习报告-bid必参校验

        :param bid: baby id
        :param lessonId: lessonId 课程id
        :param uid:用户id

        :return:
            param bid not be null
        '''
        resp = self.apistudyreport.ApiStudyReport.api_get_baby_study_report(self, uid="123",
                                                                            bid="",
                                                                            lessonId="789")
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param bid not be null")

    def testcase3_getBabyStudyReport(self):
        '''
        获取该bid该lesson的学习报告-lessonId必参校验

        :param bid: baby id
        :param lessonId: lessonId 课程id
        :param uid:用户id

        :return:
            param lessonId not be null
        '''
        resp = self.apistudyreport.ApiStudyReport.api_get_baby_study_report(self, uid="123",
                                                                            bid="456",
                                                                            lessonId="")
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param lessonId not be null")

    def testcase4_getBabyStudyReport(self):
        '''
        获取该bid该lesson的学习报告-正例

        :param bid: baby id
        :param lessonId:  课程id
        :param uid:用户id

        :return:
          {'code': 0, 'data': {'directKnowledgeList': [{'sublessonId': '4628b78469bb3478928f286ae2d8b832', 'realScore': 39, 'audioUrl': 'https://inter-user-fat-1307651193.cos.ap-singapore.myqcloud.com/image/36ac758bde314b379547a68099fc8a37.mp3', 'knowledgeId': 'GEKWP7066399', 'knowledgeText': 'car', 'audioUrlStandard': 'https://qiniucdn.jiligaga.com/resource/crmprod/bd5c01cc6f6a4a2482ab4103446fcd42-k_GEKWP7066399.mp3', 'answerText': 'car', 'displayScore': 39, 'audioTag': '智聆_英文单词评测_幼儿2', 'finishTime': 1655288381702}], 'lessonSequence': 1}, 'requestId': 'a3c0dbed3caac3ac', 'status_code': 200
        '''
        resp = self.apistudyreport.ApiStudyReport.api_get_baby_study_report(self, uid="123",
                                                                            bid="393ca6236a9547b484951a00adb1cbe2",
                                                                            lessonId="12ade73d49813a0d8d3aedabf28c0fe6")
        # print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["directKnowledgeList"][0]["knowledgeId"], "GEKWP7066399")

    def testcase1_getBabyInspireReport(self):
        '''
        获取该bid该nodeId的课后报告-正例

        :param bid: baby id
        :param nodeId: 节点id
        :param uid:用户id

        :return:

        '''

        resp = self.apistudyreport.ApiStudyReport.api_get_baby_Inspire_report(self,

                                                                            bid="04cbcb4309244c95a883b983872c59f0",
                                                                            nodeId="07a3181025bd36838056aea34f3e31e1")
        # print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["nodeId"], "07a3181025bd36838056aea34f3e31e1")
        check.equal(resp["data"]["nodeName"], "Lesson 5")
