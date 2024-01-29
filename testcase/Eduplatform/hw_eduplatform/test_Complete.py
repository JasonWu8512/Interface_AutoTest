'''
@Author : degg_wang
@Date : 2022/10/25
@File : test_Complete
'''
import time

import pytest
import pytest_check as check
from pytest_check import check_func
from config.env.domains import Domains

from datetime import datetime
from business.Eduplatform.ApiEduplatform_hw import ApiComplete

@pytest.mark.Eduplatform_hw
@pytest.mark.reg
class TestComplete(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path()
        Domains.set_domain(cls.config['hw_eduplatform_url'])
        cls.apicomplete = ApiComplete

    def testcase1_webComplete(self):
        """
            web编辑器课程知识点分数上报

        :param bid:   孩子id
        :param score:   分数
        :param lessonId: 课程id
        :param sublessonId: 子课程id
        :param gameId: gameId
        :param sectionId: sectionId
        :param finishTime: 完成时间
        :param details: details

        :return:

        """
        finishTime=int(round(time.time() * 1000))
        resp=self.apicomplete.ApiComplete.api_webComplete(self,
                                                          bid="deggtest_1025",
                                                          score="100",
                                                          lessonId="776c6c8c3f203c06b4ae03d02c3a6cef",
                                                          sublessonId="60da704637c536a4ad76f255f7b3afcd",
                                                          gameId="gameIdtest031",
                                                          sectionId="scetion031",
                                                          finishTime=finishTime,
                                                          details=[{
                                                                "knowledgeId": "testKnowledge012",
                                                                "skillId": "testSkill012",
                                                                "fixedType": 1,
                                                                "displayScore": 94,
                                                                "realScore": 93,
                                                                "audioUrl": "url1-1",
                                                                "audioTag": "tag1-1",
                                                                "ruleType": "test1",
                                                                "audioDecibel":58,
                                                                "predScore":77,
                                                                "gamePredId":"gamePredIdtest2"
                                                            }])

        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 0)


    def testcase1_geComplete(self):
        """
            cocos编辑器课程完课上报知识点

        :param bid:   孩子id
        :param score:   分数
        :param lessonId: 课程id
        :param sublessonId: 子课程id
        :param gameId: gameId
        :param sectionId: sectionId
        :param sectionType: sectionType
        :param finishTime: 完成时间
        :param special: 是否为非固定知识点（true-非固定知识点，false-固定知识点）
        :param detail: detail
        :param roundDetail: roundDetail
        :param sentenceDetail: sentenceDetail

        :return:

        """

        finishTime=int(round(time.time() * 1000))
        resp=self.apicomplete.ApiComplete.api_cocosComplete(self,
                                                            bid="testdegg1025",
                                                            score="99",
                                                            lessonId="2d41bf4571a9383cba030f4d0233a286",
                                                            sublessonId="6a43840c9b2b397e9b2ef101cba151f6",
                                                            gameId="B1GEW03D3L3",
                                                            sectionId="S1GEW03D3L3sec05",
                                                            sectionType="speak-new",
                                                            finishTime=finishTime,
                                                            special="false",
                                                            detail=[
                                                                {
                                                                    "displayScore": 91,
                                                                    "realScore": 91,
                                                                    "audioUrl": "https://inter-user-fat-1307651193.cos.ap-singapore.myqcloud.com/image/2ebd9bf2f2bd4e83866f9405cf6512ae.mp3",
                                                                    "audioTag": "智聆_英文单词评测_幼儿2"
                                                                }
                                                            ],
                                                            roundDetail=[],
                                                            sentenceDetail=[])

        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 0)
