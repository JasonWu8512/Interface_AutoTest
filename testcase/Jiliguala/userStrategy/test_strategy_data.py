# -*- coding: utf-8 -*-
# @Time : 2021/8/3 11:13 上午
# @Author : Cassie
# @File : test_strategy_data.py
from time import sleep

import pytest

from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder
from business.Jiliguala.userStrategy.ApiUserStrategy import ApiUserStrategy
from business.JlglQuery import JiglGuery
from business.Trade.tradeOrder.ApiRefundOpenFeign import ApiRefund
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.UserStrategy
class TestStrategyData:
    """
    用户策略配置数据校验相关用例
    """
    dm = Domains()
    order_no = None
    bid = None

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.strategy = ApiUserStrategy()
        cls.ge_normal_mobile = cls.config['user_strategy']['ge_normal_paid']  # 分流结果为英语正价课已购用户
        cls.ge_user = UserProperty(cls.ge_normal_mobile)
        cls.ge_token = cls.ge_user.basic_auth
        cls.ge_normal_uid = cls.ge_user.user["_id"]  # 获取用户uid
        cls.ge_normal_bid = cls.ge_user.babies["_id"]  # 获取测试账号的首个宝贝id
        cls.ma_normal_mobile = cls.config['user_strategy']['ma_normal_paid']  # 分流结果为思维正价课已购用户
        cls.ma_user = UserProperty(cls.ma_normal_mobile)
        cls.ma_token = cls.ma_user.basic_auth
        cls.ma_normal_uid = cls.ma_user.user["_id"]  # 获取用户uid
        cls.ma_normal_bid = cls.ma_user.babies["_id"]  # 获取测试账号的首个宝贝id

    @classmethod
    def teardown_class(cls):
        pass

    def teardown(self):
        ApiRefund().api_order_refund(orderNo=self.order_no)  # 操作退款

    def pay_normal(self, itemid, bid, token):
        """瓜豆购买课程接口"""
        res = ApiPingppOrder(token).api_order_purchase(physical=False, channel="guadou",
                                                       bid=bid,
                                                       itemid=itemid)
        return res

    def test_ma_normal(self):
        """测试思维正价课已购/未购对应策略匹配"""
        JiglGuery().delete_user_strategry(bid=self.ma_normal_bid)  # 删除数据库该bid的分流结果
        # 未拥有任意课程，思维科目不会被分配任何策略
        ma_res1 = self.strategy.api_get_user_strategy(bid=self.ma_normal_bid, ip="113.31.145.13", subject="MA",
                                                      uid=self.ma_normal_uid,
                                                      agent="niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)")
        assert ma_res1["data"]["subjectStrategies"][0]["contentList"][0]["contentIds"] == []
        assert ma_res1["data"]["subjectStrategies"][0]["subject"] == "MA"
        assert ma_res1["data"]["subjectStrategies"][0]["rootLandCode"] == None
        assert ma_res1["data"]["subjectStrategies"][0]["finalLandCode"] == None
        # 购买思维正价课
        pay = self.pay_normal(itemid="K1MA_K6MA", bid=self.ma_normal_bid, token=self.ma_token)
        self.order_no = pay["data"]["oid"]
        sleep(60)
        # 拥有任意思维正式课程，用户被分配到策略：正式课思维-已购
        ma_res2 = self.strategy.api_get_user_strategy(bid=self.ma_normal_bid, ip="113.31.145.13", subject="MA",
                                                      uid=self.ma_normal_uid,
                                                      agent="niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)")
        assert ma_res2["data"]["subjectStrategies"][0]["contentList"][0]["contentIds"] == ["l10"]
        assert ma_res2["data"]["subjectStrategies"][0]["subject"] == "MA"
        assert ma_res2["data"]["subjectStrategies"][0]["rootLandCode"] == "10006"
        assert ma_res2["data"]["subjectStrategies"][0]["finalLandCode"] == "20010"

    def test_ge_normal(self):
        """测试英语正价课已购/未购对应策略匹配"""
        JiglGuery().delete_user_strategry(self.ge_normal_bid)  # 删除数据库该bid的分流结果
        # 未拥有任意课程,有手机号用户,年龄为2-3岁，用户被分配到策略：英语9.9-未购
        ge_res1 = self.strategy.api_get_user_strategy(bid=self.ge_normal_bid, ip="113.31.145.13", subject="GE",
                                                      uid=self.ge_normal_uid,
                                                      agent="niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)")
        assert ge_res1["data"]["subjectStrategies"][0]["contentList"][0]["contentIds"] == ["l3"]
        assert ge_res1["data"]["subjectStrategies"][0]["subject"] == "GE"
        assert ge_res1["data"]["subjectStrategies"][0]["rootLandCode"] == "10002"
        assert ge_res1["data"]["subjectStrategies"][0]["finalLandCode"] == "20003"
        # 购买英语正价课
        pay = self.pay_normal(itemid="S1GE", bid=self.ge_normal_bid, token=self.ge_token)
        order_no = pay["data"]["oid"]
        sleep(60)
        # 拥有任意英语正式课程，用户被分配到策略：正式课英语-已购
        ge_res2 = self.strategy.api_get_user_strategy(bid=self.ge_normal_bid, ip="113.31.145.13", subject="GE",
                                                      uid=self.ge_normal_uid,
                                                      agent="niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)")
        assert ge_res2["data"]["subjectStrategies"][0]["contentList"][0]["contentIds"] == ["l6"]
        assert ge_res2["data"]["subjectStrategies"][0]["subject"] == "GE"
        assert ge_res2["data"]["subjectStrategies"][0]["rootLandCode"] == "10004"
        assert ge_res2["data"]["subjectStrategies"][0]["finalLandCode"] == "20006"
