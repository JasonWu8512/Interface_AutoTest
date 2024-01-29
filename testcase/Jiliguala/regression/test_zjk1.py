''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/12/28
===============
'''
''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/12/27
===============
'''


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.businessQuery import usersQuery
import pytest
import pytest_check as check
import os
import base64
import time
from business.Jiliguala.lessonbiz import ApiSuper
from business.businessQuery import usersQuery, pingxxorderQuery, ghsQuery
from business.Jiliguala.WebBuy.NewTeade import NewTeade
from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper


@pytest.mark.menu
class Testpossessweeks(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # # 【代码提交用】从环境变量获取env
        # env = os.environ.get('env')
        # # 【代码提交用】获取环境变量
        # cls.config = cls.dm.set_env_path(env)
        # # 【代码提交用】
        # print(env)
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')  # 测试环境
        cls.dm.set_domain(cls.config['url'])  # 准备测试的url地址

        cls.cocosEnv = cls.config["cocosEnv"]  # 读取cocos环境
        cls.CS_user = cls.config["CS_user"]  # 读取账户信息
        cls.mybid = cls.config["center"]
        cls.spu = cls.config["possess4weeks"]

        # 实例化类
        cls.possess4weeks = NewTeade()
        cls.getmobile = ApiSmsInfo()
        # 获取随机手机号
        cls.mobile1 = cls.getmobile.api_get_mobile()
        # 获取验证码
        cls.mobile = cls.mobile1["data"]

        """
        步骤
       1 站外打开1.5正价课购买链接
       2 手机号登陆
       3 点击购买
       4 购买成功页面跳转加好友页面

       返回
       1 手机号登陆成功
       2 购买成功
       3 加好友页面返回课程信息
       4 断言购买前订单与购买后订单是否一致
       5 退款

        """

    def test_Zjk1(self):
        # 随机手机号获取验证码
        resp = self.possess4weeks.api_web_sms(mobile=self.mobile)
        assert resp["code"] == 0
        print(resp)
        print(self.mobile)
        # time.sleep(4)
        # 读取数据库获取验证码
        resp0 = self.possess4weeks.api_get_sms(mobile=self.mobile)
        assert resp["code"] == 0
        print(resp0)
        code = resp0["data"]["sms"]["code"]
        print(code)
        # code = usersQuery().get_users(mobile=self.mobile)["sms"]["code"]
        # print(code)
        # 站外使用验证码登陆
        resp1 = self.possess4weeks.api_users_token(mobile=self.mobile, code=code, typ=self.mybid["typ"])
        assert resp1["data"]["registerFrom"] == "JLGL"
        assert resp1["data"]["mobile"] == self.mobile
        print(resp1)

        # 登陆成功，取用户tok和uid加密获取token


        token = resp1["data"]["tok"]
        uid = resp1["data"]["_id"]
        code = base64.b64encode(f'{uid}:{token}'.encode('utf-8'))
        token1 = 'Basic ' + str(code, encoding="utf-8")
        print(token1)

        # 点击支付生成订单
        self.possessweeks1 = NewTeade(token=token1)
        self.refund = ApiSuper(token=token1, agent=None)
        resp2 = self.possessweeks1.api_eshop_v2_orders2(payPrice=self.spu["payPrice3"],sp2xuId=self.spu["sp2xuId4"],spuNo=self.spu["spuNo4"])
        assert resp2["code"] == 0
        # 取订单号传入下一个订单信息接口
        oid = resp2["data"]["orderNo"]
        print(oid)
        print(resp2)

        # 传入oid获取商品信息
        resp3 = self.possessweeks1.api_eshop_v2_orders_charge(oid=oid, agent=self.spu["agent3"],
                                                              payTotal=self.spu["payTotal4"],
                                                              channel=self.spu["channel3"])
        assert resp3["code"] == 0
        # assert resp3["data"]["subject"] == "呱呱美语课级别1~6"
        print(resp3)
        # 购买商品， mock支付 获取mock支付需要信息，id:付款单，time_paid:支付时间，order_no:订单编号，transaction_no:支付id

        id = resp3['data']['merOrderId']
        print(id)
        time_paid = resp3['data']['miniPayRequest']["timeStamp"]
        print(time_paid)
        order_no = oid
        print(order_no)
        current_timestamp = int(time.time() * 1000)
        transaction_no = 'MOCK4200001986' + str(current_timestamp)

        # 购买支付
        resp4 = self.possessweeks1.api_post_mock(id=id, time_paid=time_paid, order_no=order_no,
                                                 transaction_no=transaction_no)
        # 断言支付成功
        assert resp4["code"] == 0
        print(resp4)

        # 购买成功接口
        resp5 = self.possessweeks1.api_order_status(oid=oid)
        # 断言支付状态为已支付
        assert resp5["data"]["status"] == "paid"
        # 断言购买的课程
        assert resp5["data"]["itemid"] == "L1XX_L6XX_E_WITHOUT_DISCOUNT"
        print(resp5)

        # 页面跳转到支付成功页
        resp6 = self.possessweeks1.api_eshop_ghs_info(orderId=oid)
        assert resp6["data"]["title"] == "呱呱美语课级别1~6"
        assert resp6["data"]["subject"] == "english"
        print(resp6)
        time.sleep(0.5)
        resp7 = self.possessweeks1.api_tutor_info_v2(orderId=oid)
        assert resp6["code"] == 0

        print(resp7)

        # 查询数据库，获取已购买的订单
        # order = pingxxorderQuery().get_pingxxorder(uid=uid, status='paid', itemid='S1GE_W1_4_SGU_new')['_id']
        # print(order)
        # 断言支付前订单id=支付后订单id
        # assert order == order_no

        # time.sleep(1)
        # 购买成功分配规划师，因为测试账号，测试环境规划师分配是固定的为911
        # ghs = ghsQuery().ghs_user(_id = uid)["ghs"]
        # #断言账户规划师分配为911
        # assert ghs == "911"
        # print(ghs)

        # 退款
        resp9 = self.refund.api_post_refund(orderNo=order_no)
        assert resp9["code"] == 200
        assert resp9["msg"] == "success"
        print(resp9)
        time.sleep(9)





