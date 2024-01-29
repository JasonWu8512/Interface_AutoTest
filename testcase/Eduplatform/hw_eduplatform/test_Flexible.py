'''
@Author : degg_wang
@Date : 2022/10/18
@File : test_Flexible
'''
import pytest
import pytest_check as check
from pytest_check import check_func
from config.env.domains import Domains

from business.Eduplatform.ApiEduplatform_hw import ApiFlexible

@pytest.mark.Eduplatform_hw
@pytest.mark.reg
class TestRoadmap(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path()
        Domains.set_domain(cls.config['hw_eduplatform_url'])
        cls.apiflexible = ApiFlexible


    def testcase1_getBabyLessonNodesInfo(self):
        """
        获取叶节点，叶节点父节点的元数据 + 节点的完课/解锁/拥有 信息-必参校验：bid

        :param bid: baby id
        :param localeLang: 区域
        :param nodeId: 节点id
        :param uid:用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLessonNodesInfo(self,
                                                                       bid = "",
                                                                       uid = "7ccb4ddb96a54f5ebe60da0d01da746d",
                                                                       nodeId = "12ade73d49813a0d8d3aedabf28c0fe6",
                                                                       localeLang = "en_US")

        print(resp)
        check.equal(resp["code"], 500)
        check.equal(resp["msg"], "internal server error")

    def testcase2_getBabyLessonNodesInfo(self):
        """
        获取叶节点，叶节点父节点的元数据 + 节点的完课/解锁/拥有 信息-必参校验：uid

        :param bid: baby id
        :param localeLang: 区域
        :param nodeId: 节点id
        :param uid:用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLessonNodesInfo(self,
                                                                       bid = "05df37a948e945a6aec76006ef3dfc97",
                                                                       uid = "",
                                                                       nodeId = "12ade73d49813a0d8d3aedabf28c0fe6",
                                                                       localeLang = "en_US")

        print(resp)
        check.equal(resp["code"], 500)
        check.equal(resp["msg"], "internal server error")

    def testcase3_getBabyLessonNodesInfo(self):
        """
        获取叶节点，叶节点父节点的元数据 + 节点的完课/解锁/拥有 信息-必参校验：nodeid

        :param bid: baby id
        :param localeLang: 区域
        :param nodeId: 节点id
        :param uid:用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLessonNodesInfo(self,
                                                                       bid = "05df37a948e945a6aec76006ef3dfc97",
                                                                       uid = "7ccb4ddb96a54f5ebe60da0d01da746d",
                                                                       nodeId = "",
                                                                       localeLang = "en_US")

        print(resp)
        check.equal(resp["code"], 500)
        check.equal(resp["msg"], "internal server error")

    def testcase4_getBabyLessonNodesInfo(self):
        """
        获取叶节点，叶节点父节点的元数据 + 节点的完课/解锁/拥有 信息-正例

        :param bid: baby id
        :param localeLang: 区域
        :param nodeId: 节点id
        :param uid:用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLessonNodesInfo(self,
                                                                       bid = "05df37a948e945a6aec76006ef3dfc97",
                                                                       uid = "7ccb4ddb96a54f5ebe60da0d01da746d",
                                                                       nodeId = "12ade73d49813a0d8d3aedabf28c0fe6",
                                                                       localeLang = "en_US")

        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["nodeCode"], "B1GEF001")

    def testcase1_getBabyLevelNodesInfo(self):
        """
        获取level+根节点下两层的节点元数据 + 节点的完课/解锁/拥有 信息-必参校验：bid

        :param bid:   孩子id
        :param levelId:   级别id
        :param localeLang: 多语言配置
        :param uid: 用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLevelNodesInfo(self,
                                                                      bid = "",
                                                                      uid = "626758eb194d452782df5ebe41f9499e",
                                                                      levelId = "2f4d023a52024a9683229273c908ca24",
                                                                      localeLang = "en_US")
        print(resp)
        check.equal(resp["code"], 500)
        check.equal(resp["msg"], "internal server error")

    def testcase2_getBabyLevelNodesInfo(self):
        """
        获取level+根节点下两层的节点元数据 + 节点的完课/解锁/拥有 信息-必参校验：uid

        :param bid:   孩子id
        :param levelId:   级别id
        :param localeLang: 多语言配置
        :param uid: 用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLevelNodesInfo(self,
                                                                      bid = "2806dca8660149549104b46b833e7f96",
                                                                      uid = "",
                                                                      levelId = "2f4d023a52024a9683229273c908ca24",
                                                                      localeLang = "en_US")
        print(resp)
        check.equal(resp["code"], 500)
        check.equal(resp["msg"], "internal server error")

    def testcase3_getBabyLevelNodesInfo(self):
        """
        获取level+根节点下两层的节点元数据 + 节点的完课/解锁/拥有 信息-必参校验：levelId

        :param bid:   孩子id
        :param levelId:   级别id
        :param localeLang: 多语言配置
        :param uid: 用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLevelNodesInfo(self,
                                                                      bid = "2806dca8660149549104b46b833e7f96",
                                                                      uid = "626758eb194d452782df5ebe41f9499e",
                                                                      levelId = "",
                                                                      localeLang = "en_US")
        print(resp)
        check.equal(resp["code"], 500)
        check.equal(resp["msg"], "internal server error")

    def testcase4_getBabyLevelNodesInfo(self):
        """
        获取level+根节点下两层的节点元数据 + 节点的完课/解锁/拥有 信息-正例

        :param bid:   孩子id
        :param levelId:   级别id
        :param localeLang: 多语言配置
        :param uid: 用户id

        :return:
            internal server error
        """
        resp = self.apiflexible.ApiFlexible.api_getBabyLevelNodesInfo(self,
                                                                      bid = "2806dca8660149549104b46b833e7f96",
                                                                      uid = "626758eb194d452782df5ebe41f9499e",
                                                                      levelId = "2f4d023a52024a9683229273c908ca24",
                                                                      localeLang = "en_US")
        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["levelCode"], "B1GE")
        check.equal(resp["data"]["levelName"], "Level 1")


    def testcase1_getUserPossessLevelInfoV2(self):
        """
        获取level列表，包含了是否解锁，是否是当前级别，学习进度-正例

        :param bid:   孩子id
        :param curriculumId:   课程Id
        :param uid: 用户id

        :return:

        """
        resp = self.apiflexible.ApiFlexible.api_getUserPossessLevelInfoV2(self,
                                                                          bid="294fa4f800974570b8a55f123df8cf86",
                                                                          uid="45b39e23288040c79d6a7e9236ded16e",
                                                                          curriculumId="8abce82b12be41a092ae39563dad97f4")
        print(resp)

        check.equal(resp["code"], 0)
        check.equal(resp["data"][0]["levelId"], "2f4d023a52024a9683229273c908ca24")
        check.equal(len(resp["data"]), 7)