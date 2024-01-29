# coding=utf-8
# @Time    : 2021/4/12
# @Author  : qilijun
# @File    : test_order_refund.py

import time

from business.businessQuery import lessonQuery, pingxxorderQuery, usersQuery, xshareQuery
from business.common.UserProperty import UserProperty
from business.mars.ApiOrder import ApiOrder
from business.mars.ApiPurchasepage import ApiPurchasepage
from business.Jiliguala.user.ApiUserInfo import ApiUserInfo
from business.xshare.ApiIncome import ApiIncome
from config.env.domains import Domains
from utils.format.format import now_timeStr

class Test_order_refund(object):
    """
    体验课订单返现接口用例
    """

    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path(env="fat")
        # 设置域名
        cls.dm.set_domain(cls.config["url"])
        # 获取测试手机号
        cls.mobile = cls.config["xshare"]["tc_user"]

        # 初始化不同身份用户
        cls.tcRedeem_user = UserProperty(cls.config["xshare"]["tcRedeem_user"])  # 构建兑换码用户user实例
        cls.tcGuadou_user = UserProperty(cls.config["xshare"]["tcGuadou_user"])  # 构建呱豆支付用户user实例
        cls.sp2xuId_math = cls.config["xshare"]["sp2xuId"]["sp2xuId_math"]  # 呱呱思维趣味AI互动课K1
        cls.sp2xuId_lianbao = cls.config["xshare"]["sp2xuId"]["sp2xuId_lianbao"]  # 英语+思维体验课
        cls.sp2xuId_english = cls.config["xshare"]["sp2xuId"]["sp2xuId_english"]  # 呱呱思维趣味AI互动课K1

        cls.new_user = ApiUserInfo()

        # 构建数据库查询实例
        cls.refund_query = xshareQuery()
        cls.order_query = pingxxorderQuery()
        cls.db_users = usersQuery()
        cls.db_lesson = lessonQuery()

        # 获取不同用户user_id
        cls.tcRedeem_user_id = cls.tcRedeem_user.user_id
        cls.tcRedeem_auth = cls.tcRedeem_user.basic_auth
        cls.tcGuadou_user_id = cls.tcGuadou_user.user_id
        cls.tcGuadou_auth = cls.tcGuadou_user.basic_auth

        # 构建返现类实例
        cls.refund_redeem = ApiIncome(authtoken=cls.tcRedeem_auth)
        cls.refund_guado = ApiIncome(authtoken=cls.tcGuadou_auth)

        cls.redeem_itemid_list = ["H5_Sample_Kbei", "H5_Sample_tmall", "H5_Sample_Pdd", "H5_Sample_Jd"]
        cls.channel_itemid_list = [
            "H5_Sample_OutsideH5",
            "H5_Sample_promoter",
            "H5_Sample_DiamondActivity",
            "H5_Sample_DiamondActivity",
            "H5_Sample_Pintuan",
            "H5_XX_Sample_XCX",
            "H5_XX_Sample",
            "H5_Cashback",
        ]
        cls.order_status_list = ["needaddress", "paid"]

    def register_user(self):
        """
        注册新用户并获取用户相关信息
        """
        if self.db_users.get_users(mobile=self.mobile) is not None:
            # 注销用户
            self.logout_user(mobile=self.mobile)

        # 注册新用户
        self.new_user.api_get_websms(mobile=self.mobile)

        # 获取用户token/用户ID/用户guaid
        self.user_prop = UserProperty(self.mobile)
        self.new_user_token = self.user_prop.basic_auth
        self.new_user_id = self.user_prop.user_id

        # 实例化对象
        self.page = ApiPurchasepage(basic_auth=self.new_user_token)
        # 实例化订单类
        self.ord = ApiOrder(basic_auth=self.new_user_token)
        # 构建返现类实例
        self.refund = ApiIncome(authtoken=self.new_user_token)

    def logout_user(self, mobile):
        """
        注销用户
        :param mobile: 注销手机号
        :return:
        """
        new_user_token = UserProperty(mobile=mobile).basic_auth
        logout_user = ApiUserInfo(token=new_user_token)
        logout_user.api_sms_logout()
        smsCode = usersQuery().get_users(mobile=mobile)["sms"]["code"]
        logout_user.api_users_security_info(mobile=mobile, smsCode=smsCode)

    def buy_tc_lesson(
        self,
        sp2xuIds,
        nonce=now_timeStr(),
        item_id="H5_XX_Sample",
        source="autoTest",
        xshare_initiator=None,
        sharer=None,
        channel="wx_wap",
        result_url="https://devt.jiliguala.com/test",
    ):
        """浏览器环境调起微信支付购买体验课"""
        # 调用后端创建订单接口
        order_res = self.ord.api_create_v2(
            item_id=item_id,
            nonce=nonce,
            source=source,
            xshare_initiator=xshare_initiator,
            sharer=sharer,
            sp2xuIds=sp2xuIds,
        )
        print(order_res)
        # 创单接口是否正常
        assert order_res["code"] == 0 and order_res["status_code"] == 200
        # 调用后端支付接口
        charge_res = self.ord.api_charge_v2(oid=order_res["data"]["orderNo"], channel=channel, result_url=result_url)
        time.sleep(5)
        assert charge_res["code"] == 0 and charge_res["status_code"] == 200
        return charge_res

    def get_user_basic_data(self, user_id):
        """
        获取用户返现前金额数据
        """
        # 查询未返现前用户金额
        query_before = self.refund_query.select_xshare_record(user_id)
        if query_before is None:
            self.all_before = 0
            self.available_before = 0
        else:
            # 更新数据库为未返现状态
            self.refund_query.update_xshare_record(user_id=user_id)
            self.all_before = query_before["cashback"]["all"]
            self.available_before = self.all_before - query_before["cashback"]["checkouted"]

    def update_cashback_data(self, user_id, course):
        """
        插入用户思维体验课完课返现数据
        :param user_id: 用户ID
        :return:
        """
        # 查询用户完课数据
        query_before = self.refund_query.select_user_flags(user_id)
        # 如果不存在完课记录
        if query_before is None:
            if course == "math":
                # 插入思维完课记录
                self.refund_query.insert_user_flags({"_id": user_id, "cashback_tc": {"K1MA": {"K1MAE01": 5}}})
            elif course == "english":
                # 插入英语完课记录
                self.refund_query.insert_user_flags({"_id": user_id, "cashback_tc": {"K1GE": {"K1GEE03": 5}}})
            elif course == "lianBao":
                # 插入联报完课记录
                self.refund_query.insert_user_flags(
                    {"_id": user_id, "cashback_tc": {"K1GE": {"K1GEE03": 5}, "K1MA": {"K1MAE01": 5}}}
                )
        # 更新完课记录
        # FIXME：APP完课接口未封装，暂时写死插入K1英语/思维/联报完课数据
        else:
            if course == "math":
                self.refund_query.update_user_flags(user_id=user_id, data={"K1MA": {"K1MAE01": 5}})
            elif course == "english":
                self.refund_query.update_user_flags(user_id=user_id, data={"K1GE": {"K1GEE03": 5}})
            elif course == "lianBao":
                self.refund_query.update_user_flags(
                    user_id=user_id, data={"K1GE": {"K1GEE03": 5}, "K1MA": {"K1MAE01": 5}}
                )

    def test_refund_tuitionFee_redeem(self):
        """
        单科目英语体验课返现(兑换码)
        """
        # 获取用户返现前金额数据
        self.get_user_basic_data(self.tcRedeem_user_id)

        # 查询用户订单数据
        order_data = self.order_query.get_pingxxorder(
            uid=self.tcRedeem_user_id, itemid={"$in": self.redeem_itemid_list}, status={"$in": self.order_status_list}
        )

        # 执行返现接口
        check_resp = self.refund_redeem.api_get_xshare_income_home()
        # 校验数据
        assert check_resp["code"] == 0
        assert check_resp["data"]["all"] == self.all_before + 990
        assert check_resp["data"]["avaliable"] == self.available_before + 990

        # 查询返现后用户金额
        query_after = self.refund_query.select_xshare_record(self.tcRedeem_user_id)

        # 数据库返现数据校验
        assert query_after["cashbackHistory"]["apprefund99"][0]["amount"] == 990
        assert query_after["cashbackHistory"]["apprefund99"][0]["oid"] == order_data["_id"]

    def test_refund_tuitionFee_guadou(self):
        """
        单科目英语体验课返现(呱豆兑换)
        """
        # 获取用户返现前金额数据
        self.get_user_basic_data(self.tcGuadou_user_id)

        # 查询用户订单
        order_data = self.order_query.get_pingxxorder(
            uid=self.tcGuadou_user_id, itemid="L1TC", status={"$in": self.order_status_list}
        )

        # 执行返现接口
        check_resp = self.refund_guado.api_get_xshare_income_home()
        assert check_resp["code"] == 0
        assert check_resp["data"]["all"] == self.all_before + 990
        assert check_resp["data"]["avaliable"] == self.available_before + 990

        # 查询返现后用户金额
        query_after = self.refund_query.select_xshare_record(self.tcGuadou_user_id)

        # 数据库返现数据校验
        assert query_after["cashbackHistory"]["apprefund99"][0]["amount"] == 990
        assert query_after["cashbackHistory"]["apprefund99"][0]["oid"] == order_data["_id"]

    def test_refund_tuitionFee_math(self):
        """
        单科目思维体验课返现
        """
        # 注册用户
        self.register_user()
        # 购买思维体验课
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_math])
        time.sleep(3)
        # 插入完课数据
        self.update_cashback_data(user_id=self.new_user_id, course="math")

        # 获取用户返现前金额数据
        self.get_user_basic_data(self.new_user_id)

        # 查询用户订单
        order_data = self.order_query.get_pingxxorder(
            uid=self.new_user_id,
            channelItemid={"$in": self.channel_itemid_list},
            status={"$in": self.order_status_list},
            courseCategory="math",
        )
        # 查询用户lessonbuy开课时间
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        pts = course_data["MATC"]["K1MATC"]["meta"]["pts"]
        # 更新用户lessonbuy返现时间为购买时间
        self.db_lesson.update_lessonbuy_math(user_id=self.new_user_id, pts=pts)

        # 执行返现接口(已到返现时间，正常返现)
        check_resp = self.refund.api_get_xshare_income_home()
        assert check_resp["data"]["all"] == self.all_before + order_data["amount"]
        assert check_resp["data"]["avaliable"] == self.available_before + order_data["amount"]
        # 查询返现后用户金额
        query_after = self.refund_query.select_xshare_record(self.new_user_id)
        # 数据库返现数据校验
        assert query_after["cashbackHistory"]["apprefund99"][0]["amount"] == order_data["amount"]
        assert query_after["cashbackHistory"]["apprefund99"][0]["oid"] == order_data["_id"]

    def test_refund_tuitionFee_tcEnglishMath(self):
        """
        联报科目体验课返现
        """
        # 注册用户
        self.register_user()
        # 调用购买体验课方法，生成联报体验课订单
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_lianbao])
        time.sleep(3)

        # 插入完课数据
        self.update_cashback_data(user_id=self.new_user_id, course="lianBao")

        # 获取用户返现前金额数据
        self.get_user_basic_data(self.new_user_id)

        # 查询用户订单
        order_data = self.order_query.get_pingxxorder(
            uid=self.new_user_id,
            channelItemid={"$in": self.channel_itemid_list},
            status={"$in": self.order_status_list},
            courseCategory="english math",
        )
        # 查询用户lessonbuy开课时间
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        pts = course_data["MATC"]["K1MATC"]["meta"]["pts"]
        # 更新用户lessonbuy返现时间为购买时间
        self.db_lesson.update_lessonbuy_math(user_id=self.new_user_id, pts=pts)
        self.db_lesson.update_lessonbuy_english(user_id=self.new_user_id, pts=pts)

        # 执行返现接口
        check_resp = self.refund.api_get_xshare_income_home()
        assert check_resp["code"] == 0
        assert check_resp["data"]["all"] == self.all_before + order_data["amount"]
        assert check_resp["data"]["avaliable"] == self.available_before + order_data["amount"]

        # 查询返现后用户金额
        query_after = self.refund_query.select_xshare_record(self.new_user_id)

        # 数据库返现数据校验
        assert query_after["cashbackHistory"]["apprefund99"][0]["amount"] == order_data["amount"]
        assert query_after["cashbackHistory"]["apprefund99"][0]["oid"] == order_data["_id"]

    def test_refund_tuitionFee_tcEnglish_Math(self):
        """
        单科目多订单体验课返现
        """
        # 注册用户
        self.register_user()
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_english])
        time.sleep(3)
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_math])
        time.sleep(3)

        # 插入完课数据
        self.update_cashback_data(user_id=self.new_user_id, course="lianBao")

        # 获取用户返现前金额数据
        self.get_user_basic_data(self.new_user_id)

        # 查询用户订单
        order_data = list(
            self.order_query.get_pingxxorder_many(
                uid=self.new_user_id,
                channelItemid={"$in": self.channel_itemid_list},
                status={"$in": self.order_status_list},
                courseCategory={"$in": ["english", "math"]},
            )
        )

        # 查询用户lessonbuy开课时间
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        pts = course_data["MATC"]["K1MATC"]["meta"]["pts"]
        # 更新用户lessonbuy返现时间为购买时间
        self.db_lesson.update_lessonbuy_math(user_id=self.new_user_id, pts=pts)
        self.db_lesson.update_lessonbuy_english(user_id=self.new_user_id, pts=pts)

        # 执行返现接口
        check_resp = self.refund.api_get_xshare_income_home()
        assert check_resp["code"] == 0
        assert check_resp["data"]["all"] == self.all_before + order_data[0]["amount"] + order_data[1]["amount"]
        assert (
            check_resp["data"]["avaliable"] == self.available_before + order_data[0]["amount"] + order_data[1]["amount"]
        )

        # 查询返现后用户金额
        query_after = self.refund_query.select_xshare_record(self.new_user_id)

        # 数据库返现数据校验
        assert len(query_after["cashbackHistory"]["apprefund99"]) == 2
        if order_data[0]["_id"] == query_after["cashbackHistory"]["apprefund99"][0]["oid"]:
            assert order_data[0]["amount"] == query_after["cashbackHistory"]["apprefund99"][0]["amount"]
        elif order_data[0]["_id"] == query_after["cashbackHistory"]["apprefund99"][1]["oid"]:
            assert order_data[0]["amount"] == query_after["cashbackHistory"]["apprefund99"][1]["amount"]

    def test_refund_failed_math(self):
        """
        单科目思维体验课完课未到返现时间不会返现
        """
        # 注册用户
        self.register_user()
        # 购买思维体验课
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_math])
        time.sleep(3)
        # 插入完课数据
        self.update_cashback_data(user_id=self.new_user_id, course="math")
        # 获取用户返现前金额数据
        self.get_user_basic_data(self.new_user_id)
        # 执行返现接口(未到返现时间，虽然完课，但是不返现)
        check_resp = self.refund.api_get_xshare_income_home()
        assert check_resp["code"] == 0
        assert check_resp["data"]["all"] == self.all_before
        assert check_resp["data"]["avaliable"] == self.available_before

    def test_refund_failed_lianBao(self):
        """
        用户存在一笔两个科目都已学完未到返现时间的联报科目订单
        """
        # 注册用户
        self.register_user()
        # 调用购买体验课方法，生成联报体验课订单
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_lianbao])
        time.sleep(3)

        # 插入完课数据
        self.update_cashback_data(user_id=self.new_user_id, course="lianBao")

        # 获取用户返现前金额数据
        self.get_user_basic_data(self.new_user_id)

        # 执行返现接口(未到返现时间，虽然完课，但是不返现)
        check_resp = self.refund.api_get_xshare_income_home()
        assert check_resp["code"] == 0
        assert check_resp["data"]["all"] == self.all_before
        assert check_resp["data"]["avaliable"] == self.available_before

    def test_refund_failed_lianBao2(self):
        """
        用户存在一笔其中一个科目已学完未到返现时间，另一个科目已学完已到返现时间的的联报科目订单，不会返现
        """
        # 注册用户
        self.register_user()
        # 调用购买体验课方法，生成联报体验课订单
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_lianbao])
        time.sleep(3)

        # 插入完课数据
        self.update_cashback_data(user_id=self.new_user_id, course="lianBao")

        # 查询用户lessonbuy开课时间
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        pts = course_data["MATC"]["K1MATC"]["meta"]["pts"]
        # 更新用户lessonbuy返现时间为购买时间，仅更新思维科目
        self.db_lesson.update_lessonbuy_math(user_id=self.new_user_id, pts=pts)

        # 获取用户返现前金额数据
        self.get_user_basic_data(self.new_user_id)

        # 执行返现接口(未到返现时间，虽然完课，但是不返现)
        check_resp = self.refund.api_get_xshare_income_home()
        assert check_resp["code"] == 0
        assert check_resp["data"]["all"] == self.all_before
        assert check_resp["data"]["avaliable"] == self.available_before
