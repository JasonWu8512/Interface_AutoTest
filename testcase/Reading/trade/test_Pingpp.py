# coding=utf-8
# @Time    : 2021/5/25 1:40 下午
# @Author  : Karen
# @File    : test_Pingpp.py

import pytest

from business.Reading.trade.ApiPurchasePage import ApiPurchasePage
from business.common.UserProperty import UserProperty
from business.Reading.trade.ApiPingpp import ApiPingpp
from business.Reading.user.ApiUser import ApiUser
from business.Reading.vip.ApiVip import ApiVip
from business.Reading.trade.ApiCreateOrder import ApiCreateOrder
from config.env.domains import Domains
from testcase.Reading.trade import logout_mobile, logon_mobile


@pytest.mark.ggrTrade
class TestPingpp(object):
    ''' Ping++ '''
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取fat环境配置
        cls.config = cls.dm.set_env_path()

        # 设置域名
        cls.dm.set_domain(cls.config['reading_url'])
        # cls.no_vip_user = UserProperty(cls.config['reading_account']['no_vip_user']) # 读取配置文件中的非vip用户
        #
        # # 实例不同身份对象
        # cls.no_vip_user = ApiPingpp(token=cls.no_vip_user.basic_auth)

        # 读取配置文件中的测试手机号：13888888883
        cls.mobile = cls.config['reading_account']['no_vip_user']

        # 如果手机账号存在则先注销，再重新注册。确保账号是干净的
        cls.u = ApiUser()
        if cls.u.get_jlgl_user(cls.mobile) != None:
            logout_mobile(cls.mobile)

        #重新注册
        cls.token = logon_mobile(cls.mobile, cls.config['ggheader_v2'])
        cls.no_vip_user = ApiPingpp(token=cls.token)


    def test_pingpp_callback(self):
        """ 01）ping++支付、退款回调 """
        # 读取购买页，如果spu是GGRVIP_Purchase_01_SPU 或 GGRVIP_Purchase_SPU 就是配了买赠活动的，其余spu无赠品
        order_user = UserProperty(self.config['reading_account']['no_vip_user'])
        resp = ApiPurchasePage(token=order_user.basic_auth).api_v2_vip_purchase()
        spu = resp['data']['spuUIElement']['commodityNo']
        print('spu是', spu)
        sgu = resp['data']['items'][0]['itemId']
        print('sgu是', sgu)

        #支付回调
        print('order_user',order_user.mobile)
        import time
        time.sleep(2)
        order_no = ApiCreateOrder(token=order_user.basic_auth).api_order_charge(sgu,'wx')
        print('order_no:',order_no)
        oid = order_no['data']['order_no']
        print('oid:',oid)
        charge_resp = self.no_vip_user.api_pingpp_charge_callback(oid)
        print('charge_resp:',charge_resp)
        assert charge_resp['code'] == 0

        # #退款回调，该接口已废弃
        # refund_resp = self.no_vip_user.api_pingpp_refund_callback(oid)
        # print('refund_resp:',refund_resp)
        # assert refund_resp['code'] == 0




