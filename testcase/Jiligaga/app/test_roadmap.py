# -*- coding: utf-8 -*-
# @Time : 2022/7/21 下午5:00
# @Author : Saber &lisa &wenling_xu
# @File : test_roadmap.py
import os

import pytest
import time
import pytest_check as check
from business.Jiligaga.app.ApiAccount import ApiAccount
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3
from business.Jiligaga.app.ApiLogin import Login
from business.Jiligaga.app.ApiRoadmapExperienceLessonTake import ApiRoadmapExperienceLessonTake
from business.Jiligaga.app.ApiRoadmapQuery import ApiRoadmapQuery
from config.env.domains import Domains
from business.Jiligaga.app.ApiUsertest import ApiMarktestaccount
from business.Jiligaga.app.ApiCompleteCourse import ApiCompleteCourse
from business.Eduplatform.ApiEduplatform_hw.ApiRoadmapStudy import ApiRoadmapStudy
from business.Jiligaga.app.ApiLessonDetail import ApiLesson
from business.Jiligaga.app.ApiAddStudentFriend import ApiAddStudentFriend
from business.mysqlQuery import HwQuery
from business.sso.ApiSso import ApiSso
from business.Crm.ApiAccount.ApiUser import ApiUser
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Jiligaga.app.ApiRedeem import ApiRedeem
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth
from business.Jiligaga.app.ApiSkip import ApiSkip


