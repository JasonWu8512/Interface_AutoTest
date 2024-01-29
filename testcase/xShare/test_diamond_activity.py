# coding=utf-8
# @Time    : 2021/4/5 11:07 上午
# @Author  : qilijun
# @File    : test_diamond_activity.py

from business.common.UserProperty import UserProperty
from business.xshare.ApiDiamond import ApiDiamond
from business.xshare.ApiManagementSystem import ApiManagementSystem
from config.env.domains import Domains


class TestDiamondActivity(object):
    """
    钻上商城活动接口用例
    """

    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path("fat")

        # 初始化不同身份用户
        cls.gmkEnglish_user = UserProperty(cls.config["xshare"]["gmkEnglish_user"])  # 构建英语正价课用户user实例
        cls.gmkMath_user = UserProperty(cls.config["xshare"]["gmkMath_user"])  # 构建思维正价课用户user实例
        cls.promoter_user = UserProperty(cls.config["xshare"]["promoter_user"])  # 构建推广人用户user实例
        cls.refunded_user = UserProperty(cls.config["xshare"]["refunded_user"])  # 构建正价课退款用户user实例
        cls.new_user = UserProperty(cls.config["xshare"]["new_user"])  # 构建未购课用户user实例

        # 实例不同身份对象
        cls.gmkEnglish = ApiDiamond(auth_token=cls.gmkEnglish_user.basic_auth)
        cls.gmkMath = ApiDiamond(auth_token=cls.gmkMath_user.basic_auth)
        cls.promoter = ApiDiamond(auth_token=cls.promoter_user.basic_auth)
        cls.refunded = ApiDiamond(auth_token=cls.refunded_user.basic_auth)
        cls.new = ApiDiamond(auth_token=cls.new_user.basic_auth)
        cls.no_auth = ApiDiamond()

        # 获取用户ID，验证充值钻石接口用例
        cls.user_id = cls.gmkEnglish_user.user_id
        cls.user_id2 = cls.refunded_user.user_id
        cls.user_id3 = cls.new_user.user_id

        cls.uidList = [cls.user_id, cls.user_id2, cls.user_id3]

        cls.no_auth_account = ApiManagementSystem()
        cls.auth_token = cls.no_auth_account.api_get_auth(
            cls.config["xshare"]["manage"]["user"], cls.config["xshare"]["manage"]["password"]
        )
        cls.with_auth_account = ApiManagementSystem(auth_token=cls.auth_token)

    def test_check_gmkEnglish_user(self):
        """
        英语正价课非推广人账号，正常生成海报
        """
        check_resp = self.gmkEnglish.api_get_sharePosterCheck()
        assert check_resp["code"] == 0
        assert check_resp["data"]["valid"] == True
        assert check_resp["status_code"] == 200

    def test_check_gmkMath_user(self):
        """
        思维正价课非推广人账号，正常生成海报
        """
        check_resp = self.gmkMath.api_get_sharePosterCheck()
        assert check_resp["code"] == 0
        assert check_resp["status_code"] == 200
        assert check_resp["data"]["valid"] == True

    def test_check_promoter_user(self):
        """
        推广人账号，正常生成海报
        """
        check_resp = self.promoter.api_get_sharePosterCheck()
        assert check_resp["code"] == 0
        assert check_resp["status_code"] == 200
        assert check_resp["data"]["valid"] == True

    def test_check_refunded_user(self):
        """
        正价课退款且非推广人账号，不能正常生成海报
        """
        check_resp = self.refunded.api_get_sharePosterCheck()
        assert check_resp["code"] == 47000
        assert check_resp["status_code"] == 401

    def test_check_new_user(self):
        """
        非正价课&非推广人用户，不能正常生成海报
        """
        check_resp = self.new.api_get_sharePosterCheck()
        assert check_resp["code"] == 47000
        assert check_resp["status_code"] == 401

    def test_check_unlogin_user(self):
        """
        未登录状态不能正常生成海报
        """
        check_resp = self.no_auth.api_get_sharePosterCheck()
        assert check_resp["code"] == 103
        assert check_resp["status_code"] == 401
        assert check_resp["msg"] == "认证失败，请退出重新登录"

    def test_check_unlogin_diamond_batch(self):
        """
        未登录状态不能充值
        """
        check_resp = self.no_auth_account.api_diamond_batch(100, "自动化测试", [self.user_id])
        assert check_resp["status_code"] == 401
        assert check_resp["message"] == "Token 缺失"

    def test_check_diamod_batch_one(self):
        """
        单用户充值
        """
        # 查询用户当前钻石数
        before_batch = self.with_auth_account.api_get_user_diamond(self.user_id)
        before_point = before_batch["data"]["point"]
        before_point_total = before_batch["data"]["total"]
        check_resp = self.with_auth_account.api_diamond_batch(100, "自动化测试", [self.user_id])
        assert check_resp["status_code"] == 200
        # 查询用户充值后钻石数
        after_query = self.with_auth_account.api_get_user_diamond(self.user_id)
        after_point = after_query["data"]["point"]
        after_point_total = after_query["data"]["total"]
        # 校验充值前后钻石数差值是否等于充值数量
        assert after_point - before_point == 100
        assert after_point_total - before_point_total == 100

    def test_check_diamod_batch_many(self):
        """
        批量用户充值
        """
        # 查询用户当前钻石数
        before_point_list = []
        before_point_total_list = []
        after_point_list = []
        after_point_total_list = []
        for user_id in self.uidList:
            before_batch = self.with_auth_account.api_get_user_diamond(user_id)
            if "data" not in before_batch.keys():
                before_point_list.append(0)
                before_point_total_list.append(0)
            else:
                before_point_list.append(int(before_batch["data"]["point"]))
                before_point_total_list.append(int(before_batch["data"]["total"]))
        check_resp = self.with_auth_account.api_diamond_batch(100, "自动化测试", self.uidList)
        assert check_resp["status_code"] == 200
        for user_id in self.uidList:
            after_query = self.with_auth_account.api_get_user_diamond(user_id)
            after_point_list.append(int(after_query["data"]["point"]))
            after_point_total_list.append(int(after_query["data"]["total"]))
        for i in range(len(self.uidList)):
            assert after_point_list[i] - before_point_list[i] == 100
            assert after_point_total_list[i] - before_point_total_list[i] == 100
