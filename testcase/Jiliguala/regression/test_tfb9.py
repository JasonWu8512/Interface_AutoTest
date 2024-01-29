'''
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/12/22
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
from business.Jiliguala.WebBuy.toufangAB import Tfab
from business.Jiliguala.WebBuy.NewTeade import NewTeade
from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper


@pytest.mark.menu
class Testpossessweeks(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # # 【代码提交用】获取环境变量
        cls.config = cls.dm.set_env_path(env)
        # # 【代码提交用】
        print(env)
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('fat')  # 测试环境
        cls.dm.set_domain(cls.config['url'])  # 准备测试的url地址

        cls.cocosEnv = cls.config["cocosEnv"]  # 读取cocos环境
        cls.CS_user = cls.config["toufangAB"]  # 读取账户信息
        cls.mybid = cls.config["center"]

        # 实例化类
        cls.possess4weeks = Tfab()
        cls.possess4weeks2 = NewTeade()
        cls.getmobile = ApiSmsInfo()
        # 获取随机手机号
        cls.mobile1 = cls.getmobile.api_get_mobile()
        # 获取验证码
        cls.mobile = cls.mobile1["data"]

        """
        步骤
       1 站外打开年课投放9.9元购买链接
       2 手机号登陆
       3 点击购买
       4 购买成功页面跳转加好友页面

       返回
       1 手机号登陆成功
       2 购买成功
       3 加好友页面返回课程信息
       4 断言购买前订单与购买后订单是否一直
       5 断言班主任分配是否为兜底班主任


        """

    def test_Tfb9(self):
        # 随机手机号获取验证码
        resp = self.possess4weeks.api_web_sms(mobile=self.mobile)
        assert resp["code"] == 0
        print(resp)

        # 读取数据库获取验证码
        resp0 = self.possess4weeks2.api_get_sms(mobile=self.mobile)
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
        self.possessweeks1 = Tfab(token=token1)
        self.refund = ApiSuper(token=token1, agent=None)
        resp2 = self.possessweeks1.api_order_create_V2(itemid=self.CS_user["itemid"],url=self.CS_user["url1"], sp2xuIds=self.CS_user["sp2xuIds1"],
                                                       source=self.CS_user["source1"],sharer= "",xshareInitiator="")
        assert resp2["code"] == 0
        # 取订单号传入下一个订单信息接口
        oid = resp2["data"]["orderNo"]
        print(oid)
        print(resp2)

        # 传入oid获取商品信息
        resp3 = self.possessweeks1.api_order_charge_V2(order=oid, extra=self.CS_user["extra1"])
        assert resp3["code"] == 0
        print(resp3)

        id = resp3['data']['id']
        time_paid = resp3['data']['created']
        order_no = resp3['data']['order_no']
        current_timestamp = int(time.time() * 1000)
        transaction_no = 'MOCK4200001986' + str(current_timestamp)

        #购买支付
        resp4 = self.possessweeks1.api_post_mock(id=id, time_paid=time_paid, order_no=order_no, transaction_no=transaction_no)
        #断言支付成功
        assert resp4["code"] == 0
        print(resp4)

        resp5 = self.possessweeks1.api_mars_order(oid =order_no)
        assert resp5["code"] == 0
        # assert resp5["status"] == "paid"    #断言支付购买成功
        print("在这",resp5)

        #填写地址
        resp6 = self.possessweeks1.api_order_address(oid=order_no)
        assert resp6["code"] == 0
        print(resp6)

        time.sleep(1)
        #购买成功，获取分配信息
        resp7 = self.possessweeks1.api_tutor_info_v2(orderId=oid)
        # 断言支付成功
        assert resp7["code"] == 0
        assert resp7["data"]["tutorList"][0]["oid"] == oid         #断言支付分配信息里的订单号
        # assert resp7["data"]["tutorList"][1]["tid"] == "T2894"
        print(resp7)
        time.sleep(9)






