# -*- coding: utf-8 -*-
# @Time: 2021/6/19 12:00 上午
# @Author: ian.zhou
# @File: test_orders_client
# @Software: PyCharm

from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiRedeem import ApiRedeem
from business.Trade.eshopClient.ApiRedeem import ApiRedeem as c_ApiRedeem
from business.Trade.tradeOrder.ApiOrderApi import ApiOrderApi
from testcase.Trade.common import OrderCommon
from business.common.UserProperty import UserProperty
from utils.format.format import time
from business.mysqlQuery import EshopQuery
import pytest


@pytest.mark.Trade
@pytest.mark.TradeCommodity
@pytest.mark.TradeOrder
@pytest.mark.TradeRedeem
class TestOrdersClient:
    """C端H5订单中心相关用例"""
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
        basic_auth = UserProperty(mobile=c_user).basic_auth
        cls.eshop_admin_redeem = ApiRedeem(token=a_token)
        cls.c_eshop_redeem = c_ApiRedeem(token=basic_auth)
        cls.orders = ApiOrderApi(token=basic_auth)
        cls.eshop_query = EshopQuery()
        cls.order_common = OrderCommon(c_user=c_user)

    def teardown(self):
        self.order_common.order_refund_and_remove(self.charge_id, self.order_no)
        self.order_no = None
        self.charge_id = None

    def test_order_address_modify(self, get_commodity):
        """
        修改收货地址：测试订单内实体未全部发货，可以修改订单收货地址
        :return:
        """
        # 生成一个含实体商品的订单
        sgu_id = get_commodity['sgu_phy']['ge']['id']
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id)['data']['detail']
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code, needAddress=True)
        self.order_no = res['data']['orderNo']
        time.sleep(5)
        # 验证订单当前地址信息正确返回
        res = self.orders.api_order_address_prepare(orderNo=self.order_no)
        assert res['code'] == 0
        assert res['data']['orderNo'] == self.order_no
        assert 'recipientAddress' in res['data']
        # 验证订单地址正确更新
        res = self.orders.api_order_address_commit(orderNo=self.order_no, addressStreet='修改测试')
        assert res['code'] == 0
        assert res['data']['recipientAddress']['addressStreet'] == '修改测试'

    def test_order_address_modify_no_physical(self, get_commodity):
        """
        修改收货地址：测试订单内不含实体，无法修改收货地址
        :return:
        """
        # 生成一个不含实体商品的订单
        sgu_id = get_commodity['sgu_system']['ge']['id']
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id)['data']['detail']
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code)
        self.order_no = res['data']['orderNo']
        time.sleep(5)
        # 验证订单内不含实体，无法修改收货地址
        res = self.orders.api_order_address_prepare(orderNo=self.order_no)
        assert res['code'] == 20002
        assert res['msg'] == '订单中无未发货商品，暂不支持修改'

    def test_order_address_modify_all_delivery(self, get_commodity):
        """
        修改收货地址：测试订单内实体已全部发货，无法修改收货地址
        :return:
        """
        # 生成一个含实体商品的订单
        sgu_id = get_commodity['sgu_phy']['ge']['id']
        redeem_code = self.eshop_admin_redeem.api_create_redeem(sguId=sgu_id)['data']['detail']
        res = self.c_eshop_redeem.api_use_redeem(redeemNo=redeem_code, needAddress=True)
        self.order_no = res['data']['orderNo']
        time.sleep(5)
        # 修改订单内实体状态为已发货
        sql = f'UPDATE orders_detail set shipment_id=1 WHERE orders_id in (SELECT id FROM orders WHERE ' \
              f'order_no="{self.order_no}") AND scgu_id<>0'
        self.eshop_query.execute_eshop_orders(sql)
        # 验证订单内实体已全部发货，无法修改收货地址
        res = self.orders.api_order_address_prepare(orderNo=self.order_no)
        assert res['code'] == 20002
        assert res['msg'] == '订单中无未发货商品，暂不支持修改'













