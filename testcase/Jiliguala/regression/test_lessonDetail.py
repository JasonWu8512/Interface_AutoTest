'''
===============
@Project  :  JLGL_autotest
@Author   :  Anna
@Data     :  2023/04/12
===============
'''
import os
import pytest
import pytest_check as check

from business.Jiliguala.lesson.ApiSuper import ApiSuper
from business.Jiliguala.systemlesson.ApiLiterature import ApiLiterature
from business.Jiliguala.userbiz.Apilearn import Api_Learn_Report
from config.env.domains import Domains
from business.Jiliguala.systemlesson.Apidetail import ApiDetail
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class TestLessonDetail:
    dm = Domains

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取envcd
        cls.env = os.environ.get('env')
        # 【代码提交用】获取环境变量
        # cls.config = cls.dm.set_env_path(cls.env)
        # 【代码提交用】
        print(cls.env)
        # # 本地调试用
        # cls.env = 'fat'
        cls.config = cls.dm.set_env_path(cls.env)
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.detail = cls.config["detail"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.detail['mobile'], p=cls.detail['pwd'])
        print(type(cls.token))
        print(cls.token)
        token = cls.token
        cls.apiDetail = ApiDetail(token)
        cls.learn_report = Api_Learn_Report(token)
        cls.super = ApiSuper(token)
        cls.literature = ApiLiterature(token)
        # 年课体验课账号
        cls.token01 = cls.user.get_token(typ="mobile", u=cls.detail['mobile01'], p=cls.detail['pwd'])
        token01 = cls.token01
        cls.apiDetail01 = ApiDetail(token01)
        cls.learn_report01 = Api_Learn_Report(token01)

        # 年课正价课账号
        cls.token02 = cls.user.get_token(typ="mobile", u=cls.detail['mobile02'], p=cls.detail['pwd'])
        token02 = cls.token02
        cls.apiDetail02 = ApiDetail(token02)
        cls.learn_report02 = Api_Learn_Report(token02)

    """
    步骤：
    1.进入课程详情页
    2.课后报告确认
    
    期望：
    1.详情页无异常
    2.课后报告展示正常
    """

    def testT_Detail(self):
        """体验课"""
        lid = self.detail["lid_t"]
        resp = self.apiDetail.api_detail(self.detail["bid01"], lid)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言当前课程级别为K1GETC
        assert resp['data']['lv'] == 'K1GE'
        # 断言课程标题，不同环境名称不一致
        if self.env == 'fat':
            assert resp['data']['cn_ttl'] == '动画王国'
        else:
            assert resp['data']['cn_ttl'] == '基础表达积累'

        # 进入课后报告
        resp01 = self.learn_report.api_report(self.detail["bid01"], lid)
        print(resp01)
        # 断言接口正常返回
        assert resp01['code'] == 0
        # 断言课程标题，不同环境名称不一致
        if self.env == 'fat':
            assert resp01['data']['cnTitle'] == '动画王国'
        else:
            assert resp01['data']['cnTitle'] == '基础表达积累'
        # 断言课程id与配置一致
        assert resp01['data']['lessons'][0]['lessonId'] == lid

    def test01_Detail(self):
        """1.5课程详情页"""
        lid = self.detail["lid_1"]
        resp = self.super.api_get_lesson_detail(bid=self.detail["bid01"], lesson_click=1, lid=lid, popup='true')
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言课程标题：'美味歌'
        assert resp['data']['cn_ttl'] == '美味歌'
        # 进入课后报告
        resp01 = self.apiDetail.api_lesson_report(bid=self.detail["bid01"], lessonid=lid)
        print(resp01)
        # 断言接口正常返回
        assert resp01['status_code'] == 200
        # 断言课程标题：'基础表达积累'
        assert resp01['data']['nick'] == '宝贝测试'
        # 断言课程id与配置一致
        assert resp01['data']['week'] == 'L1XXW01'

    def test02_Detail(self):
        """2.5课程详情页"""
        lid = self.detail["lid_2"]
        resp = self.apiDetail.api_detail(self.detail["bid01"], lid)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言当前课程级别为K1GE
        assert resp['data']['lv'] == 'K1GE'
        # 断言课程标题：'基础表达积累'
        assert resp['data']['cn_ttl'] == '基础表达积累'
        # 进入课后报告
        resp01 = self.learn_report.api_report(self.detail["bid01"], lid)
        print(resp01)
        # 断言接口正常返回
        assert resp01['code'] == 0
        # 断言课程标题：'基础表达积累'
        assert resp01['data']['cnTitle'] == '基础表达积累'
        # 断言课程id与配置一致
        assert resp01['data']['lessons'][0]['lessonId'] == lid

    def test03_Detail(self):
        """3.0课程详情页"""
        lid = self.detail["lid_3"]
        resp = self.apiDetail.api_detail(self.detail["bid01"], lid)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言当前课程级别为S1GE
        assert resp['data']['lv'] == 'S1GE'
        # 断言课程标题：'动画王国'
        assert resp['data']['cn_ttl'] == '动画王国'
        # 进入课后报告
        resp01 = self.learn_report.api_report(self.detail["bid01"], lid)
        print(resp01)
        # 断言接口正常返回
        assert resp01['code'] == 0
        # 断言课程标题：'动画王国'
        assert resp01['data']['cnTitle'] == '动画王国'
        # 断言课程id与配置一致
        assert resp01['data']['lessons'][0]['lessonId'] == lid

    def testMa_Detail(self):
        """思维课程详情页"""
        lid = self.detail["lid_m"]
        resp = self.apiDetail.api_detail(self.detail["bid01"], lid)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言当前课程级别为S1GE
        assert resp['data']['lv'] == 'K1MA'
        # 断言课程标题：'熊猫宝宝'
        assert resp['data']['cn_ttl'] == '熊猫宝宝'
        # 进入课后报告
        resp01 = self.learn_report.api_report(self.detail["bid01"], lid)
        print(resp01)
        # 断言接口正常返回
        assert resp01['code'] == 0
        # 断言课程标题：'熊猫宝宝'
        assert resp01['data']['cnTitle'] == '熊猫宝宝'
        # 断言课程id与配置一致
        assert resp01['data']['lessons'][0]['lessonId'] == lid

    def testB_Detail(self):
        """国学课程"""
        lid = self.detail["lid_g"]
        resp = self.literature.api_Literature(self.detail["bid01"], lid)
        print(resp)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id和配置一致
        assert resp['data']['_id'] == lid
        # 断言课程标题：'西安·兵马俑'
        assert resp['data']['cn_ttl'] == '西安·兵马俑'

    def testG_Detail(self):
        """百科详情页"""
        lid = self.detail["lid_b"]
        resp = self.literature.api_Literature(self.detail["bid01"], lid)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言课程标题：'濒危动物'
        assert resp['data']['cn_ttl'] == '濒危动物'

    def testYT_Detail(self):
        """年课体验课"""
        lid = self.detail["lib_yt"]
        resp = self.apiDetail01.api_detail(self.detail["bid02"], lid)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言当前课程级别为S1GE
        assert resp['data']['subject'] == 'GE'
        # 断言课程标题：'动画王国'
        assert resp['data']['cn_ttl'] == '词句学习'
        # 进入课后报告
        resp01 = self.learn_report01.api_report(self.detail["bid02"], lid)
        print(resp01)
        # 断言接口正常返回
        assert resp01['code'] == 0
        if self.env == 'fat':
            # 断言课程标题：'词句学习'
            assert resp01['data']['cnTitle'] == '词句学习'
        else:
            assert resp01['data']['cnTitle'] == '基础表达积累'
        # 断言课程id与配置一致
        assert resp01['data']['lessons'][0]['lessonId'] == lid

    def testY_Detail(self):
        """年课正价课"""
        lid = self.detail["lib_y"]
        resp = self.apiDetail02.api_detail(self.detail["bid03"], lid)
        # 断言返回状态码
        check.equal(resp["code"], 0)
        # 断言课程id与配置一致
        assert resp['data']['_id'] == lid
        # 断言当前课程级别为S1GE
        assert resp['data']['subject'] == 'GE'
        # 断言课程标题：'词句学习'
        assert resp['data']['cn_ttl'] == '词句学习'
        # 进入课后报告
        resp01 = self.learn_report02.api_report(self.detail["bid03"], lid)
        print(resp01)
        # 断言接口正常返回
        assert resp01['code'] == 0
        # 断言课程标题：'词句学习'
        assert resp01['data']['cnTitle'] == '词句学习'
        # 断言课程id与配置一致
        assert resp01['data']['lessons'][0]['lessonId'] == lid
