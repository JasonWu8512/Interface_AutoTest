# -*- coding: utf-8 -*-
# @Time : 2022/7/18 1:26 下午
# @Author : anna
from time import sleep

import pytest

from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.Jiliguala.pay.ApiTrialClass import ApiTrialClass
from business.Jiliguala.pay.ApiXx import ApiXx
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.userbiz.ApiAddress import ApiAddress
from business.businessQuery import usersQuery, pingxxorderQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from testcase.Jiliguala.userbiz.test_address import TestAddress


@pytest.mark.ShoppingTab
class TestSuper(object):
    """
    购买流程
    """
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path(env="fat")
        cls.dm.set_domain(cls.config['url'])
        cls.agent = cls.config['agent']['ios_11.12.3']
        cls.guadou = UserProperty(cls.config['order']['guadou'])  # 纯瓜豆账号
        cls.discount = UserProperty(cls.config['order']['discount'])  # 券+自然拼读+瓜豆账号
        cls.second_discount = UserProperty(cls.config['order']['second_discount'])  # 正价课第二科折扣账号
        cls.bag = UserProperty(cls.config['order']['bag'])  # 大包账号
        cls.ggr = UserProperty(cls.config['order']['ggr_user'])  # 呱呱阅读趣味拓展课程

        # 券+自然拼读+瓜豆账号，初始化
        cls.mixdis_pay = ApiSuper(cls.discount.basic_auth, cls.agent)
        # 纯瓜豆，初始化
        cls.guadou_pay = ApiSuper(cls.guadou.basic_auth, cls.agent)
        # 正价课第二科折扣，初始化
        cls.second_discount_pay = ApiSuper(cls.second_discount.basic_auth, cls.agent)
        # 大包账号，初始化
        cls.bag_pay = ApiSuper(cls.bag.basic_auth, cls.agent)
        # 趣味拓展，初始化
        cls.ggr_pay = ApiSuper(cls.ggr.basic_auth, cls.agent)
        # 获取用户的第一个bid
        cls.gd_bid = cls.guadou.babies["_id"]
        cls.discount_bid = cls.discount.babies["_id"]
        cls.second_discount_bid = cls.second_discount.babies["_id"]
        cls.bag_bid = cls.second_discount.babies["_id"]
        cls.ggr_bid = cls.ggr.babies["_id"]

        # 是否实体
        cls.physical = 'false'
        # 支付渠道
        cls.channel = 'guadou'
        # 生成随机账号
        cls.user = ApiUser()

    def test_guaDou(self):
        """纯瓜豆抵扣(2.5课程购买)：支付收银台展示、支付流程"""
        itemId = 'K4GE'
        res = self.guadou_pay.api_get_paydetail(itemId)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言商品价格=折扣价格
        assert res['data']['sweetAmount'] == res['data']['discounts'][0]["amount"]
        # 断言，纯瓜豆抵扣，支付金额=0
        assert res['data']['payAmount'] == 0

        # 客户端请求下单接口
        res01 = self.guadou_pay.api_post_purchase(self.gd_bid, itemId, self.physical, self.channel)
        print(res01)
        # 断言接口返回成功
        assert res01['code'] == 0
        # 断言支付成功
        assert res01['data']['status'] == 'paid'
        oid = res01['data']['oid']
        # 订单查询
        res02 = self.guadou_pay.api_get_order(oid)
        # print(res02)
        # 断言接口查询支付状态正常
        assert res01['data']['status'] == 'paid'
        # 返回支付结果
        res03 = self.guadou_pay.api_post_result(oid)
        # print(res03)
        # 断言接口返回成功
        assert res03['code'] == 0
        # 调用退款接口，还原数据
        self.guadou_pay.api_post_refund(oid)

    def test_second_discount(self):
        """有第二科折扣时（2.5课程购买），支付流程"""
        itemId = 'K4GE'
        # 测试支付收银台接口
        res = self.second_discount_pay.api_get_paydetail(itemId)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言，接口返回itemid和请求一致
        assert res['data']['skuId'] == itemId
        # 断言返回第二科折扣字段
        assert res['data']['discounts'][0]['ttl'] == '购第二科优惠抵扣'
        # 断言折扣金额=商品价格
        assert res['data']['sweetAmount'] == res['data']['discounts'][0]['amount'] + res['data']['discounts'][1][
            'amount']

        # 获取瓜豆抵扣金额
        gua_pay = res['data']['discounts'][1]['amount']
        # 获取支付前用户瓜豆金额
        gua_pre = usersQuery().get_users(mobile=self.config['order']['second_discount'])["guadouBalance"]
        print(gua_pre)
        # 测试客户端下单接口
        res01 = self.second_discount_pay.api_post_purchase(self.second_discount_bid, itemId, self.physical,
                                                           self.channel)
        print(res01)
        # 断言支付成功
        assert res01['data']['status'] == 'paid'
        # 获取支付后用户瓜豆金额
        gua_after = usersQuery().get_users(mobile=self.config['order']['second_discount'])["guadouBalance"]
        print(gua_after)
        # 断言支付前瓜豆金额-瓜豆抵扣金额=支付后瓜豆金额
        assert gua_after == gua_pre - gua_pay
        oid = res01['data']['oid']

        # 测试订单查询接口
        res02 = self.second_discount_pay.api_get_order(oid)
        assert res02['data']['status'] == 'paid'
        # 测试客户端返回结果接口
        res03 = self.second_discount_pay.api_post_result(oid)
        assert res03['code'] == 0
        # 还原数据
        self.second_discount_pay.api_post_refund(oid)

    def test_mix_discount(self):
        """有优惠券+自然拼读抵扣+瓜豆折扣时（1.5课程购买），支付流程"""
        itemId = 'L4XX_L5XX'
        couponTyp = "SLB1002"
        # 先领取优惠券
        res00 = self.mixdis_pay.api_post_coupon(itemId, couponTyp)
        print(res00)
        couponId = res00['data']['couponId']
        print(couponId)
        # 测试支付收银台接口
        res = self.mixdis_pay.api_get_paydetail(itemId)
        print(res)
        # 断言接口返回成功
        assert res['code'] == 0
        # 断言，接口返回itemid和请求一致
        assert res['data']['skuId'] == itemId
        # 断言返回'自然拼读课程抵扣'
        assert res['data']['discounts'][0]['ttl'] == '自然拼读课程抵扣'
        # 断言返回'优惠券抵扣'
        assert res['data']['discounts'][1]['ttl'] == '优惠券抵扣'
        # 断言返回'呱豆抵扣'
        assert res['data']['discounts'][2]['ttl'] == '呱豆抵扣'

        # 断言折扣金额=商品价格
        assert res['data']['sweetAmount'] == res['data']['discounts'][0]['amount'] + res['data']['discounts'][1][
            'amount'] + res['data']['discounts'][2]['amount']
        # 获取瓜豆抵扣金额
        gua_pay = res['data']['discounts'][2]['amount']
        # 获取支付前用户瓜豆金额
        gua_pre = usersQuery().get_users(mobile=self.config['order']['discount'])["guadouBalance"]
        print("支付前金额", gua_pre)
        print("商品金额", res['data']['sweetAmount'])
        print("自然拼读金额", res['data']['discounts'][0]['amount'])
        print("优惠券金额", res['data']['discounts'][1]['amount'])
        print("呱豆抵扣金额", res['data']['discounts'][2]['amount'])
        # 测试客户端下单接口
        res01 = self.mixdis_pay.api_post_purchase01(self.discount_bid, itemId, self.physical,
                                                    self.channel, couponId)
        print(res01)
        # 断言支付成功
        assert res01['data']['status'] == 'paid'
        # 获取支付后用户瓜豆金额
        gua_after = usersQuery().get_users(mobile=self.config['order']['discount'])["guadouBalance"]
        print("支付后金额", gua_after)
        # 断言支付前瓜豆金额-瓜豆抵扣金额=支付后瓜豆金额
        assert gua_after == gua_pre - gua_pay
        oid = res01['data']['oid']

        # 测试订单查询接口
        res02 = self.mixdis_pay.api_get_order(oid)
        assert res02['data']['status'] == 'paid'
        # 测试客户端返回结果接口
        res03 = self.mixdis_pay.api_post_result(oid)
        assert res03['code'] == 0
        # 还原数据
        self.second_discount_pay.api_post_refund(oid)

    def test_second_triDiscount(self):
        """
        体验课第二科折扣，购买流程
        前提：
        因体验课只能买一次，所以先随机生成账号
        1.新购买英语体验课，确认购买成功
        2.再检查思维体验课收银台，有第二科折扣
        """
        # 先购买英语体验课
        itemId = 'L1TC'
        # 生成随机用户
        mobile = self.user.get_mobile()
        print(mobile)
        # 注册新账号
        newUser = self.user.api_register(mobile)
        # 体验课账号信息
        trial_user = UserProperty(mobile)
        # 获取用户token信息
        token = trial_user.basic_auth
        user_id = trial_user.user_id
        # 充瓜豆
        usersQuery().update_users_guadouBalance(uid=user_id, guadouBalance=90000000)
        # 体验课信息授权，实例化类
        trial_pay = ApiSuper(trial_user.basic_auth, agent=self.agent)
        # 获取新用户bid
        trial_bid = trial_user.babies["_id"]
        res04 = trial_pay.api_post_purchase(trial_bid, itemId, "true", "guadou")
        oid = res04['data']['oid']
        # 查询生成体验课购买订单
        order = pingxxorderQuery().get_pingxxorder(uid=trial_user.user_id)['_id']
        # oid=order['_id']
        # 断言思维体验课购买成功
        assert res04['data']['oid'] == order
        trial_pay.api_get_order(oid)
        trial_pay.api_post_result(oid)
        sleep(10)
        # 测试正常添加班主任
        resp = ApiTrialClass(token).api_get_tc_paid(trial_bid, itemId)
        # 断言接口请求成功
        assert resp['code'] == 0
        # 断言接口返回班主任相关内容
        assert resp['data']['view'] == 'tutor'
        # 测试支付收银台，展示第二科折扣内容
        # 再次进入思维体验课收银台
        itemId01 = 'K1MATC_99'
        res05 = trial_pay.api_get_paydetail(itemId01)
        print(res05)
        # 断言有第二科折扣内容
        assert res05['data']['discounts'][0]['ttl'] == "购第二科优惠抵扣"
        # 断言商品金额=商品金额+折扣金额
        assert res05['data']['sweetAmount'] == res05['data']['discounts'][0]['amount'] + res05['data']['discounts'][1][
            'amount']

        # 测试购买大包
        # 先购买英语体验课
        itemId = 'F1_S1-6_WITHOUTDISCOUNT'
        # itemId = 'F2GE_W7-24_S1_S6'
        user = ApiUser()
        version = self.agent
        level = 'K1GE'
        address = ApiAddress(token, version).api_put_address("test", "12790909090", "北京市 北京市 东城区", '测试地址测试地址')
        # sleep(10)
        res06 = trial_pay.api_post_purchase(trial_bid, itemId, 'true', 'guadou')

        print(res06)
        assert res06['data']['status'] == 'paid'
        sleep(10)

        # 测试首购后，跳转规划师页面
        res07 = ApiXx(token, version).api_get_xx_paid(trial_bid, itemId, level)
        print(res07)
        assert res07['code'] == 0
        # 断言有添加规划师相关的内容
        assert res07['data']['miniapp_url'] == "jlgl://toast?msg=安装微信后才能添加规划师哦~"

    def test_bag_fail(self):
        """
        购买大包，未填写地址，购买失败
        """
        # 先购买英语体验课
        itemId = 'F1_S1-6_WITHOUTDISCOUNT'

        res06 = self.bag_pay.api_post_purchase(self.bag_bid, itemId, 'true', 'guadou')
        print(res06)
        # 断言购买大包，必须填写地址
        assert res06['msg'] == '地址不能为空'

    def test_ggr(self):
        """
        呱呱阅读购买成功
        """
        itemid = 'GGRVIP_1YearPurchase_01_SGU'
        res07 = self.ggr_pay.api_post_purchase(self.ggr_bid, itemid, 'true', 'guadou')
        print(res07)
        # 断言呱呱阅读购买成功
        assert res07['data']['status'] == 'paid'
        # 还原数据
        oid = res07['data']['oid']
        self.ggr_pay.api_post_refund(oid)

    def test_expand(self):
        """
        趣味拓展购买成功
        """
        itemid = 'AlbumCIX001'
        res07 = self.ggr_pay.api_post_purchase(self.ggr_bid, itemid, 'false', 'guadou')
        print(res07)
        # 趣味拓展购买成功
        assert res07['data']['status'] == 'paid'
        # 还原数据
        oid = res07['data']['oid']
        self.ggr_pay.api_post_refund(oid)

    def test_gx(self):
        """
        国学素养购买成功
        """
        itemid = 'A1GX_SGU'
        res08 = self.ggr_pay.api_post_purchase(self.ggr_bid, itemid, 'false', 'guadou')
        print(res08)
        # 趣味拓展购买成功
        assert res08['data']['status'] == 'paid'
        # 还原数据
        oid = res08['data']['oid']
        self.ggr_pay.api_post_refund(oid)

    def test_bk(self):
        """
        百科购买成功
        """
        itemid = 'B1GX_SGU'
        res09 = self.ggr_pay.api_post_purchase(self.ggr_bid, itemid, 'false', 'guadou')
        print(res09)
        # 趣味拓展购买成功
        assert res09['data']['status'] == 'paid'
        # 还原数据
        oid = res09['data']['oid']
        self.ggr_pay.api_post_refund(oid)
