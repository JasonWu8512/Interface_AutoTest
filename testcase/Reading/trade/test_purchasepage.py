# coding=utf-8
# @Time    : 2021/5/12 5:35 下午
# @Author  : Karen
# @File    : test_purchasepage.py

import pytest
from business.common.UserProperty import UserProperty
from business.Reading.trade.ApiPurchasePage import ApiPurchasePage
from business.Reading.user.ApiUser import ApiUser
from business.Reading.vip.ApiVip import ApiVip
from business.Reading.vip.ApiRedeem import ApiRedeem
from config.env.domains import Domains
from testcase.Reading.trade import logout_mobile, logon_mobile


@pytest.mark.ggrTrade
class TestPurchasePage(object):
    ''' 访问购买页 '''
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取fat环境配置
        cls.config = cls.dm.set_env_path()

        # 设置域名
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = ApiUser().get_guest_token()  # 创建游客并获取token
        cls.guest = ApiPurchasePage(token=cls.guest_token)  # 创建游客实例

        # 初始化不同身份用户
        cls.vip388_user = UserProperty(cls.config['reading_account']['vip388_user'])  # 读取配置文件中的年卡用户
        cls.vip488_user = UserProperty(cls.config['reading_account']['vip488_user'])  # 读取配置文件中的终身卡用户
        #cls.no_vip_user = UserProperty(cls.config['reading_account']['no_vip_user'])  # 读取配置文件中的非vip用户

        # 实例不同身份对象
        cls.vip388_user = ApiPurchasePage(token=cls.vip388_user.basic_auth)
        cls.vip488_user = ApiPurchasePage(token=cls.vip488_user.basic_auth)
        #cls.no_vip_user = ApiPurchasePage(token=cls.no_vip_user.basic_auth)

        # 读取配置文件中的测试手机号：13888888883
        cls.mobile = cls.config['reading_account']['no_vip_user']

        # 如果手机账号存在则先注销，再重新注册。确保账号是干净的
        cls.u = ApiUser()
        if cls.u.get_jlgl_user(cls.mobile) != None:
            logout_mobile(cls.mobile)

        # 重新注册
        cls.token = logon_mobile(cls.mobile, cls.config['ggheader_v2'])
        cls.no_vip_user = ApiPurchasePage(token=cls.token)



    def set_vip388(self):
        '''使用兑换码成为年卡用户'''

        # 生成兑换码
        token = UserProperty(self.config['admin_account']['user']).basic_auth #获取admin用户token
        redeem = ApiRedeem(token=token) #创建兑换码实例
        code = redeem.api_circulars_redeem("GGREADVIP_365")['data']['code'][0] #调用生成兑换码接口，并提取兑换码
        print('年卡兑换码:',code)

        # 兑换
        ApiRedeem(token=self.token).api_redeem_exchange(code)
        resp = ApiVip(token=self.token).api_get_vip()
        print(resp)
        assert resp['data']['vip'] == True
        assert resp['data']['paid'] == True
        assert resp['data']['isLifetime'] == False

        # 返回年卡兑换码
        return code

    def set_vip488(self):
        '''使用兑换码成为终身卡用户'''

        # 生成兑换码
        token = UserProperty(self.config['admin_account']['user']).basic_auth  # 获取admin用户token
        redeem = ApiRedeem(token=token)  # 创建兑换码实例
        code = redeem.api_circulars_redeem("GGREADVIP_Lifetime")['data']['code'][0]  # 调用生成兑换码接口，并提取兑换码
        print('终身卡兑换码:', code)

        # 兑换
        ApiRedeem(token=self.token).api_redeem_exchange(code)
        resp = ApiVip(token=self.token).api_get_vip()
        print(resp)
        assert resp['data']['vip'] == True
        assert resp['data']['paid'] == True
        assert resp['data']['isLifetime'] == True

        # 返回终身卡兑换码
        return code

    def refun_redeem(self,code):
        '''兑换码退款'''
        token = UserProperty(self.config['admin_account']['user']).basic_auth  # 获取admin用户token
        redeem = ApiRedeem(token=token)  # 创建兑换码实例
        redeem.api_redeem_refund(code)
        print('兑换码已退款:',code)

    def test_vip388_user_NewPurchasePage(self):
        ''' 01) 年卡用户访问v1.4.0之后的购买页 '''
        resp = self.vip388_user.api_v2_vip_purchase()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['items'][0]['amount'] == 38800
        assert len(resp['data']['items']) == 2
        assert resp['data']['purchaseBtn']['text'] == '立即升级终身卡'


    def test_vip488_user_NewPurchasePage(self):
        ''' 02) 终身卡用户访问v1.4.0之后的购买页 '''
        resp = self.vip488_user.api_v2_vip_purchase()
        print(resp)
        assert resp['code'] == 251070
        assert resp['msg'] == '您已经是付费 vip 用户了哦'


    def test_no_vip_user_NewPurchasePage(self):
        ''' 03) 非VIP用户访问v1.4.0之后的购买页 '''
        resp = self.no_vip_user.api_v2_vip_purchase()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['items'][0]['amount'] == 38800
        assert resp['data']['items'][1]['amount'] == 48800
        assert resp['data']['purchaseBtn']['text'] == '立即抢购'


    def test_guest_NewPurchasePage(self):
        ''' 04) 游客用户访问v1.4.0之后的购买页 '''

        resp = self.guest.api_v2_vip_purchase()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['items'][0]['amount'] == 38800
        assert resp['data']['items'][1]['amount'] == 48800
        assert resp['data']['purchaseBtn']['text'] == '立即抢购'


    def test_vip388_user_iapPurchasePage(self):
        ''' 05) 年卡用户访问iOS reviewmode购买页 '''
        resp = self.vip388_user.api_vip_iap()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['items'][0]['itemId'] == 'ReadingVIP40'


    def test_vip488_user_iapPurchasePage(self):
        ''' 06) 终身卡用户访问iOS reviewmode购买页 '''
        resp = self.vip488_user.api_vip_iap()
        print(resp)
        assert resp['status'] == 500
        assert resp['message'][:30] == 'This user has been LifetimeVip'


    def test_no_vip_user_iapPurchasePage(self):
        ''' 07) 非VIP用户访问iOS reviewmode购买页 '''
        resp = self.no_vip_user.api_vip_iap()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['items'][0]['type'] == 'month'
        assert resp['data']['items'][0]['itemId'] == 'ReadingVIP40'


    def test_guest_iapPurchasePage(self):
        ''' 08) 游客用户访问iOS reviewmode购买页 '''
        resp = self.guest.api_vip_iap()
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['items'][0]['itemId'] == 'ReadingVIP40'
        assert resp['data']['items'][0]['type'] == 'month'
        assert len(resp['data']['items']) == 1