@pytest.mark.GagaReg
class TestApiRoadmapQuery(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('fat')
        # 获取配置文件的手机号
        cls.gaga_app = cls.dm.set_env_path('fat')["gaga_app"]
        print(cls.gaga_app)
        cls.sso = cls.dm.set_env_path('fat')["sso"]
        print(cls.sso)
        cls.apiaddstudentfriend = ApiAddStudentFriend()
        cls.login = Login()
        cls.apiAccountV3 = ApiAccountV3()
        cls.apiAccount = ApiAccount()
        cls.apiroadmapstudy = ApiRoadmapStudy()
        cls.apiuser = ApiUser()
        cls.hwquery = HwQuery()
        cls.apisso = ApiSso(email_address=None, pwd=None)
        cls.apiroadmapexperiencelessontake = ApiRoadmapExperienceLessonTake()
        cls.user = UserProperty(email_address=cls.sso["email"], pwd=cls.sso["pw"])
        cls.apiaddstudentfriend = ApiAddStudentFriend(cls.user.cookies)
        cls.source = cls.config['gaga_app']['source01']

    def test_roadmap_completed(self):
        """
        已拥有level1，校验
        level1 lesson1 completed
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
        apiadminauth = ApiAdminAuth()
        a_token = apiadminauth.api_login(username=self.sso["email"], password=self.sso["pw"])["data"][
            "token"]
        # 获取兑换码
        self.apiredeem = ApiRedeem(token=a_token)
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
        # 第一节课程完成
        uid = resp1["data"]["user"]["userNo"]
        lid = resp["data"]["roadmap"]["elements"][0]["lessons"][0]["id"]
        Domains.set_domain(self.config['hw_eduplatform_url'])
        apilesson = ApiLesson(token=authorization)
        nodeId = apilesson.api_lesson_detail_v2(bid=bid, lid=lid)
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][0]["_id"],
                                                  score="90")
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][1]["_id"],
                                                  score="90")
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][2]["_id"],
                                                  score="90")
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][3]["_id"],
                                                  score="90")
        # 获取该bid下路线图的数据
        self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.29.0")
        resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
        # 获取level1 lesson2状态
        status = resp.get('data').get('roadmap').get('elements')[0].get('lessons')[0].get('status')
        # 校验一下是否是已完成
        check.equal(status, 'completed')
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        """注销-人转已领取过体验课的用户"""
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_roadmap_skipped(self):
        """
        已拥有level1，校验
        level1 lesson2 skipped
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
        apiadminauth = ApiAdminAuth()
        a_token = apiadminauth.api_login(username=self.sso["email"], password=self.sso["pw"])["data"][
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
        lid = resp["data"]["roadmap"]["elements"][0]["lessons"]
        apiskip = ApiSkip(authorization)
        apiskip.skip(lid=lid[0]["id"], bid=bid)
        # 获取该bid下路线图的数据
        self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.29.0")
        resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
        print(resp)
        # 获取level1 lesson2状态
        status01 = resp.get('data').get('roadmap').get('elements')[0].get('lessons')[0].get('status')
        print(status01)
        # 校验一下是否是跳课
        check.equal(status01, 'skipped')
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        """注销-人转已领取过体验课的用户"""
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_roadmap_absent_current(self):
        """
        已拥有level1，校验
        level1 lesson3 当前课 状态absent
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
        apiadminauth = ApiAdminAuth()
        a_token = apiadminauth.api_login(username=self.sso["email"], password=self.sso["pw"])["data"][
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
        lid = resp["data"]["roadmap"]["elements"][0]["lessons"]
        apiskip = ApiSkip(authorization)
        apiskip.skip(lid=lid[0]["id"], bid=bid)
        apiskip.skip(lid=lid[1]["id"], bid=bid)
        # 获取该bid下路线图的数据
        self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.29.0")
        resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
        # 获取level1 lesson3状态
        status02 = resp.get('data').get('roadmap').get('elements')[0].get('lessons')[2].get('status')
        current = resp.get('data').get('roadmap').get('elements')[0].get('lessons')[2].get('current')
        print(status02, current)
        # 校验一下当前课
        check.equal(status02, 'absent')
        check.equal(current, True)
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        """注销-人转已领取过体验课的用户"""
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_roadmap_locked(self):
        """
        已拥有level1，校验
        level1 lesson4 当前课 状态locked未上到
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
        # 获取该bid下路线图的数据
        self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.29.0")
        resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
        print(resp)
        # 获取level1 lesson4状态
        status03 = resp.get('data').get('roadmap').get('elements')[2].get('lessons')[3].get('status')
        current = resp.get('data').get('roadmap').get('elements')[2].get('lessons')[3].get('current')
        print(status03, current)
        # 校验一下当前课
        check.equal(status03, 'locked')
        check.equal(current, False)

    # def test_roadmap_first_purchase_banner(self):
    #     """
    #     机转账户未购买课程，校验首购banner
    #     """
    #     # 手机号密码登录
    #     # resp0 = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone03"])
    #     resp0 = self.apiAccountV3.login_password(phone=self.gaga_app["phone03"], pwd=self.gaga_app["pwd"],
    #                                              countrycode=self.gaga_app["countryCodeTw"])
    #     # 获取token
    #     authorization = resp0["data"]["auth"]
    #     print(authorization)
    #     bid = self.gaga_app["bidsaber"]
    #     print(bid)
    #     # 获取该bid下路线图的数据
    #     self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.18.0")
    #     resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
    #     print(resp)
    #     # 获取banner id
    #     banner_id = resp.get('data').get('roadmap').get('elements')[1].get('id')
    #     print(banner_id)
    #     # 校验一下banner id 是否为首购
    #     check.equal(banner_id, 'first_purchase_level1')

    # def test_roadmap_second_purchase_banner(self):
    #     """
    #     机转账户购买过小课包，校验复购banner，已经没有此场景
    #     """
    #     # 手机号密码登录
    #     # resp0 = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone04"])
    #     resp0 = self.apiAccountV3.login_password(phone=self.gaga_app["phone04"], pwd=self.gaga_app["pwd"],
    #                                              countrycode=self.gaga_app["countryCodeTw"])
    #     # 获取token
    #     authorization = resp0["data"]["auth"]
    #     print(authorization)
    #     bid = self.gaga_app["bidsaber"]
    #     print(bid)
    #     self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.18.0")
    #     resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
    #     print(resp)
    #     # 获取banner id
    #     banner_id = resp.get('data').get('roadmap').get('elements')[5].get('id')
    #     print(banner_id)
    #     # 校验一下banner id 是否为复购
    #     check.equal(banner_id, '4uint_purchase_level1_unit5')

    def test_roadmap_new_salesman(self):
        """
        人转账户未领取0元课
        """
        # 手机号密码登录
        # resp0 = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone05"])
        resp0 = self.apiAccountV3.login_password(phone=self.gaga_app["phone05"], pwd=self.gaga_app["pwd"],
                                                 countrycode=self.gaga_app["countryCodeTw"])

        # 获取token
        authorization = resp0["data"]["auth"]
        print(authorization)
        bid = resp0["data"]["user"]["babyList"][0]["bid"]
        print(bid)
        self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.29.0")
        resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
        print(resp)
        # 获取体验营状态
        status = resp.get('data').get('roadmap').get('elements')[0].get('id')
        print(status)
        # 校验一下体验营状态
        check.equal(status, 'experience_level1')

    def test_roadmap_salesman_haveTraillesson(self):
        """
        人转账户已领取0元课
        """
        # 手机号密码登录
        # resp0 = self.login.phone_pwd_login(pwd=self.gaga_app["pwd"], phone=self.gaga_app["phone06"])
        resp0 = self.apiAccountV3.login_password(phone=self.gaga_app["phone06"], pwd=self.gaga_app["pwd"],
                                                 countrycode=self.gaga_app["countryCodeTw"])
        # 获取token
        authorization = resp0["data"]["auth"]
        print(authorization)
        bid = resp0["data"]["user"]["babyList"][0]["bid"]
        print(bid)
        self.AuthApiRoadmapQuery = ApiRoadmapQuery(token=authorization, appversion="1.29.0")
        resp = self.AuthApiRoadmapQuery.api_roadmap_query(bid=bid)
        print(resp)
        # 获取体验营状态
        status = resp.get('data').get('roadmap').get('elements')[0].get('status')
        print(status)
        # 校验一下体验营状态
        check.equal(status, 'paid')

    def test_roadmap_experience_lesson_take_source01(self):
        """人转--满足领取条件，领取体验课
        领取体验课入口：
        路线图运营位入口领取
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone08"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone08"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone08"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        authorization = resp1["data"]["auth"]
        self.apiroadmapexperiencelessontake = ApiRoadmapExperienceLessonTake(token=authorization)
        # 路线图按钮入口领取
        resp = self.apiroadmapexperiencelessontake.api_roadmap_experience_lessontake(source=self.gaga_app["source01"])
        check.equal(resp["code"], 0)
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        self.apiAccountV3.close_user()




    def test_roadmap_experience_lesson_take(self):
        """人转--满足领取条件，领取体验课
        领取体验课入口：
        路线图按钮入口领取
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone08"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone08"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone08"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        authorization = resp1["data"]["auth"]
        self.apiroadmapexperiencelessontake = ApiRoadmapExperienceLessonTake(token=authorization)
        # 路线图按钮入口领取
        resp = self.apiroadmapexperiencelessontake.api_roadmap_experience_lessontake(source=self.gaga_app["source02"])
        check.equal(resp["code"], 0)
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        self.apiAccountV3.close_user()


    def test_roadmap_experience_lesson_take(self):
        """人转--满足领取条件，领取体验课
        领取体验课入口：
        路线图弹窗领取
        """
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone08"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone08"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone08"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        authorization = resp1["data"]["auth"]
        self.apiroadmapexperiencelessontake = ApiRoadmapExperienceLessonTake(token=authorization)
        # 路线图弹窗领取
        resp = self.apiroadmapexperiencelessontake.api_roadmap_experience_lessontake(source=self.gaga_app["source03"])
        check.equal(resp["code"], 0)
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        self.apiAccountV3.close_user()


    def test_roadmap_experience_lesson_repeattake(self):
        """人转--已参加过活动的用户-活动参与次数达到上限"""
        # 获取手机号验证码
        self.apiAccountV3.login_send_code(account=self.gaga_app["phone08"],
                                          countrycode=self.gaga_app["countryCodeTw"])
        # return验证码
        code = self.apiAccount.return_phone_code(phone=self.gaga_app["phone08"], country=self.gaga_app["countrytw"])
        # 验证码登录
        resp1 = self.apiAccountV3.login_validate_code(account=self.gaga_app["phone08"], code=code,
                                                      countrycode=self.gaga_app["countryCodeTw"])
        authorization = resp1["data"]["auth"]
        print(authorization)
        self.apiroadmapexperiencelessontake = ApiRoadmapExperienceLessonTake(token=authorization)
        self.apiroadmapexperiencelessontake.api_roadmap_experience_lessontake(source=self.gaga_app["source02"])
        resp = self.apiroadmapexperiencelessontake.api_roadmap_experience_lessontake(source=self.gaga_app["source02"])
        check.equal(resp["code"], 50401)
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        """注销-人转已领取过体验课的用户"""
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_complete_course(self):
        """
        人转--账号新登录
        人转--满足领取条件，领取体验课
        标注测试账号
        执行开课接口
        获取当前bid
        校验第一节体验营的状态absent
        完成第一节体验营的课程
        校验第一节体验营的状态comleted
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
        # 校验第一节体验营的状态absent
        bid = resp1["data"]["user"]["babyList"][0]["bid"]
        apiroadmapquery = ApiRoadmapQuery(token=authorization, appversion='1.30.0')
        resp = apiroadmapquery.api_roadmap_query(bid=bid)
        absent = resp['data']['roadmap']['elements'][1]['lessons'][0]['status']
        # 完成第一节体验营的课程
        lid = resp["data"]["roadmap"]["elements"][1]["lessons"][0]["id"]
        Domains.set_domain(self.config['hw_eduplatform_url'])
        apilesson = ApiLesson(token=authorization)
        nodeId = apilesson.api_lesson_detail_v2(bid=bid, lid=lid)
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][0]["_id"],
                                                  score="90")
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][1]["_id"],
                                                  score="90")
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][2]["_id"],
                                                  score="90")
        self.apiroadmapstudy.api_leafNodeComplete(bid=bid, uid=uid, finishTime="1662795332000",
                                                  nodeId=nodeId["data"]["subs"][3]["_id"],
                                                  score="90")
        resp = apiroadmapquery.api_roadmap_query(bid=bid)
        completed = resp['data']['roadmap']['elements'][1]['lessons'][0]['status']
        check.equal(absent, "absent")
        check.equal(completed, "completed")
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)

    def test_add_student_friend(self):
        """
        1.校验没有加好友之前的添加状态：未添加
        2.执行crm加好友接口
        3.校验添加好友之后的添加状态：已添加
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
        # 校验没有加好友前的状态
        uid = resp1["data"]["user"]["userNo"]
        # 查询数据库
        query_leads_assign = self.hwquery.uid_query_leads_assign(uid=uid)
        print(query_leads_assign)
        # frequency=0
        # while True:
        #     # 执行查询语句
        #     frequency= frequency+1
        #     query_leads_assign = self.hwquery.uid_query_leads_assign(uid=uid)
        #     print(query_leads_assign)
        #     if frequency==5:
        #         print(frequency)
        #         break
        #     elif query_leads_assign:
        #         query_leads_assign = query_leads_assign[0]["bind_status"]
        #         print(query_leads_assign)
        #         break
        #     else:
        #         query_leads_assign = self.hwquery.uid_query_leads_assign(uid=uid)
        #         print(query_leads_assign)
        #         print("00000000")
        # 添加班主任好友
        termid = query_leads_assign["term_id"]
        print(termid)
        tid = query_leads_assign["salesman_id"]
        no_bind_status = query_leads_assign["bind_status"]
        print(no_bind_status)
        self.apiaddstudentfriend.add_student_friend(termId=termid, tid=tid, userId=uid)
        # 校验加好友前的状态
        bind_status = self.hwquery.uid_query_leads_assign(uid=uid)["bind_status"]
        print(bind_status)
        check.equal(no_bind_status, 0)
        check.equal(bind_status, 1)
        """注销-人转已领取过体验课的用户"""
        self.apiAccountV3 = ApiAccountV3(token=authorization)
        resp = self.apiAccountV3.close_user()
        check.equal(resp["code"], 0)
