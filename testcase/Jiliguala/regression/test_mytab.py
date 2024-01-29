''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/4/10
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.mytab.mytab import Mytab
from business.Jiliguala.user.ApiUser import ApiUser
from business.businessQuery import usersQuery
import base64
import os


@pytest.mark.menu
class TestMytab(object):
    dm = Domains()

    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # 【代码提交用】获取环境变量
        cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        print(env)
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')  # 测试环境  本地调试用
        cls.dm.set_domain(cls.config['url'])  # 准备测试的url地址
        cls.user = ApiUser()
        cls.myBid = cls.config["center"]  # 读取所用到的bid
        cls.cocosEnv = cls.config["cocosEnv"]  # 读取cocos环境
        cls.CS_user = cls.config["CS_user"]  # 读取账户信息
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])  # 登陆用户获取token
        cls.myapi = Mytab(token=cls.token)  # 传入token

    def test01_v3_tab(self):

        """
        家长中心详情页
        """
        resp = self.myapi.api_cenyer_v3_tab(self.myBid["bid"])
        assert resp["code"] == 0
        check.equal(resp["code"], 0)

    def test02_currentLevel(self):

        """
        切换宝贝，设置该宝贝为当前宝贝
        """
        resp = self.myapi.api_currentLevel(self.myBid["bid"])
        check.equal(resp["code"],0)
        assert resp["data"]["level"] == "L1XX" or "S5GE"

    def test03_babies(self):

        """
        添加新的宝贝
        """
        resp = self.myapi.api_babies(self.myBid["bid"])
        # bid1 = self.myapi.api_babies()
        resp2 = self.myapi.api_delete_check(resp)
        check.equal(resp2["code"],0)

    def test04_sms_logout(self):
        """
        获取验证码
        """
        resp = self.myapi.api_sms_logout()
        check.equal(resp["code"],0)

    def test05_delete_babies(self):
        """
        删除宝贝
        """
        bid1 = self.myapi.api_babies(self.myBid["bid"])                              #获取需要删除宝贝的bid
        code = usersQuery().get_users(mobile=self.CS_user["user"])["sms"]["code"]    #获取验证码
        resp = self.myapi.api_delete_babies(bid1,self.CS_user["user"],code)
        check.equal(resp["code"],0)

    def test06_get_home(self):
        resp = self.myapi.api_get_home()
        # 断言返回code码正常
        check.equal(resp["code"], 0)
        print(resp)
        # 断言用户状态为1(魔石商城用户)
        check.equal(resp["data"]["userStatus"], 1)

    def test07_get_item(self):
        resp = self.myapi.api_get_item()
        # 断言接口正常返回商品
        check.equal(resp["data"]["items"][0]["commodityTitle"], "呱呱手机支架" or "叽里呱啦定制印章")

    def test08_get_detail(self):
        resp = self.myapi.api_get_detail("MG_goods_012_SPU")
        resp01 = resp["data"]["itemName"]
        print(resp01)
        # 断言商品信息与接口返回一致
        check.equal(resp["data"]["itemName"], "呱呱手机支架")
        print(resp)

    def test09_get_trans(self):
        resp = self.myapi.api_get_trans('0', 'in')
        # 断言返回code码正常
        check.equal(resp["code"], 0)
        print(resp)
        # 断言页码
        check.equal(resp["data"]["pageNo"], 1)

        # 断言收入tab数据
        check.equal(resp["data"]["transactions"][0]["title"], "英语学习奖励")

        # 断言支出tab数据
        resp01 = self.myapi.api_get_trans('0', 'out')
        check.equal(resp01["data"]["transactions"][0]["title"], "魔石商城兑换商品")

    def test10_coupon_available(self):
        """
        优惠券未使用
        """
        resp = self.myapi.api_coupon_available(self.myBid["bid"],self.myBid["level"])
        check.equal(resp["code"], 0)


    def test11_coupon_expired(self):
        """
        优惠券已过期
        """
        resp = self.myapi.api_coupon_available(self.myBid["bid"],self.myBid["level"])
        check.equal(resp["code"], 0)

    def test12_coupon_consumed(self):
        """
        优惠券已使用
        """
        resp = self.myapi.api_coupon_available(self.myBid["bid"],self.myBid["level"])
        check.equal(resp["code"], 0)

    def test13_commodity_spu(self):
        """
        学习材料及周边详情页
        """
        resp = self.myapi.api_commodity_spu()
        check.equal(resp["code"], 0)

    def test14_commodity_spu_Liang_SPU_ALL(self):
        """
        学习材料及周边商品详情页
        """
        resp = self.myapi.api_commodity_spu_Liang_SPU_ALL()
        check.equal(resp["code"], 0)

    def test15_trade_order(self):
        """
        订单物流详情页
        """
        resp = self.myapi.api_trade_order()
        check.equal(resp["code"], 0)

    def test16_trade_order_details(self):
        """
        订单物流详情页
        """
        resp = self.myapi.api_trade_order_details(self.myBid["api_url"])
        check.equal(resp["code"], 0)

    # def test17_web_sms(self):
    #     """
    #     站外获取验证码
    #     """
    #     resp = self.myapi.api_web_sms(self.myBid["mobile"])
    #     check.equal(resp["code"], 0)

    # def test18_users_token(self):
    #     """
    #     站外验证码登录
    #     登录后获取该账号的token
    #     传入到注销接口中获取注销账号验证码
    #     注销账号
    #     """
    #     #站外获取验证码
    #     resp0= self.myapi.api_web_sms(self.myBid["mobile"])
    #     check.equal(resp0["code"], 0)
    #
    #     #验证码登录成功
    #     self.code = usersQuery().get_users(mobile=self.myBid["mobile"])["sms"]["code"]
    #     resp = self.myapi.api_users_token(self.myBid["mobile"],self.code,typ = self.myBid["typ"])
    #     check.equal(resp["code"], 0)
    #
    #     #获取登陆后的账号的token
    #     token = resp["data"]["tok"]
    #     uid = resp["data"]["_id"]
    #     code = base64.b64encode(f'{uid}:{token}'.encode('utf-8'))
    #     token1 = 'Basic ' + str(code, encoding="utf-8")
    #     print(token1)
    #     #实例化传入token
    #     self.myapi1 = Mytab(token= token1)
    #     resp1=self.myapi1.api_users_sms_logout()
    #     assert resp1["code"] == 0
    #
    #     #传入验证码注销账号
    #     self.code1 = usersQuery().get_users(mobile=self.myBid["mobile"])["sms"]["code"]
    #     resp2 =self.myapi1.api_security_info(mobile=self.myBid["mobile"],code = self.code1)
    #     assert resp2["code"] == 0
    #     assert resp2["data"]["status"] == "success"
    #     #传入token





