# -*- coding: utf-8 -*-
# @Time: 2021/6/18 7:45 下午
# @Author: ian.zhou
# @File: test_redeem_client
# @Software: PyCharm


from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from business.Trade.eshopAdmin.ApiRedeem import ApiRedeem
from business.Trade.eshopClient.ApiRedeem import ApiRedeem as c_ApiRedeem
from business.Trade.eshopClient.ApiGhs import ApiGhs
from testcase.Trade.common import OrderCommon
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.common.UserProperty import UserProperty
from utils.format.format import time, dateToTimeStamp, timeStampToTimeStr
from business.mysqlQuery import EshopQuery
from business.businessQuery import xshareQuery, ghsQuery
import pytest


@pytest.mark.Trade
@pytest.mark.TradeRedeem
@pytest.mark.TradeCommodity
@pytest.mark.TradeOrder
class TestRedeemClient:
    """C端兑换码兑换相关用例"""
    order_no = None
    charge_id = None

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        # 获取管理后台用户token
        a_user = cls.config['eshop']['admin']['user']
        a_pwd = cls.config['eshop']['admin']['pwd']
        a_token = ApiAdminAuth().api_login(username=a_user, password=a_pwd).get('data').get('token')
        # 获取C端用户token
        c_user = cls.config['eshop']['user']
        c_auth = UserProperty(mobile=c_user).basic_auth
        cls.uid = UserProperty(mobile=c_user).user_id
        cls.eshop_admin_commodity = ApiCommodity(token=a_token)
        cls.eshop_admin_redeem = ApiRedeem(token=a_token)
        cls.c_eshop_redeem = c_ApiRedeem(token=c_auth)
        cls.c_eshop_ghs = ApiGhs(token=c_auth)
        cls.xshare_query, cls.ghs_query, cls.eshop_query = xshareQuery(), ghsQuery(), EshopQuery()
        cls.order_common = OrderCommon(c_user=c_user)

    def teardown(self):
        self.order_common.order_refund_and_remove(self.charge_id, self.order_no)
        self.order_no = None
        self.charge_id = None

    @pytest.mark.parametrize('subject', ['GE', 'MA'])
    def test_redeem_system_course(self, get_commodity, subject):
        """
        兑换码：测试兑换正价课
        :param subject: 科目 英语：GE  思维：MA
        """
        # 获取生成兑换码的SGU id
        sgu_id = get_commodity['sgu_system']['ge']['id']
        if subject == 'MA':
            sgu_id = get_commodity['sgu_system']['ma']['id']
        # 生成一个兑换码
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id)['data']['detailList']
        # 删除用户规划师
        self.ghs_query.delete_ghs_user(_id=self.uid)
        self.ghs_query.delete_math_ghs_user(uid=self.uid)
        # 验证正价课兑换成功
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[0])
        self.order_no = res['data']['orderNo']
        assert res['code'] == 0
        assert not res['data']['isXshare']
        time.sleep(5)
        # 验证首次拥有正价课应分配对应科目规划师
        res = self.c_eshop_ghs.api_get_ghs(orderId=self.order_no)
        assert res['code'] == 0
        assert res['data']['eshopFirst']
        assert res['data'].get('url', 0) != 0
        # 验证已使用的兑换码无法进行兑换
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[0])
        assert res['code'] == 140001
        assert res['msg'] == '兑换码不可用'

    @pytest.mark.parametrize('subject', ['GE', 'MA'])
    def test_redeem_trial_course(self, get_commodity, subject):
        """
        兑换码：测试兑换体验课
        :param subject: GE：英语体验课 MA：思维体验课
        """
        # 获取生成兑换码的SGU id
        sgu_no = get_commodity['sgu_trial']['ge']['no']
        if subject == 'MA':
            sgu_no = get_commodity['sgu_trial']['ma']['no']
        sgu_id = self.eshop_admin_commodity.api_get_sxu_list(commodityNo=sgu_no, sxuType=2)['data']['content'][0]['id']
        # 生成一个兑换码
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id, num=2)['data']['detailList']
        # 验证体验课含实体，兑换需填写地址
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[0])
        assert res['code'] == 140004
        assert res['msg'] == '需要填写收货人地址'
        # 验证兑换成功返回isXshare为true
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[0], needAddress=True)
        self.order_no = res['data']['orderNo']
        assert res['data']['isXshare']
        # 验证非新用户，无法兑换体验课
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[1])
        assert res['code'] == 140007

    def test_redeem_destroyed(self, get_commodity):
        """
        兑换码：测试已销毁的兑换码无法使用
        """
        # 获取生成兑换码的SGU id
        sgu_id = get_commodity['sgu_system']['ge']['id']
        # 生成一个兑换码
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id, num=1)['data']['detailList']
        # 销毁兑换码
        self.eshop_admin_redeem.api_destroy_redeem(redeemNoList=redeem_code)
        # 验证已销毁的兑换码无法使用
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[0])
        assert res['code'] == 140001
        assert res['msg'] == '兑换码不可用'

    def test_redeem_expired(self, get_commodity):
        """
        兑换码：测试已过期的兑换码无法使用
        """
        # 获取生成兑换码的SGU id
        sgu_id = get_commodity['sgu_system']['ge']['id']
        # 生成一个兑换码
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id)['data']['detailList']
        # 修改兑换码过期时间
        expired_time = timeStampToTimeStr(dateToTimeStamp(hour=-1))
        sql = f'UPDATE redeem SET expire_at="{expired_time}" WHERE redeem_no="{redeem_code[0]}"'
        self.eshop_query.execute_eshop_orders(sql)
        # 验证已过期的兑换码无法使用
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code[0])
        assert res['code'] == 140002
        assert res['msg'] == '兑换码已过期'
