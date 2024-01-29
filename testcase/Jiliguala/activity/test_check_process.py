# -*- coding: utf-8 -*-
# @Time : 2021/6/10 5:19 下午
# @Author : Cassie
# @File : test_check_process.py
import pytest

from business.Jiliguala.activity.ApiCheck import ApiCheck
from business.Jiliguala.lesson.ApiSuper import ApiSuper
from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder
from business.businessQuery import lessonQuery
from business.checkCase import checkcase
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.Activity
class TestCheckProcess:
    """
    老呱美1.5课程进行完课，打卡进度相关用例
    """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.check_lesson_user = cls.config['activity']['check_lesson_user']  # 配置文件读取测试账号
        cls.user = UserProperty(cls.check_lesson_user)
        cls.token = cls.user.basic_auth
        cls.bid = cls.user.babies["_id"]  # 获取测试账号的首个宝贝id
        cls.uid = cls.user.user["_id"]  # 获取用户uid
        cls.version = cls.config['version']['ver11.6']
        cls.agent = cls.config['agent']['ios_11.6']
        cls.check = ApiCheck(cls.token, cls.version, cls.agent)
        cls.pay = ApiPingppOrder(cls.token)
        cls.lesson = ApiSuper(cls.token, cls.agent)
        cls.order = ApiPingppOrder(cls.token)

    @pytest.fixture()
    def reset_check_record(self):
        case = checkcase.getCase(task="i1", days=7)
        lessonQuery().delete_check_record(self.uid)
        lessonQuery().update_check_record(self.uid, case)
        print("SET case, Task: {}, days: {}".format("i1", 7))

    @classmethod
    def teardown_class(cls):
        pass

    def complete_lesson(self):
        """呱美1.5课程，用户进行完课"""
        res = None
        lessonid = "L0XX026"
        units = []
        lesson_detail = self.lesson.api_get_lesson_detail(bid=self.bid, lesson_click=1, popup="true", lid=lessonid)
        sublist = lesson_detail["data"]["subs"]
        for i in range(0, len(sublist)):
            sublessonid = sublist[i]["_id"]
            print("子课程id为：", sublessonid)
            res = self.lesson.api_lesson_progress(bid=self.bid, lessonid=lessonid, sublessonid=sublessonid, units=units)
            print(res)
        return res

    def test_check_status(self, reset_check_record):
        """老呱美课程完课接口lessonprogress，返回的参与打卡状态checked字段校验"""
        # 用户当天首次完课，校验参与打卡状态为成功
        assert self.complete_lesson()["data"]["checked"] == True
        # 用户当天首次完课，校验参与打卡状态为失败
        assert self.complete_lesson()["data"]["checked"] == False

    def test_api_get_config(self):
        """查询打卡活动配置"""
        res = self.check.api_get_config()
        print(res)
        assert res["code"] == 0

    def test_api_get_meta(self):
        """查询用户的打卡进度"""
        res = self.check.api_get_meta(self.bid)
        print(res)
        assert res["code"] == 0
