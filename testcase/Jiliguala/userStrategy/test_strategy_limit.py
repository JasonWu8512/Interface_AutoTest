# -*- coding: utf-8 -*-
# @Time : 2021/8/2 2:00 下午
# @Author : Cassie
# @File : test_strategy_limit.py
import pytest

from business.Jiliguala.userStrategy.ApiUserStrategy import ApiUserStrategy
from business.JlglQuery import JiglGuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


@pytest.mark.UserStrategy
class TestStrategyLimit:
    """
    用户策略配置参数校验相关用例
    """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.strategy = ApiUserStrategy()
        cls.ma_exp_mobile = cls.config['user_strategy']['ma_9.9_notpaid']  # 分流结果为思维9.9未购用户
        cls.ma_user = UserProperty(cls.ma_exp_mobile)
        cls.ma_exp_uid = cls.ma_user.user["_id"]  # 获取用户uid
        cls.ma_exp_bid = cls.ma_user.babies["_id"]  # 获取测试账号的首个宝贝id

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        JiglGuery().delete_user_strategry(self.ma_exp_bid)  # 删除数据库该bid的分流结果

    @pytest.mark.parametrize("ip", ["61.32.0.1", "1.11.23.33"])
    def test_oversea_ip(self, ip):
        """
        未拥有任意思维课程&拥有任意英语正式课程，海外ip用户不会被分配到拓科思维9.9业务线
        """
        agent = "niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)"
        # 未拥有任意思维课程&拥有任意英语正式课程，海外ip用户不会被分配到拓科思维9.9业务线
        ma_res = self.strategy.api_get_user_strategy(bid=self.ma_exp_bid, ip=ip, subject="MA",
                                                     uid=self.ma_exp_uid,
                                                     agent=agent)
        assert ma_res["data"]["subjectStrategies"][0]["contentList"][0]["contentIds"] == []

    @pytest.mark.parametrize("ip", ["113.31.145.13", "162.105.173.9"])
    def test_insea_ip(self, ip):
        """
        未拥有任意思维课程&拥有任意英语正式课程，海外ip用户会被分配到拓科思维9.9业务线
        """
        agent = "niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)"
        # 未拥有任意思维课程&拥有任意英语正式课程，海外ip用户不会被分配到拓科思维9.9业务线
        ma_res = self.strategy.api_get_user_strategy(bid=self.ma_exp_bid, ip=ip, subject="MA",
                                                     uid=self.ma_exp_uid,
                                                     agent=agent)
        assert ma_res["data"]["subjectStrategies"][0]["contentList"][0]["contentIds"] == ["l9"]

    @pytest.mark.parametrize("agent", ["niuwa/11.7.0 (iPhone; iOS 13.6.1; Scale/3.00)",
                                       "Dalvik/2.1.0 (Linux; U; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00); NiuWa : 110790; AndroidVersion : 11.7.9"])
    def test_version(self, agent):
        """策略配置版本号为>=11.8.0,android/ios分别传入不符合的版本号，不会被分配到对应的策略"""
        ma_res = self.strategy.api_get_user_strategy(bid=self.ma_exp_bid, ip="113.31.145.13", subject="MA",
                                                     uid=self.ma_exp_uid,
                                                     agent=agent)
        assert ma_res["data"]["subjectStrategies"][0]["contentList"][0]["contentIds"] == []
