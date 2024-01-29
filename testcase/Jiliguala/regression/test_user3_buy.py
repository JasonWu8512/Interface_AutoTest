# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2023/11/23 2:29 下午
@Author   : Anna
@File     : test_user3_buy.py
"""
import base64
import os
import time

import pytest
import pytest_check as check

from business.Jiliguala.lesson.ApiPaid import ApiPaid
from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.Jiliguala.onboarding.ApiUseronboarding import ApiUseronboarding
from business.Jiliguala.pay.ApiShoppingTab import ApiShoppingTab
from business.Jiliguala.pay.ApiTrialClass import ApiTrialClass
from business.Jiliguala.pay.ApiXx import ApiXx
from business.Jiliguala.systemlesson.ApiHome import ApiHome
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.userbiz.ApiUserCenter import ApiUserCenter
from business.Trade.tradeOrder.ApiOrderApi import ApiOrderApi
from business.businessQuery import usersQuery, pingxxorderQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


class TestUserBuy(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # # 【代码提交用】获取环境变量
        cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        print(env)
        # 本地调试用，获取环境变量
        # cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化ApiSmsInfo类，用户登录调用
        cls.mobile = cls.config['regression']['mobile02']
        cls.user = UserProperty(cls.mobile)
        cls.pwd = cls.config['regression']['pwd']
        # bid
        cls.bid = cls.config['regression']['bid02']
        # 获取用户token信息
        cls.token = cls.user.basic_auth
        print(cls.token)
        # 实例化ApiSmsInfo类
        cls.sms = ApiSmsInfo(cls.token)
        # 实例化首页
        cls.home = ApiHome(cls.token)
        # 实例化购买TAB
        cls.version = cls.config['version']['ver11.17.0']
        cls.agent = cls.config['User-Agent']['ios_11.17.0']
        cls.shoppingTab = ApiShoppingTab(cls.token, cls.version, cls.agent)
        # 实例化购买相关
        cls.super = ApiSuper(cls.token, cls.agent)
        # 3.0大包itemid
        cls.itemId = cls.config['regression']['itemId02']
        # 是否有实体
        cls.physical = cls.config['regression']['physical']
        # 购买方式
        cls.channel = cls.config['regression']['channel']
        # 课程级别
        cls.level = cls.config['regression']['level02']
        # xApp(首页请求需要)
        cls.xApp = cls.config['home']['x-app-params']

    """
    步骤：
    1.用户密码登录
    2.进入期外大包（需要填地址），课程详情页
    3.点击立即购买
    4.购买大包
    5.通过我的学习内容，选择K1
   
    返回：
    1.登录成功
    2.课程详情页，展示大包课相关信息
    3.支付浮层，金额展示正确
    3.大包课购买成功
       -我的学习内容，展示大包课
    4.首页展示大包课，正常展示开课时间
    """

    def test_user(self):
        """用户购买3.0大包课"""
        user_login = self.sms.api_get_password(u=self.mobile, typ='mobile', p=self.pwd)
        bid = user_login['data']['b'][0]['_id']
        uid = user_login['data']['b'][0]['prt']
        tok = user_login['data']['tok']
        mobile = user_login['data']['mobile']
        print(tok)
        print(bid)
        print(uid)
        print(user_login)
        # 用户token信息
        code = base64.b64encode(f'{uid}:{tok}'.encode('utf-8'))
        auth01 = 'Basic ' + str(code, encoding="utf-8")
        # 断言登录成功
        assert user_login['data']['mobile'] == self.mobile
        # 进入购买详情页
        lesson_buy = self.super.api_get_lessonbuy('shopping_tab', self.itemId)
        # 断言购买详情页，展示大包课相关信息
        print(lesson_buy)
        itemId01 = lesson_buy['data']['display_items'][0]['_id']
        print(itemId01)
        print(self.itemId)
        assert itemId01 == self.itemId
        # 获取商品价格
        sweetAmount = lesson_buy['data']['display_items'][0]['sweetAmount']
        print(sweetAmount)
        # sgu信息
        sgu = lesson_buy['data']['display_items'][0]['_id']
        print(sgu)
        # 点击立即购买，调起支付浮层
        payDetail = self.super.api_get_paydetail(sgu)
        # 断言浮层展示课程金额无误
        assert payDetail['data']['sweetAmount'] == sweetAmount

        # # 优惠信息
        # couponId = payDetail['data']['discounts'][0]['couponid']
        # 购买大包课
        order01 = self.super.api_post_purchase(bid=bid, itemid=sgu, physical=self.physical, channel=self.channel)
        print(order01)
        id = order01['data']['id']
        time_paid = order01['data']['created']
        order_no = order01['data']['order_no']
        current_timestamp = int(time.time() * 1000)
        transaction_no = 'MOCK4200001986' + str(current_timestamp)
        buy = self.super.api_post_mock(id=id, time_paid=time_paid, order_no=order_no, transaction_no=transaction_no)
        # 查询订单状态为paid的订单
        order = pingxxorderQuery().get_pingxxorder(uid=uid, status='paid', itemid=self.itemId)['_id']
        # 断言数据库正常生成，且与下单订单id一致
        assert order_no == order
        self.super.api_get_order(order_no)
        self.super.api_post_result(order_no)

        """点击订单物流，可以看到订单列表，展示大包课订单"""
        self.order = ApiOrderApi(auth01)
        indent = self.order.api_order_myorder()
        print(indent['data'][0]['detailList'][0]['commodityNo'])

        # 断言订单物流正确展示了大包课订单
        assert indent['data'][00]['detailList'][0]['commodityNo'] == sgu
        """点击订单物流，可以看到订单详情，展示大包课"""
        order_detail = self.order.api_order_detail(order_no)
        # 断言详情页订单id无误
        assert order_detail['data']['orderNo'] == order_no
        # 断言详情页展示正价课信息
        assert order_detail['data']['detailList'][0]['commodityNo'] == sgu

        """点击我的学习内容，展示大包信息"""
        self.paid = ApiPaid(auth01, self.version, self.agent)
        paid = self.paid.api_get_lesson_paid_v2(bid)
        # 断言，我的学习内容处展示大包课信息
        assert paid['data'][0]['data'][0]['details'][0]['type'] == 'GuaAdvancedClass'
        assert paid['data'][0]['data'][0]['details'][0]['subTitle'] == '已拥有8个级别：T1、T2、K1、K2、K3、K4、K5、K6'

        """通过我的学习内容，选择大包课"""
        home = ApiHome(auth01, version=self.agent, xApp=self.xApp).api_get_v4_home(bid)
        print(home)
        # 断言展示
        weekTitle = home['data']['roadmap']['elements'][1]['weekTitle']
        print(weekTitle)
        assert '共 24 周' in weekTitle

        # 还原数据
        refund = self.super.api_post_refund(order_no)
        print(refund)
        # 断言数据库里订单状态=refund
        refund = pingxxorderQuery().get_pingxxorder(_id=order_no)['status']
