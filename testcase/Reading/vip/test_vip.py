# coding=utf-8
import pytest
import pytest_check as check

from business.Reading.user.ApiUser import ApiUser
from config.env.domains import Domains
from business.Reading.vip.ApiVip import ApiVip
from business.common.UserProperty import UserProperty
from business.Reading.vip.ApiRedeem import ApiRedeem
from business.Reading.vip.ApiSendVip import ApiSendVip
from time import sleep


@pytest.mark.ggrVip
class TestVip(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])

        cls.mobile = cls.config['reading_account']['user2'] # 13888888884
        user = UserProperty(cls.mobile)
        cls.vip = ApiVip(token=user.basic_auth)

        # 13888888884 注销
        logout_resp = cls.vip.api_get_user_sms_logout(cls.mobile)
        cls.u = ApiUser()
        db_user = cls.u.get_jlgl_user(cls.mobile)
        code = db_user['sms']['code']
        cls.vip.api_delete_user('mobilecode', cls.mobile, code)
        sleep(2)

        # 13888888884 注册
        cls.u.api_get_user_sms_login(cls.mobile, cls.config['ggheader_v2'])
        db_user = cls.u.get_jlgl_user(cls.mobile)
        cls.id = db_user['_id']
        code = db_user['sms']['code']
        cls.token = cls.u.get_token(typ="mobilecode", u=cls.mobile, p=code)
        #print(cls.token)
        cls.vip = ApiVip(token=cls.token)


    def test_get_vip_success(self):
        """获取vip状态"""
        sleep(2)
        resp = self.vip.api_get_vip() # 13888888884
        sleep(2)
        check.equal(resp["code"], 0)
        check.equal(resp['data']['vip'], False)
        check.equal(resp['data']['paid'], False)

        # 生成兑换码
        user1 = UserProperty(self.config['admin_account']['user'])
        token1 = user1.basic_auth
        redeem1 = ApiRedeem(token=token1)
        res = redeem1.api_circulars_redeem("GGREADVIP_365")
        code = res['data']['code'][0]
        print('【兑换码】',code)

        # 兑换
        redeem2 = ApiRedeem(token=self.token)
        redeem2.api_redeem_exchange(code)
        resp1 = self.vip.api_get_vip()
        #print(resp1)
        check.equal(resp1['data']['vip'], True)
        check.equal(resp1['data']['paid'], True)
        check.equal(resp1['data']['isLifetime'], False)
        # 注销兑换码
        redeem1.api_redeem_refund(code)


    def test_api_get_v2_vip_purchase(self):
        """测试订单页面"""
        resp = self.vip.api_get_v2_vip_purchase()
        print(resp)
        check.equal(resp["code"], 0)
        amount1 = resp['data']['items'][0]['amount']
        amount2 = resp['data']['items'][1]['amount']
        check.equal(amount1, 38800)
        check.equal(amount2, 48800)


    def test_send_vip(self):
        """测试赠送7天vip"""
        sleep(2)
        admin = UserProperty(self.config['admin_account']['user'])
        send_vip = ApiSendVip(token=admin.basic_auth)
        resp = send_vip.api_send_vip(self.id) # 13888888884

        check.equal(resp["code"], 0)
        resp1 = self.vip.api_get_vip()
        sleep(2)
        check.equal(resp1['data']['vip'], True)
        check.equal(resp1['data']['paid'], False)


    def test_api_vip_trial(self):
        """测试站外领取7天vip"""
        #注销
        self.vip.api_get_user_sms_logout(self.mobile)
        db_user = self.u.get_jlgl_user(self.mobile)
        code = db_user['sms']['code']
        print(code)
        self.vip.api_delete_user('mobilecode', self.mobile, code)

        # 发送验证码
        self.u.api_get_user_sms(self.mobile, self.config['ggheader_v2'],)
        # code
        db_user = self.u.get_jlgl_user(self.mobile)
        code = db_user['sms']['code']
        print(code)

        # 站外领取vip
        user = UserProperty(self.mobile)
        token = user.basic_auth
        vip = ApiVip(token=token)
        resp = vip.api_vip_trial(self.mobile, code, "DetailShareBook", "ReadingVIPFree_7_Share")
        print(resp)
        # check.equal(resp["code"], 0)
        check.equal(resp["data"]['newClaim'], True)