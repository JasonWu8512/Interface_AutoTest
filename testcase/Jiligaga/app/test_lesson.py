# -*- coding: utf-8 -*-
# @Time : 2022/10/23 下午6:32
# @Author : Saber
# @File : test_lesson.py

import pytest
import time
import pytest_check as check
from config.env.domains import Domains
from business.Jiligaga.app.ApiLogin import Login
from business.Jiligaga.app.ApiLesson import ApiLesson
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3
from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiSkip import ApiSkip
from business.Jiligaga.app.ApiRoadmapExperienceLessonTake import ApiRoadmapExperienceLessonTake
from business.Jiligaga.app.ApiUsertest import ApiMarktestaccount
from business.Jiligaga.app.ApiCompleteCourse import ApiCompleteCourse
from business.Jiligaga.app.ApiRoadmapQuery import ApiRoadmapQuery
from business.Eduplatform.ApiEduplatform_hw.ApiRoadmapStudy import ApiRoadmapStudy
from business.Jiligaga.app.ApiRedeem import ApiRedeem
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth


@pytest.mark.GagaReg
class TestLesson(object):
    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        # 获取配置文件的手机号
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        cls.config = cls.dm.set_env_path('fat')
        cls.sso = cls.dm.set_env_path('fat')["sso"]
        cls.apiredeem = ApiRedeem()
        cls.apilesson = ApiLesson()
        cls.login = Login()
        cls.apiAccountV3 = ApiAccountV3()
        cls.apiAccount = ApiAccount()
        cls.apiadminauth = ApiAdminAuth()
        cls.apiroadmapstudy = ApiRoadmapStudy()

    def test_api_lesson_detail_v2_get(self):
        """
        获取课程详情页数据能调通
        """

        # 手机号密码登录
        # resp0 = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone"])
        resp0 = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                 countrycode=self.gaga_app["countryCodeTw"])
        # 获取token
        authorization = resp0["data"]["auth"]
        print(authorization)
        bid = self.gaga_app["bidsaber"]
        print(bid)
        self.Authapi_Lesson = ApiLesson(token=authorization)
        resp = self.Authapi_Lesson.api_lesson_detail_v2(bid=bid,
                                                        lid='12ade73d49813a0d8d3aedabf28c0fe6')
        check.equal(resp["code"], 0)

    def test_api_lesson_detail_v2_completed(self):
        """
        获取课程详情页数据level1 lesson1 sublesson1 completed状态
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone08"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone08"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone08"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        # 获取token
        authorization = resp1["data"]["auth"]
        # 调用领取接口，领取体验课
        self.apiroadmapexperiencelessontake = ApiRoadmapExperienceLessonTake(token=authorization)
        resp = self.apiroadmapexperiencelessontake.api_roadmap_experience_lessontake(source=self.gaga_app["source02"])
        # 标注测试账号
        apimarktestaccount = ApiMarktestaccount()
        apimarktestaccount.api_mark_testaccount(areacode=self.gaga_app["countrytw"], phone=self.gaga_app["phone08"])
        # 修改开课时间
        time.sleep(6)
        uid = resp1["data"]["user"]["userNo"]
        starttime = int(round(time.time() * 1000))
        apicompletecourse = ApiCompleteCourse()
        apicompletecourse.course_schedule_update(uid=uid, starttime=starttime)
        bid = resp1["data"]["user"]["babyList"][0]["bid"]
        apiroadmapquery = ApiRoadmapQuery(token=authorization, appversion='1.30.0')
        resp = apiroadmapquery.api_roadmap_query(bid=bid)
        # 完成第一节体验营的课程
        lid = resp["data"]["roadmap"]["elements"][1]["lessons"][0]["id"]
        Domains.set_domain(self.config['hw_eduplatform_url'])
        apilesson = ApiLesson(token=authorization)
        nodeId = apilesson.api_lesson_detail_v2(bid=bid, lid=lid)
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][0]["_id"],
                                                  score="90")
        self.Authapi_Lesson = ApiLesson(token=authorization)
        resp = self.Authapi_Lesson.api_lesson_detail_v2(bid=bid, lid=lid)
        status = resp.get('data').get('subs')[0].get('status')
        print(status)
        check.equal(status, 'completed')
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_api_lesson_detail_v2_skipped(self):
        """
        获取课程详情页数据level1 lesson2 sublesson2 absent状态
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone08"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone08"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone08"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        # 获取token
        authorization = resp1["data"]["auth"]

        """输入有效的的兑换码兑换"""
        t = int(round(time.time() * 1000))
        t1 = t + 100000
        # 获取商城后台token
        a_token = self.apiadminauth.api_login(username=self.sso["email"], password=self.sso["pw"])["data"][
            "token"]
        print(a_token)
        # 获取兑换码
        self.apiredeem = ApiRedeem(token=a_token)
        print(self.apiredeem)
        redeemNo = self.apiredeem.redeeming(startTime=t, expireTime=t1)["data"][0]
        self.apiredeem = ApiRedeem(token=authorization)
        # 兑换码兑换
        resp = self.apiredeem.api_redeem_redeeming(redeemNo=redeemNo)["msg"]
        # 标注测试账号
        apimarktestaccount = ApiMarktestaccount()
        apimarktestaccount.api_mark_testaccount(areacode=self.gaga_app["countrytw"], phone=self.gaga_app["phone08"])
        apiroadmapquery = ApiRoadmapQuery(token=authorization, appversion='1.30.0')
        bid = resp1["data"]["user"]["babyList"][0]["bid"]
        resp = apiroadmapquery.api_roadmap_query(bid=bid)
        # 跳过第一节课程
        lid = resp["data"]["roadmap"]["elements"][1]["lessons"][0]["id"]
        apiskip = ApiSkip(authorization)
        apiskip.skip(lid=lid, bid=bid)
        self.Authapi_Lesson = ApiLesson(token=authorization)
        resp = self.Authapi_Lesson.api_lesson_detail_v2(bid=bid, lid=lid)
        status = resp.get('data').get('subs')[1].get('status')
        check.equal(status, 'locked')
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_api_lesson_detail_v2_locked(self):
        """
        获取课程详情页数据level1 lesson2 sublesson2 locked状态
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone08"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone08"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone08"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        # 获取token
        authorization = resp1["data"]["auth"]
        # 调用领取接口，领取体验课
        self.apiroadmapexperiencelessontake = ApiRoadmapExperienceLessonTake(token=authorization)
        resp = self.apiroadmapexperiencelessontake.api_roadmap_experience_lessontake(source=self.gaga_app["source02"])
        # 标注测试账号
        apimarktestaccount = ApiMarktestaccount()
        apimarktestaccount.api_mark_testaccount(areacode=self.gaga_app["countrytw"], phone=self.gaga_app["phone08"])
        # 修改开课时间
        time.sleep(6)
        uid = resp1["data"]["user"]["userNo"]
        starttime = int(round(time.time() * 1000))
        apicompletecourse = ApiCompleteCourse()
        apicompletecourse.course_schedule_update(uid=uid, starttime=starttime)
        bid = resp1["data"]["user"]["babyList"][0]["bid"]
        apiroadmapquery = ApiRoadmapQuery(token=authorization, appversion='1.30.0')
        resp = apiroadmapquery.api_roadmap_query(bid=bid)
        # 完成第一节体验营的课程
        lid = resp["data"]["roadmap"]["elements"][1]["lessons"]
        Domains.set_domain(self.config['hw_eduplatform_url'])
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=lid[0]["id"],
                                                  score="90")
        self.Authapi_Lesson = ApiLesson(token=authorization)
        resp = self.Authapi_Lesson.api_lesson_detail_v2(bid=bid, lid=lid[1]["id"])
        status = resp.get('data').get('subs')[1].get('status')
        check.equal(status, 'locked')
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_api_lesson_resource_get(self):
        """
         获取课程资源数据，能调通
        """
        # 手机号密码登录
        # resp0 = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone"])
        resp0 = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                 countrycode=self.gaga_app["countryCodeTw"])
        # 获取token
        authorization = resp0["data"]["auth"]
        print(authorization)
        bid = self.gaga_app["bidsaber"]
        print(bid)
        self.Authapi_lesson = ApiLesson(token=authorization)
        resp = self.Authapi_lesson.api_lesson_resource(bid=bid, cocosEnv=self.gaga_app["cocosEnv"],
                                                       lessonIds='12ade73d49813a0d8d3aedabf28c0fe6,5819a4160d2b345ebaacdba233c72ef2',
                                                       lessonVersion='2')
        print(resp)
        check.equal(resp["code"], 0)
