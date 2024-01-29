# -*- coding: utf-8 -*-
# @Time : 2021/6/8 5:32 下午
# @Author : Cassie
# @File : test_check_order.py
import logging

import pytest

from business.Jiliguala.activity.ApiCheck import ApiCheck
from business.Jiliguala.lesson.ApiSuper import ApiSuper
from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder
from business.businessQuery import lessonQuery
from business.checkCase import checkcase
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.format.format import get_datetime


@pytest.mark.Activity
class TestCheckOrder:
    """
    老呱美1.5课程打卡订单相关用例
    """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.check_order_user = cls.config['activity']['check_order_user']  # 配置文件读取测试账号
        cls.user = UserProperty(cls.check_order_user)
        cls.token = cls.user.basic_auth
        cls.bid = cls.user.babies["_id"]  # 获取用户首个宝贝id
        cls.uid = cls.user.user["_id"]  # 获取用户uid
        cls.version = cls.config['version']['ver11.6']
        cls.agent = cls.config['agent']['ios_11.6']
        cls.check = ApiCheck(cls.token, cls.version, cls.agent)
        cls.pay = ApiPingppOrder(cls.token)
        cls.lesson = ApiSuper(cls.token, cls.agent)
        cls.order = ApiPingppOrder(cls.token)

    def setup(self):
        case = checkcase.getCase(task="i2", days=16)
        lessonQuery().delete_check_record(self.uid)
        lessonQuery().update_check_record(self.uid, case)
        print("SET case, Task: {}, days: {}".format("i2", 16))

    @classmethod
    def teardown_class(cls):
        pass

    def get_check_order(self):
        """获取用户的打卡订单id"""
        id = "i2"
        check_progress = self.check.api_get_meta(self.bid)
        oid = check_progress["data"][id]["oid"]
        print("订单id为: %s" % oid)
        return oid

    def update_success_time(self, day, hour, aid):
        """修改打卡活动记录的挑战成功时间"""
        time = get_datetime(day=day, hour=hour)
        check = lessonQuery().update_check_record(self.uid,
                                                  {f'{aid}.chSuccessInfo.successTime': time})
        print(check)

    def test_chek_order_address(self):
        """打卡订单提交校验收货地址"""
        # 查询订单详情接口，获取商品信息
        oid = self.get_check_order()
        ttl = self.order.api_get_realobject(oid=oid)["data"]["item"]["ttl"]
        # 未填写收货地址,无法提交给出提示
        res_fail = self.order.api_check_order(oid=oid, comment="", ttl=ttl)
        assert res_fail["code"] == 181
        assert res_fail["msg"] == "请先完善收货信息"
        # 用户填写收货地址后，可以正常提交订单
        self.order.api_check_address(region="天津市 天津市 和平区", addr="自动化测试", oid=oid,
                                     tel="11111111111", name='测试')  # 填写收货地址
        res_suc = self.order.api_check_order(oid=oid, comment="", ttl=ttl)  # 提交订单
        assert res_suc["code"] == 0
        assert res_suc["data"] == "success"

    @pytest.mark.parametrize("day_reduce,day_increase", [(-91, -30), (-180, -89)])
    def test_chek_order_time(self, day_reduce, day_increase):
        """打卡订单提交校验挑战成功时间"""
        # 查询订单详情接口，获取商品信息
        oid = self.get_check_order()
        ttl = self.order.api_get_realobject(oid=oid)["data"]["item"]["ttl"]
        self.order.api_check_address(region="天津市 天津市 和平区", addr="自动化测试", oid=oid,
                                     tel="11111111111", name='测试')  # 填写收货地址
        # 挑战成功时间设置为3个月前，无法提交订单
        self.update_success_time(day=day_reduce, hour=0, aid="i2")
        res_fail = self.order.api_check_order(oid=oid, comment="", ttl=ttl)
        assert res_fail["code"] == 393
        assert res_fail["msg"] == "已超过领取时限，不能领取"

        # 挑战成功时间设置为小于3个月,可以正常提交订单
        self.update_success_time(day=day_increase, hour=0, aid="i2")
        res_suc = self.order.api_check_order(oid=oid, comment="", ttl=ttl)
        assert res_suc["code"] == 0
        assert res_suc["data"] == "success"

    def test_chek_order_repeat(self):
        """打卡订单提交校验重复提交"""
        # 查询订单详情接口，获取商品信息
        oid = self.get_check_order()
        ttl = self.order.api_get_realobject(oid=oid)["data"]["item"]["ttl"]
        # 用户填写收货地址，首次提交订单
        self.order.api_check_address(region="天津市 天津市 和平区", addr="自动化测试", oid=oid,
                                     tel="11111111111", name='测试')  # 填写收货地址
        res_suc = self.order.api_check_order(oid=oid, comment="", ttl=ttl)  # 提交订单
        assert res_suc["code"] == 0
        assert res_suc["data"] == "success"
        # 已提交的订单，再次进行提交
        res_fail = self.order.api_check_order(oid=oid, comment="", ttl=ttl)  # 提交订单
        assert res_fail["code"] == 500
        assert res_fail["msg"] == "重复提交"
