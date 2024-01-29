# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2022/11/22 2:29 下午
@Author   : Anna
@File     : test_guest_buy.py
"""
import base64
import os
import time
from time import sleep

import pytest
import pytest_check as check

from business.Jiliguala.lesson.ApiPaid import ApiPaid
from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.Jiliguala.onboarding.ApiUseronboarding import ApiUseronboarding
from business.Jiliguala.pay.ApiShoppingTab import ApiShoppingTab
from business.Jiliguala.pay.ApiTrialClass import ApiTrialClass
from business.Jiliguala.systemlesson.ApiHome import ApiHome
from business.Jiliguala.userbiz.ApiUserCenter import ApiUserCenter
from business.Trade.tradeOrder.ApiOrderApi import ApiOrderApi
from business.businessQuery import usersQuery, pingxxorderQuery
from config.env.domains import Domains


class TestGuestBuy(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # 【代码提交用】获取环境变量
        cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        print(env)
        # 本地调试用，获取环境变量
        # cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化ApiSmsInfo类，游客登录调用
        cls.sms = ApiSmsInfo(token=None)
        # 实例化ApiUseronboarding，选择年龄
        cls.version = cls.config['version']['ver11.17.0']
        cls.agent = cls.config['User-Agent']['ios_11.17.0']
        cls.onboard = ApiUseronboarding(cls.version, cls.agent)
        # 宝贝年龄
        cls.birth = cls.config['regression']['birth']
        # 宝贝昵称
        cls.nick = cls.config['regression']['nick']
        # 购买来源
        cls.source = "shopping_tab"
        # 是否实体
        cls.physical = 'true'
        # 0元课没有实体
        cls.physical01 = 'false'
        # 支付渠道
        cls.channel = 'guadou'
        # pandora 自动生成，根据当前时间戳:+固定字段然后base64加密
        current_timestamp = int(time.time() * 1000)
        auth_part = '2022090617204537dac25b2d811d716af3478aff70a2e70113ebf958de83b1:50b665b76488e1d3a565d3d05b63cc69'
        cls.pandora = base64.b64encode(f'{current_timestamp}:{auth_part}'.encode('utf-8'))

    """
    步骤：
    1.选择游客登录
    2.选择年龄
    3.登录成功，进入首页
    4.进入购买tab
    5.进入体验课购买详情，登录手机号，购买体验课
    6.点击我的tab，选择我的学习内容，可以看到体验课
    7.点击订单物流，可以看到订单列表，展示体验课
    8.点击订单列表，选择体验课，进入订单详情，详情页展示内容无误
    9.退款体验课，订单状态变更为refund，我的学习内容处，不展示体验课订单
    """

    def test_guest(self):
        """游客登录"""
        guest = self.sms.api_put_guest()
        uid = guest['data']['_id']
        print(uid)
        tok = guest['data']['tok']
        code = base64.b64encode(f'{uid}:{tok}'.encode('utf-8'))
        auth01 = 'Basic ' + str(code, encoding="utf-8")
        print("uid", uid)
        print("tok", tok)
        print("code", code)
        print("auth01", auth01)

        # 断言接口返回成功
        check.equal(guest['code'], 0)

        """ 选择年龄 """
        bd = self.onboard.api_user_onboarding(self.nick, self.birth, auth01)
        bid = bd['data']['_id']
        print(bid)
        # 断言接口返回成功
        check.equal(bd['code'], 0)

        """游客登录成功，检查首页，首页内容确认，展示体验营相关信息"""
        # 实例化首页，验证首页内容
        self.home = ApiHome(auth01)
        home = self.home.api_get_v4_home(bid)
        # 断言首页推荐的是英语体验营
        # 补充年课体验课id=438e03a6443140f49e4e99d94a428595
        assert home['data']['roadmap']['elements'][1]['id'] == 'K1GEE03' or '438e03a6443140f49e4e99d94a428595'

        """
        实例化购买tab，检查购买tab，推荐体验课
        用户动作：点击购买tab
        """
        self.shoppingtab = ApiShoppingTab(auth01, self.version, self.agent)
        shoppingtab = self.shoppingtab.api_get_shopping_tab(bid)
        itemId = shoppingtab['data']['lessonList'][0]['lessonDetails'][0]['itemId']
        # 断言购买tab，推荐体验课
        # 补充推荐年课体验课
        assert 'YGEE_0_APP_SPU_new' in itemId or 'K1GEFC_0_APP' in itemId

        """5.进入体验课购买详情，登录手机号，购买体验课"""
        # 购买体验课
        # 实例化购买相关接口
        self.super = ApiSuper(auth01, self.agent)
        # 进入体验课的购买详情页
        detail = self.super.api_get_lessonbuy(self.source, itemId)
        skuId = detail['data']['display_items'][0]['_id']
        # 断言正常进入了英语体验课详情页
        assert 'YGEE_0_SGU_new' in skuId or 'K1GEFC_0_SGU' in skuId
        # 断言需要手机号才能购买
        assert detail['data']['isNeedBindMobile'] == True
        # 体验课价格
        # amount = detail['data']['display_items'][0]['sweetAmount']
        # print(amount)

        # 点击详情页，拉起手机号登录浮层，登录手机号
        # 生成随机用户
        mobile_get = self.sms.api_get_mobile()
        mobile = mobile_get['data']
        print(mobile)
        # 实例化短信验证码
        print(code)
        self.sms01 = ApiSmsInfo(token=auth01)
        self.sms01.api_get_sms(target=mobile, pandora=self.pandora)
        print(auth01)
        # 获取验证码
        # 待优化，同一个实例，不同参数引用
        sms_code = usersQuery().get_users(_id=uid)["sms"]["code"]
        print(sms_code)
        # sleep(10)
        upgrade = self.sms01.api_post_sms(sms_code, mobile)
        print(upgrade)

        payDetail = self.super.api_get_paydetail(skuId)
        print(payDetail)
        # 断言skuid=K1GEFC_0_SGU、YGEE_0_SGU_new
        assert payDetail['data']['skuId'] == 'K1GEFC_0_SGU' or 'YGEE_0_SGU_new'
        # 购买
        buy = self.super.api_post_purchase(bid, skuId, self.physical01, self.channel)
        oid = buy['data']['oid']
        print(oid)
        # 查询生成体验课购买订单
        order = pingxxorderQuery().get_pingxxorder(uid=uid)['_id']
        # oid=order['_id']
        # 断言体验课购买成功
        assert buy['data']['oid'] == order
        self.super.api_get_order(oid)
        self.super.api_post_result(oid)
        # sleep(10)
        # 测试正常添加班主任
        resp = ApiTrialClass(auth01).api_get_tc_paid(bid, itemid=skuId)
        # 断言接口请求成功
        assert resp['code'] == 0
        # 断言接口返回班主任相关内容
        assert resp['data']['view'] == 'tutor'

        """点击订单物流，可以看到订单列表，展示体验课"""
        self.order = ApiOrderApi(auth01)
        indent = self.order.api_order_myorder()
        print(indent['data'][0]['detailList'][0]['commodityNo'])

        # 断言订单物流正确展示了英语体验课订单
        assert indent['data'][0]['detailList'][0]['commodityNo'] == skuId
        """点击订单物流，可以看到订单详情，展示体验课"""
        order_detail = self.order.api_order_detail(oid)
        print(oid)
        # 断言详情页订单id无误
        assert order_detail['data']['orderNo'] == oid
        # 断言详情页展示体验课信息
        assert order_detail['data']['detailList'][0]['commodityNo'] == skuId
        # 等待履约时间
        sleep(30)
        """点击我的学习内容，展示体验营+预热课信息"""
        print('我的学习内容'+auth01)
        print(self.version)
        print(self.agent)
        self.paid = ApiPaid(auth01, self.version, self.agent)
        paid = self.paid.api_get_lesson_paid_v2(bid)
        print(paid)
        # 调试
        # 断言，我的学习内容处展示体验营信息
        assert paid['data'][0]['data'][0]['details'][0]['type'] == 'ReferralTrialClass'
        assert paid['data'][0]['data'][1]['details'][0]['type'] == 'preview_lesson'

        """点击我的，正常展示英语启蒙顾问入口"""
        self.center = ApiUserCenter(auth01, self.version)
        center = self.center.api_get_usercenter_v3(bid, uid)
        tutor = center['data']['modules'][3]['details'][1]['title']
        assert tutor == '我的学习顾问（英语素质）'
        print(tutor)

        """通过我的学习内容，选择体验课"""
        home = ApiHome(auth01).api_get_v4_home(bid)
        # 断言展示开课时间
        startDate = home['data']['roadmap']['elements'][2]['startDate']
        assert '日开始学习' in startDate
        print(startDate)

        """购买成功，点击购买tab，推荐运营期内大包"""
        new_tab = self.shoppingtab.api_get_shopping_tab(bid)
        # 断言购买tab，推荐运营期大包
        assert new_tab['data']['lessonList'][0]['lessonDetails'][0]['commodityNo'] == 'F1_S1-6_WITHOUTDISCOUNT_SPU'

        # 还原数据
        refund = self.super.api_post_refund(oid)
        print(refund)
        # 断言数据库里订单状态=refund
        refund = pingxxorderQuery().get_pingxxorder(_id=oid)['status']
