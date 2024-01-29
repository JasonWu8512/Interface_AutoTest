'''
@Author : degg_wang
@Date : 2022/10/18
@File : test_Roadmap
'''
import pytest
import pytest_check as check
from pytest_check import check_func
from config.env.domains import Domains

from business.Eduplatform.ApiEduplatform_hw import ApiRoadmap

@pytest.mark.Eduplatform_hw
@pytest.mark.reg
class TestRoadmap(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path()
        Domains.set_domain(cls.config['hw_eduplatform_url'])
        cls.apiroadmap = ApiRoadmap

    # def testcase1_(self):
    #     '''
    #
    #
    #     :param bid: baby id
    #     :param nodeId: nodeId
    #     :param uid: 用户id
    #     :param localeLang: 地区
    #
    #     :return:
    #         internal server error
    #     '''
    #     resp = self.apiroadmap.ApiRoadmap.api_getLessonMetaInfoV2(self, uid="", bid="123", nodeId="456", localeLang="en_US")
    #
    #     print(resp)
    #     check.equal(resp["code"], 500)
    #     check.equal(resp["message"], "internal server error")


