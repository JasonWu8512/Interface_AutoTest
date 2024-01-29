# coding=utf-8
# @Time    : 2021/5/25 1:40 下午
# @Author  : Karen
# @File    : test_CreateOrder.py

import pytest

from business.Reading.trade.ApiCreateOrder import ApiCreateOrder
from business.Reading.trade.ApiPingpp import ApiPingpp
from business.Reading.trade.ApiPurchasePage import ApiPurchasePage
from business.Reading.user.ApiUser import ApiUser
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from testcase.Reading.trade import logout_mobile, logon_mobile


@pytest.mark.ggrTrade
class TestCreateOrder(object):
    ''' 下单 '''
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取fat环境配置
        cls.config = cls.dm.set_env_path()

        # 设置域名
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = ApiUser().get_guest_token()  # 创建游客并获取token
        cls.guest = ApiCreateOrder(token=cls.guest_token)  # 创建游客实例

        # 初始化不同身份用户
        cls.user = UserProperty(cls.config['reading_account']['user'])# 读取配置文件中的带订单号的用户
        cls.vip388_user = UserProperty(cls.config['reading_account']['vip388_user'])  # 读取配置文件中的年卡用户
        cls.vip488_user = UserProperty(cls.config['reading_account']['vip488_user'])  # 读取配置文件中的终身卡用户
        cls.no_vip_user = UserProperty(cls.config['reading_account']['no_vip_user'])  # 读取配置文件中的非vip用户

        # 实例不同身份对象
        cls.user = ApiCreateOrder(token=cls.user.basic_auth)
        cls.vip388_user = ApiCreateOrder(token=cls.vip388_user.basic_auth)
        cls.vip488_user = ApiCreateOrder(token=cls.vip488_user.basic_auth)
        #cls.no_vip_user = ApiCreateOrder(token=cls.no_vip_user.basic_auth)

        # 读取配置文件中的测试手机号：13888888883
        cls.mobile = cls.config['reading_account']['no_vip_user']

        # 如果手机账号存在则先注销，再重新注册。确保账号是干净的
        cls.u = ApiUser()
        if cls.u.get_jlgl_user(cls.mobile)!= None:
            #注销
            logout_mobile(cls.mobile)

        #重新注册
        cls.token = logon_mobile(cls.mobile, cls.config['ggheader_v2'])
        cls.no_vip_user = ApiCreateOrder(token=cls.token)

        order_user = UserProperty(cls.config['reading_account']['no_vip_user'])
        resp = ApiPurchasePage(token=order_user.basic_auth).api_v2_vip_purchase()
        spu = resp['data']['spuUIElement']['commodityNo']
        print('spu是', spu)
        cls.year_sgu = resp['data']['items'][0]['itemId']
        cls.life_sgu = resp['data']['items'][1]['itemId']
        print('年卡sgu是:', cls.year_sgu)
        print('终身卡sgu是:', cls.life_sgu)

    def test_create_vip388_order(self):
        ''' 01) 非vip用户创建年卡订单，不涉及支付'''
        resp = self.no_vip_user.api_create_order(self.year_sgu)
        print(resp)
        print('订单号:',resp['data']['oid'])
        assert resp['code'] == 0
        assert resp['data']['oid'] != None

    def test_create_vip488_order(self):
        ''' 02) 非vip用户创建终身卡订单，不涉及支付'''
        resp = self.no_vip_user.api_create_order(self.life_sgu)
        print(resp)
        print('订单号:',resp['data']['oid'])
        assert resp['code'] == 0
        assert resp['data']['oid'] != None

    def test_guest_create_vip488_order(self):
        ''' 03) 游客创建终身卡订单，不涉及支付'''
        resp = self.guest.api_create_order(self.life_sgu)
        print('返回数据:',resp)
        print('订单号:',resp['data']['oid'])
        assert resp['code'] == 0
        assert resp['data']['oid'] != None

    def test_create_LexileTest_order(self):
        ''' 04) 年卡vip用户创建蓝思测试订单，不涉及支付'''
        # resp = self.vip388_user.api_create_order('LexileTestOnce')
        # print(resp)
        # print('订单号:',resp['data']['oid'])
        # assert resp['code'] == 0
        # assert resp['data']['oid'] != None
        pass #蓝思测试已下线

    def test_order_charge(self):
        ''' 05) 非vip用户创建终身卡订单，并请求ping++'''
        resp = self.no_vip_user.api_order_charge(self.life_sgu,'wx')
        print('resp:', resp)
        oid = resp['data']['order_no']
        print('订单号:', oid)
        assert resp['code'] == 0
        assert resp['data']['order_no'] != None
        assert resp['data']['subject'] == '畅读VIP终身卡'

        #退款
        # no_vip_user = UserProperty(self.config['reading_account']['no_vip_user'])
        # refund = ApiPingpp(token=no_vip_user.basic_auth).api_pingpp_refund_callback(oid)
        # print('退款成功',refund)



    def test_order_pingpp_charge(self):
        ''' 06) 请求 pingpp ，创建 pingpp 的 charge 对象，站外支付时使用'''
        oid = self.no_vip_user.api_order_charge(self.life_sgu,'wx')['data']['order_no']
        resp = self.no_vip_user.api_order_pingpp_charge(oid,'wx')
        print('订单号:', oid)
        print('请求',resp)
        assert resp['code'] == 0
        assert resp['data']['order_no'] != None
        assert resp['data']['subject'] == '畅读VIP终身卡'
        assert resp['data']['object'] == 'charge'

        # 退款
        # no_vip_user = UserProperty(self.config['reading_account']['no_vip_user'])
        # refund = ApiPingpp(token=no_vip_user.basic_auth).api_pingpp_refund_callback(oid)


    def test_charge_paying(self):
        ''' 08) 支付完成后由客户端触发将订单变为 paying 状态'''
        oid = self.no_vip_user.api_order_charge(self.life_sgu,'wx')['data']['order_no']
        resp = self.no_vip_user.api_order_charge_paying(oid)
        print('订单号:', oid)
        print('请求',resp)

        # 退款
        # no_vip_user = UserProperty(self.config['reading_account']['no_vip_user'])
        # refund = ApiPingpp(token=no_vip_user.basic_auth).api_pingpp_refund_callback(oid)


    def test_order_status_notpaid(self):
        ''' 09) 订单状态：未支付'''
        order = self.no_vip_user.api_create_order(self.life_sgu)
        import time
        time.sleep(2)
        id = order['data']['oid'] #获取订单号
        resp = self.no_vip_user.api_get_order(id)
        print('订单号:',id)
        print('请求',resp)
        assert resp['code'] == 0
        assert resp['data']['status'] == 'notpaid'

    def test_order_status_paid(self):
        '''10) 订单状态：已支付'''
        resp = self.user.api_get_order('O61182206362312704')
        print('请求', resp)
        assert resp['code'] == 0
        assert resp['data']['status'] == 'paid'

    def test_order_status_refunded(self):
        '''11) 订单状态：已退款'''
        # 退款接口已作废，本条用例仅在fat环境执行
        if self.config['env'] == 'fat':
            resp = self.user.api_get_order('O60946347436941312')
            print('请求', resp)
            assert resp['code'] == 0
            assert resp['data']['status'] == 'refunded'
        else:
            print('非fat环境，不执行本条用例！')

    def test_order_status_needAddress(self):
        '''12) 订单状态：未填写地址'''
        # 退款接口已作废，本条用例仅在fat环境执行
        if self.config['env'] == 'fat':
            resp = self.user.api_get_order('O54311239949750272')
            print('请求', resp)
            assert resp['code'] == 0
            assert resp['data']['status'] == 'paid'
        else:
            print('非fat环境，不执行本条用例！')

    def test_ios_failed_text(self):
        ''' 13) iOS支付失败后发送短信'''
        resp = self.no_vip_user.api_order_ios_failed()
        print('请求', resp)
        assert resp['code'] == 0
        assert resp['data'] == {}
