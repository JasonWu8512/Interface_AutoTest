'''
@Author : degg_wang
@Date : 2022/9/26
@File : test_RoadmapStudy
'''
import pytest
import pytest_check as check
from pytest_check import check_func
from business.Eduplatform.ApiEduplatform_hw import ApiRoadmapStudy
from config.env.domains import Domains

@pytest.mark.Eduplatform_hw
@pytest.mark.reg
class TestRoadmapStudy(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path()
        Domains.set_domain(cls.config['hw_eduplatform_url'])
        cls.apiroadmapstudy = ApiRoadmapStudy

    def testcase1_leafNodeComplete(self):
        '''
            叶节点完课-必参校验：bid

        :param bid: baby id
        :param nodeId: nodeId
        :param finishTime: 完成时间
        :param score: 分数

        :return:
            param bid not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_leafNodeComplete(self,
                                                                       bid="",nodeId="4628b78469bb3478928f286ae2d8b832",
                                                                       finishTime="1646286444515",
                                                                       score="90")
        print(resp)
        # check.equal(resp["status"], 500)
        # check.equal(resp["message"], "param bid not be null")
        check.is_in("param bid not be null",resp["message"],msg="bcl")

    def testcase2_leafNodeComplete(self):
        '''
            叶节点完课-必参校验：finishTime

        :param bid: baby id
        :param nodeId: nodeId
        :param finishTime: 完成时间
        :param score: 分数

        :return:
            param finishTime not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_leafNodeComplete(self,
                                                                       bid="ac1a6bb4a7b14c429e4cf50f3b48ef87",nodeId="4628b78469bb3478928f286ae2d8b832",
                                                                       finishTime="",
                                                                       score="90")
        print(resp)
        # check.equal(resp["status"], 500)
        # check.equal(resp["message"], "param bid not be null")
        check.is_in("param finishTime not be null",resp["message"],msg="bcl")

    def testcase3_leafNodeComplete(self):
        '''
            叶节点完课-必参校验：nodeId

        :param bid: baby id
        :param nodeId: nodeId
        :param finishTime: 完成时间
        :param score: 分数

        :return:
            param nodeId not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_leafNodeComplete(self,
                                                                       bid="ac1a6bb4a7b14c429e4cf50f3b48ef87",nodeId="",
                                                                       finishTime="1646286444515",
                                                                       score="90")
        print(resp)
        # check.equal(resp["status"], 500)
        # check.equal(resp["message"], "param bid not be null")
        check.is_in("param nodeId not be null",resp["message"],msg="bcl")

    def testcase4_leafNodeComplete(self):
        '''
            叶节点完课-必参校验：nodeId

        :param bid: baby id
        :param nodeId: nodeId
        :param finishTime: 完成时间
        :param score: 分数

        :return:
            param nodeId not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_leafNodeComplete(self,
                                                                       bid="ac1a6bb4a7b14c429e4cf50f3b48ef87",nodeId="",
                                                                       finishTime="1646286444515",
                                                                       score="90")
        print(resp)
        # check.equal(resp["status"], 500)
        # check.equal(resp["message"], "param bid not be null")
        check.is_in("param nodeId not be null",resp["message"],msg="bcl")
    def testcase5_leafNodeComplete(self):
        '''
            叶节点完课-正例：

        :param bid: baby id
        :param nodeId: nodeId
        :param finishTime: 完成时间
        :param score: 分数

        :return:

        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_leafNodeComplete(self,
                                                                       bid="ac1a6bb4a7b14c429e4cf50f3b48ef87",nodeId="12ade73d49813a0d8d3aedabf28c0fe6",
                                                                       finishTime="1646286444515",
                                                                       score="90")
        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 0)
        # check.is_in("param nodeId not be null",resp["message"],msg="bcl")



    def testcase1_setUserCurrentLevel(self):
        '''
            设置用户当前所在级别-正例：

        :param bid: baby id
        :param uid: 用户ID
        :param levelId: 级别ID

        :return:
            param nodeId not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_setUserCurrentLevel(self,
                                                                       bid="45b39e23288040c79d6a7e9236ded16e",uid="294fa4f800974570b8a55f123df8cf86",
                                                                       levelId="3b30c06ed96f497fbe40d20ee4e509b6")
        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 0)


    def testcase2_setUserCurrentLevel(self):
        '''
            设置用户当前所在级别-必参校验：uid

        :param bid: baby id
        :param uid: 用户ID
        :param levelId: 级别ID

        :return:
            param uid not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_setUserCurrentLevel(self,
                                                                       bid="45b39e23288040c79d6a7e9236ded16e",uid="",
                                                                       levelId="3b30c06ed96f497fbe40d20ee4e509b6")
        print(resp)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param uid not be null")


    def testcase3_setUserCurrentLevel(self):
        '''
            设置用户当前所在级别-必参校验：bid

        :param bid: baby id
        :param uid: 用户ID
        :param levelId: 级别ID

        :return:
            param bid not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_setUserCurrentLevel(self,
                                                                       bid="",uid="294fa4f800974570b8a55f123df8cf86",
                                                                       levelId="3b30c06ed96f497fbe40d20ee4e509b6")
        print(resp)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param bid not be null")


    def testcase4_setUserCurrentLevel(self):
        '''
            设置用户当前所在级别-必参校验：levelId

        :param bid: baby id
        :param uid: 用户ID
        :param levelId: 级别ID

        :return:
            param levelId not be null
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_setUserCurrentLevel(self,
                                                                       bid="45b39e23288040c79d6a7e9236ded16e",uid="294fa4f800974570b8a55f123df8cf86",
                                                                       levelId="")
        print(resp)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param levelId not be null")


    def testcase1_skipLesson(self):
        '''
            跳过课程-正例：

        :param bid: baby id
        :param uid: 用户ID
        :param nodeId: nodeId

        :return:
            {'code': 0, 'data': {'nextLessonId': '', 'secondLessonId': ''}
        '''
        resp=self.apiroadmapstudy.ApiRoadmapStudy.api_skipLesson(self,
                                                                       bid="05df37a948e945a6aec76006ef3dfc97",uid="7ccb4ddb96a54f5ebe60da0d01da746d",
                                                                       nodeId="ca6dfda037743e648f96385549656e4c")
        print(resp)
        check.equal(resp["code"], 0)
        # check.equal(resp["message"], "param levelId not be null")



