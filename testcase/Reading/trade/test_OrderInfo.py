# coding=utf-8
# @Time    : 2021/5/25 1:40 下午
# @Author  : Karen
# @File    : test_OrderInfo.py

import pytest
from business.common.UserProperty import UserProperty
from business.Reading.trade.ApiOrderInfo import ApiOrderInfo
from business.Reading.trade.ApiCreateOrder import ApiCreateOrder
from business.Reading.user.ApiUser import ApiUser
from business.Reading.vip.ApiVip import ApiVip
from business.Reading.trade.ApiPingpp import ApiPingpp
from business.Reading.trade.ApiPurchasePage import ApiPurchasePage
from config.env.domains import Domains
from testcase.Reading.trade import logout_mobile, logon_mobile


@pytest.mark.ggrTrade
class TestOrderInfo(object):
    ''' 订单信息相关 '''
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取fat环境配置
        cls.config = cls.dm.set_env_path()

        # 设置域名
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = ApiUser().get_guest_token()  # 创建游客并获取token
        cls.guest = ApiOrderInfo(token=cls.guest_token)  # 创建游客实例

        # 初始化不同身份用户
        cls.user = UserProperty(cls.config['reading_account']['user'])  # 读取配置文件中的带订单号的用户
        cls.vip388_user = UserProperty(cls.config['reading_account']['vip388_user']) # 读取配置文件中的年卡用户
        cls.vip488_user = UserProperty(cls.config['reading_account']['vip488_user']) # 读取配置文件中的终身卡用户
        #cls.no_vip_user = UserProperty(cls.config['reading_account']['no_vip_user']) # 读取配置文件中的非vip用户

        # 实例不同身份对象
        cls.user = ApiOrderInfo(token=cls.user.basic_auth)
        cls.vip388_user = ApiOrderInfo(token=cls.vip388_user.basic_auth)
        cls.vip488_user = ApiOrderInfo(token=cls.vip488_user.basic_auth)
        #cls.no_vip_user = ApiOrderInfo(token=cls.no_vip_user.basic_auth)

        # 读取配置文件中的测试手机号：13888888883
        cls.mobile = cls.config['reading_account']['no_vip_user']

        # 如果手机账号存在则先注销，再重新注册。确保账号是干净的
        cls.u = ApiUser()
        if cls.u.get_jlgl_user(cls.mobile) != None:
            logout_mobile(cls.mobile)

        # 重新注册
        cls.token = logon_mobile(cls.mobile, cls.config['ggheader_v2'])
        cls.no_vip_user = ApiOrderInfo(token=cls.token)



    def test_order_list_empty(self):
        ''' 01) 无订单时访问订单列表页,应返回空'''
        resp = self.guest.api_order_list()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['orderList'] == []


    def test_order_list_notempty(self):
        ''' 02) 有终身卡订单时访问订单列表页 -> 返回该笔订单信息'''
        resp = self.vip488_user.api_order_list()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['orderList'][0]['ttl'] == '终身畅读VIP'
        assert resp['data']['orderList'][0]['orderStatus'] == 'paid'


    def test_order_detail(self):
        ''' 03) 获取订单详情页'''
        id = self.user.api_order_list()['data']['orderList'][0]['id']
        resp = self.user.api_order_detail(id)
        print('订单号:',id)
        print('订单详情数据:',resp)
        assert resp['code'] == 0
        assert resp['data']['ttl'] != None
        assert resp['data']['channel'] == 'wx'
        assert resp['data']['oid'] == id


    def test_putAddress_logistics(self):
        ''' 04) 填写收货地址、物流信息'''

        # 读取购买页，如果spu是GGRVIP_Purchase_01_SPU 或 GGRVIP_Purchase_SPU 就是配了买赠活动的，其余spu无赠品
        order_user = UserProperty(self.config['reading_account']['no_vip_user'])
        resp = ApiPurchasePage(token=order_user.basic_auth).api_v2_vip_purchase()
        spu = resp['data']['spuUIElement']['commodityNo']
        print('spu是', spu)
        sgu = resp['data']['items'][0]['itemId']
        print('sgu是', sgu)

        if spu == 'GGRVIP_Purchase_SPU' or spu == 'GGRVIP_Purchase_01_SPU':
            #购买终身卡，填写收货信息（商品中台里需要配置实体赠品）

            oid = ApiCreateOrder(token=order_user.basic_auth).api_order_charge(sgu, 'wx')['data']['order_no']  # 下单,并获取订单号
            charge_resp = ApiPingpp(token=order_user.basic_auth).api_pingpp_charge_callback(oid)
            print('charge_resp:', charge_resp)
            resp = self.no_vip_user.api_order_address(oid=oid, name='Karen测试', phone='13816435634', province='上海', city='上海',
                                                      district='长宁区', detail='测试订单不要发货')
            print(resp)
            assert resp['code'] == 0
            assert resp['msg'] == 'success'

            #物流信息
            resp = self.no_vip_user.api_order_logistics_detail(oid='O66619827773796352')
            print('返回数据',resp)
            assert resp['code'] == 0
            assert resp['data']['name'] != None #商品名称不为空
            assert resp['data']['icon'] != None #商品图片不为空
            assert resp['data']['shipping']['name'] != None #收货人姓名不为空
            assert resp['data']['shipping']['phone'] != None #手机号不为空
            assert resp['data']['shipping']['detail'] != None #收货地址不为空

            #退款
            refund_resp = ApiPingpp(token=order_user.basic_auth).api_pingpp_refund_callback(oid)
            print('refund_resp:', refund_resp)

        else:
            print('当前未配置买赠活动，跳过此条用例')
            pass


    def test_order_gifts(self):
        ''' 05) 获取订单赠品'''

        # 读取购买页，如果spu是GGRVIP_Purchase_01_SPU 或 GGRVIP_Purchase_SPU 就是配了买赠活动的，其余spu无赠品
        order_user = UserProperty(self.config['reading_account']['no_vip_user'])
        resp = ApiPurchasePage(token=order_user.basic_auth).api_v2_vip_purchase()
        spu = resp['data']['spuUIElement']['commodityNo']
        print('spu是',spu)
        sgu = resp['data']['items'][0]['itemId']
        print('sgu是', sgu)

        if spu == 'GGRVIP_Purchase_SPU' or spu == 'GGRVIP_Purchase_01_SPU':
            order_no = ApiCreateOrder(token=order_user.basic_auth).api_order_charge(sgu, 'wx')
            print('order_no:', order_no)
            oid = order_no['data']['order_no']
            print('oid:', oid)
            charge_resp = ApiPingpp(token=order_user.basic_auth).api_pingpp_charge_callback(oid)
            print('charge_resp:', charge_resp)

            #请求订单赠品
            resp = self.no_vip_user.api_order_gifts(oid)
            print('返回数据：',resp)
            assert resp['code'] == 0
            assert resp['data']['itemId'] == sgu
            assert resp['data']['gifts'] != None
            print('赠品信息:',resp['data']['gifts'])

            #退款
            refund_resp = ApiPingpp(token=order_user.basic_auth).api_pingpp_refund_callback(oid)
            print('refund_resp:', refund_resp)
        else:
            print('当前未配置买赠活动，跳过此条用例')
            pass


    def test_order_notice(self):
        ''' 06) 获取当前物流公告'''
        resp = self.user.api_order_notice('orderdetail')
        assert resp['code'] == 0
        assert resp['msg'] == 'success'
