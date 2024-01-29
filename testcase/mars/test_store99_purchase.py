# coding=utf-8
# @Time    : 2021-5-20 13:39
# @Author  : lijun_qi
# @File    : test_store99_purchase.py
# @Software: PyCharm

import time

import pytest
import pytest_check as check

from business.businessQuery import lessonQuery, pingxxorderQuery, usersQuery
from business.common.UserProperty import UserProperty
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.Trade.tradeOrder.ApiRefundOpenFeign import ApiRefund
from business.mars.ApiMyOrderListAndAddressAndTutor import ApiPostAddress
from business.mars.ApiOrder import ApiOrder
from business.mars.ApiPurchasepage import ApiPurchasepage
from business.Jiliguala.user.ApiUserInfo import ApiUserInfo
from business.mysqlQuery import EshopQuery
from business.zero.dataTool.ApiPromoterData import ApiPromoterData
from business.zero.mock.ApiMock import ApiMock
from config.env.domains import Domains
from utils.format.format import now_timeStr


@pytest.mark.xShare
@pytest.mark.Mars
# @pytest.mark.Test_store_purchase
class Test_store_purchase(object):
    """
    store项目9.9体验课购买，不包含小程序
    """

    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path(env="fat")
        # 设置域名
        cls.dm.set_domain(cls.config["url"])

        # 初始化用户数据
        cls.mobile = cls.config["xshare"]["tc_user"]
        cls.unionId = cls.config["xshare"]["unionId"]

        # 初始化购课sp2xuId
        cls.sp2xuId_lianbao = cls.config["xshare"]["sp2xuId"]["sp2xuId_lianbao"]  # 英语+思维体验课
        cls.sp2xuId_math = cls.config["xshare"]["sp2xuId"]["sp2xuId_math"]  # 呱呱思维趣味AI互动课K1
        cls.sp2xuId_english = cls.config["xshare"]["sp2xuId"]["sp2xuId_english"]  # 呱呱英语趣味AI互动课K1
        cls.sp2xuId_Normal = cls.config["xshare"]["sp2xuId"]["sp2xuId_Normal"]  # 呱呱思维正价课
        # 实例用户对象
        cls.new_user = ApiUserInfo()

        # 数据工具
        cls.dataTool = ApiPromoterData()
        # 退款
        cls.refund = ApiRefund()
        # 开mock
        cls.mock = ApiMock()
        # cls.mock.api_update_mock_status(
        #     status=True, env=cls.config["env"], server_list=["交易中台"], user_email="lijun_qi@jiliguala.com"
        # )
        # time.sleep(120)
        # 实例化数据库查询对象
        cls.query = pingxxorderQuery()
        cls.db_lesson = lessonQuery()
        cls.db_users = usersQuery()
        cls.db_eshop = EshopQuery()

        price = cls.db_eshop.eshop.query(
            'select price_rmb from commodity where commodity_no ="Ian-Test-MA"'
        )  # 呱呱思维正价课价格
        cls.sp2xuId_pay_price = int(price[0]["price_rmb"])
        # cls.sp2xuId_pay_price = cls.config["xshare"]["sp2xuId"]["sp2xuId_pay_price"]  # 呱呱思维正价课价格

    @classmethod
    def teardown_class(cls):
        pass
        # 关mock
        # cls.mock.api_update_mock_status(
        #     status=False, env=cls.config["env"], server_list=["交易中台"], user_email="lijun_qi@jiliguala.com"
        # )

    def setup_method(self):
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
        self.new_user_guaid = self.user_prop.user_guaid
        self.wechattoken = UserProperty(self.mobile, unionid=self.unionId).encryptWechatToken_bindwechat
        # 实例化对象
        self.page = ApiPurchasepage(basic_auth=self.new_user_token)
        # 实例化订单类
        self.ord = ApiOrder(basic_auth=self.new_user_token)

    def teardown_method(self):
        """
        注销用户重复使用
        """
        self.logout_user(mobile=self.mobile)

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

    def buy_normal_lesson(self, token, channel, sp2xu_id, pay_price, pay_total, useGuadou=False):
        """购买正价课"""
        normal_order = ApiNewOrders(token)
        create_order = normal_order.api_order_create(sp2xuId=sp2xu_id, payPrice=pay_price, useGuadou=useGuadou)
        purchase_res = normal_order.api_charge_create(
            oid=create_order["data"]["orderNo"], channel=channel, payTotal=pay_total
        )
        return purchase_res

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

    def buy_tc_lesson_wechat(
        self,
        sp2xuIds,
        pay_wechat_token,
        nonce=now_timeStr(),
        item_id="H5_XX_Sample",
        source="autoTest",
        xshare_initiator=None,
        sharer=None,
        channel="wx_pub",
        pay_wechat_token_typ="silent",
    ):
        """微信环境调起微信支付购买体验课"""
        # 调用后端创建订单接口
        order_res = self.ord.api_create_v2(
            item_id=item_id,
            nonce=nonce,
            source=source,
            xshare_initiator=xshare_initiator,
            sharer=sharer,
            sp2xuIds=sp2xuIds,
        )
        # 创单接口是否正常
        assert order_res["code"] == 0 and order_res["status_code"] == 200

        # 调用后端支付接口
        charge_res = self.ord.api_charge_v2(
            oid=order_res["data"]["orderNo"],
            channel=channel,
            pay_wechat_token_typ=pay_wechat_token_typ,
            pay_wechat_token=pay_wechat_token,
        )
        time.sleep(5)
        assert charge_res["code"] == 0 and charge_res["status_code"] == 200

        return charge_res

    def create_tc_order(
        self,
        sp2xuIds,
        nonce=now_timeStr(),
        item_id="H5_XX_Sample",
        source="autoTest",
        xshare_initiator=None,
        sharer=None,
    ):
        """创建体验课订单"""
        # 调用后端创建订单接口
        order_res = self.ord.api_create_v2(
            item_id=item_id,
            nonce=nonce,
            source=source,
            xshare_initiator=xshare_initiator,
            sharer=sharer,
            sp2xuIds=sp2xuIds,
        )
        return order_res

    def course_refuded(
        self,
        orderNo,
    ):
        resp_refund = self.refund.api_order_refund(orderNo=orderNo)
        check.equal(resp_refund["status_code"], 200)

    def test_new_user_purchase_english(self):
        """
        新用户购买英语单科目体验课
        @return:
        """
        # 调用购买体验课方法，生成英语体验课订单
        purchase_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_english])
        time.sleep(3)
        # 检查订单状态是否正确
        order_data = self.query.get_pingxxorder(_id=purchase_res["data"]["order_no"])
        assert order_data["status"] == "needaddress"  # 订单状态
        assert order_data["courseCategory"] == "english"  # 科目信息
        assert order_data["amount"] == purchase_res["data"]["amount"]  # 价格
        # 检查课程数据是否正确
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        assert len(course_data["TC"]["K1GETC"]["buy"]) == 5
        print(purchase_res["data"]["order_no"])

    def test_new_user_purchase_math(self):
        """
        新用户购买思维单科目体验课
        @return:
        """
        # 调用购买体验课方法，生成思维体验课订单
        purchase_res = self.buy_tc_lesson_wechat(sp2xuIds=[self.sp2xuId_math], pay_wechat_token=self.wechattoken)
        time.sleep(3)
        # 检查订单状态是否正确
        order_data = self.query.get_pingxxorder(_id=purchase_res["data"]["order_no"])
        assert order_data["status"] == "needaddress"  # 订单状态
        assert order_data["courseCategory"] == "math"  # 科目信息
        assert order_data["amount"] == purchase_res["data"]["amount"]  # 价格
        # 检查课程数据是否正确
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        assert len(course_data["MATC"]["K1MATC"]["buy"]) == 5
        print(purchase_res["data"]["order_no"])

    def test_new_user_purchase_lianbao(self):
        """
        新用户购买联报科目体验课
        @return:
        """
        # 调用购买体验课方法，生成联报体验课订单
        purchase_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_lianbao])
        time.sleep(3)
        # 检查订单状态是否正确
        order_data = self.query.get_pingxxorder(_id=purchase_res["data"]["order_no"])
        assert order_data["status"] == "needaddress"
        assert order_data["courseCategory"] == "english math"
        assert order_data["amount"] == purchase_res["data"]["amount"]
        # 检查课程数据是否正确
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        assert len(course_data["TC"]["K1GETC"]["buy"]) == 5
        assert len(course_data["MATC"]["K1MATC"]["buy"]) == 5
        print(purchase_res["data"]["order_no"])

    def test_new_user_purchase_math_english(self):
        """
        新用户购买思维单科目后继续购买英语体验课
        @return:
        """
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_math])
        time.sleep(3)
        purchase_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_english])
        # 检查订单状态是否正确
        order_data = self.query.get_pingxxorder(_id=purchase_res["data"]["order_no"])
        assert order_data["status"] == "needaddress"
        assert order_data["courseCategory"] == "english"
        assert order_data["amount"] == 600
        # 检查课程数据是否正确
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        assert len(course_data["TC"]["K1GETC"]["buy"]) == 5
        print(purchase_res["data"]["order_no"])

    def test_new_user_purchase_second_course(self):
        """
        新用户购买思维正价课后继续购买英语体验课
        @return:
        """
        # 用户购买思维正价课
        self.buy_normal_lesson(
            token=self.new_user_token,
            channel="wx_pub",
            sp2xu_id=self.sp2xuId_Normal,
            pay_price=self.sp2xuId_pay_price,
            pay_total=self.sp2xuId_pay_price,
        )
        time.sleep(5)
        # 用户继续购买英语体验课
        purchase_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_english])
        time.sleep(3)
        # 检查订单状态是否正确
        order_data = self.query.get_pingxxorder(_id=purchase_res["data"]["order_no"])
        assert order_data["status"] == "needaddress"
        assert order_data["courseCategory"] == "english"
        assert order_data["amount"] == 600
        # 检查课程数据是否正确
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        assert len(course_data["TC"]["K1GETC"]["buy"]) == 5
        print(purchase_res["data"]["order_no"])

    def test_new_user_purchase_math_math(self):
        """
        新用户购买思维体验课后继续购买思维体验课
        @return:
        """
        # 先购买思维体验课
        self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_math])
        time.sleep(3)
        # 再次购买思维体验课
        create_res = self.create_tc_order(sp2xuIds=[self.sp2xuId_math])
        # 检查创单接口返回
        assert create_res["status_code"] == 200 and create_res["code"] == 44301

    def test_new_user_purchase_mathNormal_math(self):
        """
        新用户购买思维正价课后再次购买思维体验课
        @return:
        """
        # 用户购买思维正价课
        self.buy_normal_lesson(
            token=self.new_user_token,
            channel="wx_pub",
            sp2xu_id=self.sp2xuId_Normal,
            pay_price=self.sp2xuId_pay_price,
            pay_total=self.sp2xuId_pay_price,
        )
        time.sleep(5)
        # 再次购买思维体验课
        create_res = self.create_tc_order(sp2xuIds=[self.sp2xuId_math])
        # 检查创单接口返回
        assert create_res["status_code"] == 200 and create_res["code"] == 44203

    def test_new_user_purchase_eng_refund_eng(self):
        """
        新用户购买英语体验课退款后再次购买英语体验课
        @return:
        """
        # 先购买英语体验课
        purchase_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_english])
        time.sleep(3)

        # 退款英语体验课订单
        self.course_refuded(orderNo=purchase_res["data"]["order_no"])
        time.sleep(5)
        # 再次购买英语体验课
        create_res = self.create_tc_order(sp2xuIds=[self.sp2xuId_english])
        # 检查创单接口返回
        assert create_res["status_code"] == 200 and create_res["code"] == 44301

    def test_new_user_purchase_eng_refund_math(self):
        """
        新用户购买英语体验课退款后继续购买思维体验课
        @return:
        """
        # 先购买英语体验课
        pur_eng_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_english])
        time.sleep(3)
        # 英语订单填地址
        address = ApiPostAddress(auth_token=self.new_user_token)
        address_res = address.post_address(oid=pur_eng_res["data"]["order_no"])
        check.equal(address_res["status_code"], 200)
        # 退款英语体验课订单
        self.course_refuded(orderNo=pur_eng_res["data"]["order_no"])
        time.sleep(5)
        # 购买思维体验课
        pur_math_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_math])
        # 检查订单状态是否正确
        order_data = self.query.get_pingxxorder(_id=pur_math_res["data"]["order_no"])
        assert order_data["status"] == "needaddress"
        assert order_data["courseCategory"] == "math"
        assert order_data["amount"] == 990
        # 检查课程数据是否正确
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        assert len(course_data["MATC"]["K1MATC"]["buy"]) == 5
        print(pur_math_res["data"]["order_no"])

    def test_new_user_purchase_normalmath_refund_english(self):
        """
        新用户购买思维正价课后退款后再次购买英语体验课
        @return:
        """
        # 用户购买思维正价课
        pur_math_res = self.buy_normal_lesson(
            token=self.new_user_token,
            channel="wx_pub",
            sp2xu_id=self.sp2xuId_Normal,
            pay_price=self.sp2xuId_pay_price,
            pay_total=self.sp2xuId_pay_price,
        )
        time.sleep(5)
        # 退款思维正价课订单
        self.course_refuded(orderNo=pur_math_res["data"]["order_no"])
        time.sleep(5)
        # 购买英语体验课
        pur_english_res = self.buy_tc_lesson(sp2xuIds=[self.sp2xuId_english])
        # 检查订单状态是否正确
        order_data = self.query.get_pingxxorder(_id=pur_english_res["data"]["order_no"])
        assert order_data["status"] == "needaddress"
        assert order_data["courseCategory"] == "english"
        assert order_data["amount"] == 990
        # 检查课程数据是否正确
        course_data = self.db_lesson.get_lessonbuy(_id=self.new_user_id)
        assert len(course_data["TC"]["K1GETC"]["buy"]) == 5
        print(pur_english_res["data"]["order_no"])
