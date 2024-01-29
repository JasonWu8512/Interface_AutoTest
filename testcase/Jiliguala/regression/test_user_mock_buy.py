# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2023/11/02 2:29 下午
@Author   : Anna
@File     : test_user_mock_buy.py
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



class TestUserMBuy(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        # env = os.environ.get('env')
        # # 【代码提交用】获取环境变量
        # cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        # print(env)
        # 本地调试用，获取环境变量
        # cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化ApiSmsInfo类，用户登录调用
        cls.mobile = cls.config['regression']['mobile']
        cls.pwd = cls.config['regression']['pwd']
        cls.user = UserProperty(cls.mobile)
        # bid
        cls.bid = cls.config['regression']['bid']
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
        # 四周课itemid
        cls.itemId = cls.config['regression']['itemId']
        # 是否有实体
        cls.physical = cls.config['regression']['physical']
        # 购买方式
        cls.channel = cls.config['regression']['channel']
        # 课程级别
        cls.level = cls.config['regression']['level']
        # xApp(首页请求需要)
        cls.xApp = cls.config['home']['x-app-params']


    """
    步骤：
   1.用户密码登录
   2.用户已经买了体验课且过期了，进入购买tab
   3.进入四周课，课程详情页
   4.点击立即购买
   5.购买四周课
   6.通过我的学习内容，选择四周课
   
    返回：
    1.登录成功
    2.购买tab，推荐四周课
    3.购买详情页，展示双月课相关信息
    4.支付浮层，金额展示正确
    5.双月课购买成功
      -我的学习内容，展示四周课
    6.首页展示双月课，正常展示开课时间
    """

    def test_user(self):
        """用户购买正价课"""
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
        # 进入购买tab
        shopping_tab = self.shoppingTab.api_get_shopping_tab(self.bid)
        print(shopping_tab)
        itemId = shopping_tab['data']['lessonList'][0]['lessonDetails'][0]['itemId']
        print(self.itemId)
        # 断言购买tab，推荐四周课
        assert itemId == self.itemId
        # 进入购买详情页
        lesson_buy = self.super.api_get_lessonbuy('shopping_tab', itemId)
        # 断言购买详情页，展示四周课相关信息
        print(lesson_buy)
        itemId01 = lesson_buy['data']['extendMap']['spuId']
        print(itemId01)
        print(self.itemId)
        assert lesson_buy['data']['extendMap']['spuId'] == self.itemId
        # 获取商品价格
        sweetAmount = lesson_buy['data']['display_items'][0]['sweetAmount']
        print(sweetAmount)
        # 会场相关信息
        extendMap = lesson_buy['data']['extendMap']
        print(extendMap)

        # 优惠券信息
        couponTypActivity = lesson_buy['data']['couponTypActivity']
        # sgu信息
        sgu = lesson_buy['data']['display_items'][0]['_id']
        print(sgu)
        # 点击立即购买，调起支付浮层
        payDetail = self.super.api_get_paydetail(sgu, couponTypActivity)
        # 断言浮层展示课程金额无误
        assert payDetail['data']['sweetAmount'] == sweetAmount

        # 优惠信息
        couponId = payDetail['data']['discounts'][0]['couponid']
        # 购买四周课
        order01 = self.super.api_post_purchase(bid=bid, itemid=sgu, physical=self.physical, channel=self.channel,
                                               couponid=couponId)
        print(order01)
        id = order01['data']['id']
        time_paid = order01['data']['created']
        order_no = order01['data']['order_no']
        current_timestamp = int(time.time() * 1000)
        transaction_no = 'MOCK4200001986' + str(current_timestamp)
        buy = self.super.api_post_mock(id=id, time_paid=time_paid, order_no=order_no, transaction_no=transaction_no)
        # 查询订单状态为paid的订单
        order = pingxxorderQuery().get_pingxxorder(uid=uid, status='paid', itemid='S1GE_W1_4_SGU_new')['_id']
        # 断言数据库正常生成，且与下单订单id一致
        assert order_no == order
        self.super.api_get_order(order_no)
        self.super.api_post_result(order_no)

        """点击订单物流，可以看到订单列表，展示88四周课订单"""
        self.order = ApiOrderApi(auth01)
        indent = self.order.api_order_myorder()
        print(indent['data'][0]['detailList'][0]['commodityNo'])

        # 断言订单物流正确展示了英语体验课订单
        assert indent['data'][00]['detailList'][0]['commodityNo'] == sgu
        """点击订单物流，可以看到订单详情，展示四周课"""
        order_detail = self.order.api_order_detail(order_no)
        # 断言详情页订单id无误
        assert order_detail['data']['orderNo'] == order_no
        # 断言详情页展示正价课信息
        assert order_detail['data']['detailList'][0]['commodityNo'] == sgu

        """点击我的学习内容，展示四周课信息"""
        self.paid = ApiPaid(auth01, self.version, self.agent)
        paid = self.paid.api_get_lesson_paid_v2(bid)
        # 断言，我的学习内容处展示四周课信息
        assert paid['data'][0]['data'][0]['details'][0]['type'] == 'GuaAdvancedClass'
        assert paid['data'][0]['data'][0]['details'][0]['subTitle'] == '已拥有1个级别：K1'

        """通过我的学习内容，选择四周课"""
        home = ApiHome(auth01, version=self.agent, xApp=self.xApp).api_get_v4_home(bid)
        print(home)
        # 断言展示仅拥有4周字样
        weekTitle = home['data']['roadmap']['elements'][1]['weekTitle']
        assert weekTitle == '第 1 周 / 共 24 周（仅拥有4周）'

        # 还原数据
        refund = self.super.api_post_refund(order_no)
        print(refund)
        # 断言数据库里订单状态=refund
        refund = pingxxorderQuery().get_pingxxorder(_id=order_no)['status']
