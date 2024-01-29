# coding=utf-8
# @Time    : 2021/3/30 5:25 下午
# @Author  : jerry
# @File    : test_promoter_status.py
import time
import pytest

from business.zero.dataTool.ApiPromoterData import ApiPromoterData
from business.zero.mock.ApiMock import ApiMock
from config.env.domains import Domains
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.promoter.ApiPromoterLogin import ApiPromoterLogin
from business.common.UserProperty import UserProperty
from business.mars.ApiOrder import ApiOrder
from business.promoter.ApiRefund import ApiRefund
from utils.enums.businessEnums import PromoterOperationEnum
from utils.format.format import now_timeStr
from business.businessQuery import promoterQuery, pingxxorderQuery, wcuserQuery


@pytest.mark.promoter
@pytest.mark.promoterStatus
class TestPromoterStatus:
    """推广人资格与状态相关用例"""
    promoterQuery = promoterQuery()
    wcuserQuery = wcuserQuery()
    # pingxxorderQuery = promoterQuery()
    promoter_order = None
    fan_99order = None
    fan_normal_order = None
    fan_99mock_response = None
    promoter_id = None
    oid = []

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.universal_promoterUser = UserProperty(cls.config['promoter']['promoter2'])  # 构建异常推广人的user实例
        cls.user = UserProperty(cls.config['promoter']['promoter3'])  # 构建还未成为推广人的用户user实例，用于测试自动注册等场景
        cls.user_6weeks = UserProperty(cls.config['promoter']['promoter10'])  # 双月课推广人账号
        cls.fanUser = UserProperty(cls.config['promoter']['fan2'])  # 构建上面用户好友的user实例，用于测试自动注册等场景
        cls.fanUser_6weeks = UserProperty(cls.config['promoter']['fan9'])  # 双月课粉丝
        # 设置wc_users 为当前当前用户uid
        #cls.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=cls.fanUser.user_id)
        cls.fanuser_wechattoken = cls.fanUser.encryptWechatToken_pingpp
        cls.promoterLogin_universal = ApiPromoterLogin(
            wechat_token=cls.universal_promoterUser.encryptWechatToken_promoter)
        cls.pro_refund = ApiRefund()  # 创建一个用于退款的实例
        cls.promoter_dataTool = ApiPromoterData()
        cls.fanUser_order = ApiOrder(wechat_token=cls.fanuser_wechattoken, basic_auth=cls.fanUser.basic_auth)
        # cls.mock = ApiMock()
        # cls.mock.api_update_mock_status(status=True, env=cls.config['env'], server_list=['交易中台'],
        #                                 user_email='jack_wu@jiliguala.com')
        cls.pingxxorderQuery = pingxxorderQuery()
        # time.sleep(150)

    def teardown(self):
        # 如果粉丝9.9课退款成功，删除订单
        if self.fan_99mock_response is not None:
            if self.fan_99mock_response["status"] == 'succeeded':
                time.sleep(5)
                if self.fan_99order:
                    self.pingxxorderQuery.delete_pingxxorder(_id=self.fan_99order)
                    self.fan_99order = None
        if self.oid:
            for id in self.oid:
                res = self.pro_refund.api_refund(id)
                if res["code"] == 200:
                    self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                                 operation=PromoterOperationEnum.get_chinese(
                                                                     "删除粉丝购买的课程记录"),
                                                                 orderId=id)
            self.oid = []
        # 删除推广人账户表记录
        if self.promoter_id:
            self.promoterQuery.delete_promoter_accounts(_id=self.promoter_id)
            self.promoter_id = None
        # 删除锁粉信息,删除粉丝锁粉的信息
        self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                     operation=PromoterOperationEnum.get_chinese("删除锁粉信息"),
                                                     mobile=self.fanUser.mobile)


    def buy_h5_sample_diamond_activity(self, sp2xuIds, sharer, pay_wechat_token):
        """买9.9"""
        # 生成9.9订单记录
        order_res = self.fanUser_order.api_create_v2(item_id='H5_Sample_DiamondActivity', nonce=now_timeStr(),
                                                     source="AppHomeView", xshare_initiator=sharer,
                                                     sharer=sharer, sp2xuIds=sp2xuIds)
        # 支付订单
        charge_res = self.fanUser_order.api_charge_v2(oid=order_res['data']['orderNo'], channel='wx_pub',
                                                      pay_wechat_token_typ="silent",
                                                      pay_wechat_token=pay_wechat_token)
        return charge_res

    def buy_lesson(self, token, channel, sp2xu_id, pay_price, guadou_num, pay_total):
        """购买呱美课"""
        order = ApiNewOrders(token)
        create_order = order.api_order_create(sp2xuId=sp2xu_id, payPrice=pay_price, guaDouNum=guadou_num)
        time.sleep(5)
        purchase_res = order.api_charge_create(oid=create_order['data']['orderNo'], channel=channel, payTotal=pay_total,
                                               guadouDiscount=guadou_num)
        return purchase_res

    # @pytest.mark.parametrize("sp2xu_id, pay_price, guadou_num, channel, pay_total, sp2xuIds",
    #                          [("1036", 0, 48800, "wx_pub", 0, [2819]), ("928", 0, 329900, "wx_pub", 0, [2821])])
    # def test_auto_register_promoter(self, sp2xu_id, pay_price, guadou_num, channel, pay_total, sp2xuIds):
    #     """用户购买了呱美课，邀请的9.9好友也购买了呱美课，自动注册成推广人，state为inactive"""
    #     # 用户购买呱美课
    #     user_token = self.user.basic_auth
    #     user_res = self.buy_lesson(token=user_token, channel=channel, sp2xu_id=sp2xu_id, pay_price=pay_price,
    #                                guadou_num=guadou_num, pay_total=pay_total)
    #     # 推广人正价课订单号
    #     self.promoter_order = user_res['data']['order_no']
    #     # 好友购买9.9体验课
    #     sample_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=sp2xuIds, sharer=self.user.user_id,
    #                                                             pay_wechat_token=self.fanUser.encryptWechatToken_pingpp)
    #     # 好友购买9.9体验课订单号
    #     self.fan_99order = sample_charge_res['data']['order_no']
    #     # 好友购买呱美课
    #     fan_user_token = self.fanUser.basic_auth
    #     fan_user_res = self.buy_lesson(token=fan_user_token, channel=channel, sp2xu_id=sp2xu_id,
    #                                    pay_price=pay_price,
    #                                    guadou_num=guadou_num, pay_total=pay_total)
    #     # 粉丝正价课订单号
    #     self.fan_normal_order = fan_user_res['data']['order_no']
    #     time.sleep(3)
    #     new_promoter = self.promoterQuery.get_promoter_accounts(mobile=self.user.user_mobile)  # 判断是否自动注册成推广人了
    #     self.promoter_id = new_promoter['_id']
    #     # 退款，还原测试数据
    #     self.fan_99mock_response = self.mock.api_refund_mock(chargeid=sample_charge_res['data']['id'])
    #
    #     assert new_promoter
    #     assert new_promoter['state'] == 'inactive'

    @pytest.mark.parametrize("type,sp2xu_id, pay_price, guadou_num, channel, pay_total",
                             [("promoter", "3063", 0, 12800, "wx_pub", 0), ("fan", "3063", 0, 12800, "wx_pub", 0)])
    def test_buy_6weeks_course_not_create_promoter(self, type, sp2xu_id, pay_price, guadou_num, channel, pay_total):
        """15460000060 推广人账号，15460000062是粉丝账号，已经锁粉成功，预备推广人购买双月课，或者粉丝购买双月课不创建账号
        推广人先买了思维正价课，再购买英语双月课
        """
        if type == 'promoter':
            # 推广人用户购买双月课
            user_token = self.user_6weeks.basic_auth
        else:
            # 粉丝购买双月课
            user_token = self.fanUser_6weeks.basic_auth
        user_res = self.buy_lesson(token=user_token, channel=channel, sp2xu_id=sp2xu_id, pay_price=pay_price,
                                   guadou_num=guadou_num, pay_total=pay_total)
        # 推广人正价课订单号
        self.oid.append(user_res["data"]["order_no"])
        new_promoter = self.promoterQuery.get_promoter_accounts(mobile=self.user_6weeks.user_mobile)  # 判断是否自动注册成推广人了
        assert new_promoter == None

    @pytest.mark.parametrize("sp2xu_id, pay_price, guadou_num, channel, pay_total",
                             [("3063", 0, 12800, "wx_pub", 0)])
    def test_buy_6weeks_course_no_commision(self, sp2xu_id, pay_price, guadou_num, channel, pay_total):
        """15460000060 推广人账号，15460000062是粉丝账号，已经锁粉成功，粉丝购买正价课不算业绩不分佣金
        """
        # 粉丝先购买思维正价课创建账号
        fan_token = self.fanUser_6weeks.basic_auth
        fan_res = self.buy_lesson(token=fan_token, channel=channel, sp2xu_id='928', pay_price=0,
                                  guadou_num=329900, pay_total=0)
        self.oid.append(fan_res["data"]["order_no"])
        time.sleep(3)
        create_promoter = self.promoterQuery.get_promoter_accounts(mobile=self.user_6weeks.user_mobile)
        self.promoter_id=create_promoter['_id']
        old_Total_Amount = create_promoter['totalAmount']
        # 粉丝购买双月课
        user_token = self.fanUser_6weeks.basic_auth
        user_res = self.buy_lesson(token=user_token, channel=channel, sp2xu_id=sp2xu_id, pay_price=pay_price,
                                   guadou_num=guadou_num, pay_total=pay_total)
        # 推广人正价课订单号
        user_order=user_res["data"]["order_no"]
        self.oid.append(user_order)
        new_promoter = self.promoterQuery.get_promoter_accounts(mobile=self.user_6weeks.user_mobile)  #获取推广人业绩
        commision = self.promoterQuery.get_promoter_order(_id=user_order)
        #对比业绩是否增加，是否分拥
        assert new_promoter['totalAmount'] == old_Total_Amount
        for x in commision:
            assert None == x

    @pytest.mark.parametrize("sp2xu_id, pay_price, guadou_num, channel, pay_total",
                             [("3063", 0, 12800, "wx_pub", 0)])
    def test_buy_6weeks_course_no_promoter_commision(self, sp2xu_id, pay_price, guadou_num, channel, pay_total):
        """15460000060 推广人账号，15460000062是粉丝账号，已经锁粉成功，推广人扩科购买正价课不算业绩不返现
        """
        # 粉丝先购买思维正价课创建账号
        fan_token = self.fanUser_6weeks.basic_auth
        fan_res = self.buy_lesson(token=fan_token, channel=channel, sp2xu_id='928', pay_price=0,
                                  guadou_num=329900, pay_total=0)
        self.oid.append(fan_res["data"]["order_no"])
        time.sleep(3)
        create_promoter = self.promoterQuery.get_promoter_accounts(mobile=self.user_6weeks.user_mobile)
        self.promoter_id = create_promoter['_id']
        old_Total_Amount = create_promoter['totalAmount']
        # 推广人购买双月课
        user_token = self.user_6weeks.basic_auth
        user_res = self.buy_lesson(token=user_token, channel=channel, sp2xu_id=sp2xu_id, pay_price=pay_price,
                                   guadou_num=guadou_num, pay_total=pay_total)
        # 推广人正价课订单号
        six_weeks_order=user_res["data"]["order_no"]
        self.oid.append(six_weeks_order)
        new_promoter = self.promoterQuery.get_promoter_accounts(mobile=self.user_6weeks.user_mobile)  # 获取推广人业绩
        #获取推广人返现记录
        commision = self.promoterQuery.get_promoter_own_order(_id=six_weeks_order)
        # 对比业绩是否增加，是否分拥
        assert new_promoter['totalAmount'] == old_Total_Amount
        for x in commision:
            assert None == x

    @pytest.mark.parametrize("mobile", ["15460000019"])
    def test_promoter_register_fail1(self, mobile):
        """
        注册推广人需满足两个条件：
        1.自己已购买呱美课（呱呱美语课Lv0-Lv6任一产品）
        2.自己通过邀请好友购买9.9订单锁粉，且锁粉好友中至少1人已购买呱美课
        测试未购买呱美课（两个条件均未满足）
        """
        res_universal = self.promoterLogin_universal.api_promoter_login(mobile)
        assert res_universal["code"] == 42222
        assert res_universal["msg"] == "仅限呱呱美语课用户注册"

    @pytest.mark.parametrize("sp2xu_id, pay_price, guadou_num, channel, pay_total", [("951", 0, 1200, "wx_pub", 0)])
    def test_promoter_register_fail2(self, sp2xu_id, pay_price, guadou_num, channel, pay_total):
        """
        注册推广人需满足两个条件：
        1.自己已购买呱美课（呱呱美语课Lv0-Lv6任一产品）
        2.自己通过邀请好友购买9.9订单锁粉，且锁粉好友中至少1人已购买呱美课
        购买呱美课没有粉丝（满足条件1未满足条件2）的账号注册推广人失败
        """
        # 构造用户自己先购买了呱美课
        token = self.universal_promoterUser.basic_auth
        order = ApiNewOrders(token)
        create_order = order.api_order_create(sp2xuId=sp2xu_id, payPrice=pay_price, guaDouNum=guadou_num)
        charge_res = order.api_charge_create(oid=create_order['data']['orderNo'], channel=channel, payTotal=pay_total,
                                             guadouDiscount=guadou_num)
        time.sleep(1)
        res_universal = self.promoterLogin_universal.api_promoter_login(self.universal_promoterUser.user_mobile)
        self.pro_refund.api_refund(charge_res['data']['order_no'])
        assert res_universal["code"] == 44444
        assert res_universal["msg"] == "仅限推荐的好友已购呱呱美语课的用户注册"
