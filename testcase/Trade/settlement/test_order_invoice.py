# -*- coding: utf-8 -*-
# @Time: 2021/5/21 11:06 上午
# @Author: ian.zhou
# @File: test_order_invoice
# @Software: PyCharm

from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.common.UserProperty import UserProperty
from business.Trade.tradeSettlement.ApiInvoice import ApiInvoiceAdmin, ApiInvoiceClient
from testcase.Trade.common import OrderCommon
from business.mysqlQuery import EshopQuery
import pytest
import datetime
import time


@pytest.mark.Trade
@pytest.mark.TradeSettlement
class TestOrderInvoice:
    """订单发票相关用例"""

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
        cls.eshop_query = EshopQuery()
        cls.invoice_client = ApiInvoiceClient(token=basic_auth)
        cls.invoice_admin = ApiInvoiceAdmin(token=a_token)
        cls.order_common = OrderCommon(c_user=c_user)

    @pytest.fixture(scope='class')
    def get_one_order(self, get_commodity):
        """前置生成一个现金支付的订单"""
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_phy']['ge']['no']
        order = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no, guadou_num=0)
        order_no, charge_id = order[0], order[1]
        time.sleep(3)
        order_detail = self.eshop_query.query_eshop_orders(sql=f'SELECT * FROM orders WHERE order_no="{order_no}"')[0]
        yield order_detail
        self.order_common.order_refund_and_remove(charge_id=charge_id, order_no=order_no)

    @pytest.fixture(scope='function')
    def reset_order_info(self, get_one_order):
        """前置还原订单相关信息、并删除订单开票记录"""
        # 还原订单相关信息
        order_no = get_one_order['order_no']
        state, pay_price, pay_at = get_one_order['state'], get_one_order['pay_price'], get_one_order['pay_at']
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET state={state}, pay_price={pay_price}, pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 删除订单开票记录
        self.eshop_query.delete_order_invoice_record(order_no=order_no)

    @pytest.mark.parametrize("title_type", [0, 1])
    def test_e_invoice_apply_1(self, get_one_order, reset_order_info, title_type):
        """
        电子发票：符合条件订单可以申请开具电子发票
        :param title_type: 0：个人 1：企业单位
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 修改订单支付时间为使其符合开票条件
        pay_at = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 验证可开票订单列表正确返回此订单
        res = self.invoice_client.api_invoice_order_list()['data']['content']
        order_list = [order['orderNo'] for order in res]
        assert order_no in order_list
        # 验证开票信息正确返回
        res = self.invoice_client.api_invoice_apply_prepare(orderNos=[order_no])
        assert res['code'] == 0
        assert res['data']['invoiceContent'] == '明细'
        assert res['data']['price'] == get_one_order['pay_price']
        # 验证开票申请提交成功
        res = self.invoice_client.api_invoice_apply(orderNos=[order_no], buyerType=title_type)
        assert res['code'] == 0
        assert 'serialNo' in res['data']
        serial_no = res['data']['serialNo']
        time.sleep(3)
        # 验证开票申请信息正确返回
        res = self.invoice_client.api_invoice_detail(serialNo=serial_no)
        assert res['code'] == 0
        assert res['data']['serialNo'] == serial_no
        assert res['data']['status'] == 1
        # 验证管理后台订单开票状态正确返回
        res = self.invoice_admin.api_get_order_invoice_info(orderNo=order_no)
        assert res['code'] == 0
        assert res['data']['invoiceType'] == 0
        assert res['data']['status'] == 1
        assert res['data']['invoiceTypeDesc'] == '增值税电子普通发票'
        assert res['data']['statusDesc'] == '已开票'
        assert not res['data']['allowSetPaperInvoice']
        assert not res['data']['allowCancel']

    def test_e_invoice_apply_2(self, get_one_order, reset_order_info):
        """
        电子发票：已开电子发票订单不能开具发票
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 修改订单支付时间为使其符合电子发票开票条件
        pay_at = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 申请开具电子发票
        self.invoice_client.api_invoice_apply(orderNos=[order_no])
        time.sleep(3)
        # 验证可开票订单列表不返回已开电子发票订单
        res = self.invoice_client.api_invoice_order_list()['data']['content']
        order_list = [order['orderNo'] for order in res]
        assert order_no not in order_list
        # 验证已开电子发票订单无法提交电子发票开票申请
        res = self.invoice_client.api_invoice_apply(orderNos=[order_no])
        assert res['code'] == 42002
        assert res['msg'] == '选中订单部分不可开票, 请重新选择'
        # 验证已开电子发票订单不能设置已开纸质票
        res = self.invoice_admin.api_set_paper_invoice(orderNo=order_no)
        assert res['code'] == 200200
        assert res['msg'] == '当前状态不允许设置为纸质发票'

    @pytest.mark.parametrize('state', [1, 6, 5])
    def test_e_invoice_apply_3(self, get_one_order, reset_order_info, state):
        """
        电子发票：未支付、已取消、已退款的订单不能开具发票
        :param state: 1：未支付 6：已取消 5：已退款
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 修改订单支付时间符合电子发票开票条件，并修改订单状态至目标状态
        pay_at = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET state={state}, pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 验证可开票订单列表不返回此订单
        res = self.invoice_client.api_invoice_order_list()['data']['content']
        order_list = [order['orderNo'] for order in res]
        assert order_no not in order_list
        # 验证无法提交电子发票开票申请
        res = self.invoice_client.api_invoice_apply(orderNos=[order_no])
        assert res['code'] == 42002
        assert res['msg'] == '选中订单部分不可开票, 请重新选择'
        # 验证不能设置已开纸质票
        res = self.invoice_admin.api_set_paper_invoice(orderNo=order_no)
        assert res['code'] == 200200
        assert res['msg'] == '当前订单状态不允许设置为纸质发票'

    def test_e_invoice_apply_4(self, get_one_order, reset_order_info):
        """
        电子发票：支付时间超过180天的订单不能申请开具电子发票
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 修改订单支付时间为超过6个月
        pay_at = (datetime.datetime.now() - datetime.timedelta(days=185)).strftime("%Y-%m-%d %H:%M:%S")
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 验证可开票订单列表
        res = self.invoice_client.api_invoice_order_list()['data']['content']
        order_list = [order['orderNo'] for order in res]
        assert order_no not in order_list
        # 验证无法提交开票申请
        res = self.invoice_client.api_invoice_apply(orderNos=[order_no])
        assert res['code'] == 42002
        assert res['msg'] == '选中订单部分不可开票, 请重新选择'

    def test_e_invoice_apply_5(self, get_one_order, reset_order_info):
        """
        电子发票：现金支付金额为0的订单不能申请开具电子发票
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 修改订单的支付时间符合电子发票开票条件，并修改订单现金支付金额为0
        pay_at = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET pay_price=0, pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 验证可开票订单列表不返回此订单
        res = self.invoice_client.api_invoice_order_list()['data']['content']
        order_list = [order['orderNo'] for order in res]
        assert order_no not in order_list
        # 验证无法提交开票申请
        res = self.invoice_client.api_invoice_apply(orderNos=[order_no])
        assert res['code'] == 42002
        assert res['msg'] == '选中订单部分不可开票, 请重新选择'

    def test_e_invoice_apply_6(self, get_one_order, reset_order_info):
        """
        电子发票：管理后台取消阻塞状态的开票申请（status=0，stage=1）
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 修改订单的支付时间符合电子发票开票条件
        pay_at = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 申请开具电子发票
        serial_no = self.invoice_client.api_invoice_apply(orderNos=[order_no])['data']['serialNo']
        time.sleep(3)
        # 设置开票申请为阻塞状态
        self.eshop_query.execute_trade_settlement(sql=f'UPDATE invoice_apply SET status=0, stage=1 WHERE serial_no="{serial_no}"')
        # 验证管理后台订单开票状态正确返回
        res = self.invoice_admin.api_get_order_invoice_info(orderNo=order_no)
        assert res['data']['allowCancel']
        # 验证申请可以成功取消
        res = self.invoice_admin.api_cancel_blocked_invoice_apply(orderNo=order_no)
        assert res['code'] == 0
        # 验证开票申请取消后可以重新申请电子发票开票
        res = self.invoice_client.api_invoice_order_list()['data']['content']
        order_list = [order['orderNo'] for order in res]
        assert order_no in order_list
        # 验证开票申请取消后可以重新设置已开纸质发票
        res = self.invoice_admin.api_get_order_invoice_info(orderNo=order_no)
        assert res['code'] == 0
        assert res['data']['invoiceType'] == 0
        assert res['data']['status'] == 2
        assert res['data']['invoiceTypeDesc'] == '增值税电子普通发票'
        assert res['data']['statusDesc'] == '开票失败'
        assert res['data']['allowSetPaperInvoice']
        assert not res['data']['allowCancel']

    def test_set_paper_invoice_1(self, get_one_order, reset_order_info):
        """
        纸质发票：管理后台设置订单已开纸质发票
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 验证订单正确设置纸质发票
        res = self.invoice_admin.api_set_paper_invoice(orderNo=order_no)
        assert res['code'] == 0
        # 验证订单开票状态正确返回
        res = self.invoice_admin.api_get_order_invoice_info(orderNo=order_no)
        assert res['code'] == 0
        assert res['data']['invoiceType'] == 1
        assert res['data']['status'] == 1
        assert res['data']['invoiceTypeDesc'] == '增值税纸质普通发票'
        assert res['data']['statusDesc'] == '已开票'
        assert not res['data']['allowSetPaperInvoice']
        assert not res['data']['allowCancel']

    def test_set_paper_invoice_2(self, get_one_order, reset_order_info):
        """
        纸质发票：已开纸质发票的订单不能申请开具电子发票
        :return:
        """
        # 获取开票订单
        order_no = get_one_order['order_no']
        # 修改订单支付时间符合电子发票开票条件
        pay_at = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        self.eshop_query.execute_eshop_orders(sql=f'UPDATE orders SET pay_at="{pay_at}" WHERE order_no="{order_no}"')
        # 设置订单已开纸质发票
        self.invoice_admin.api_set_paper_invoice(orderNo=order_no)
        # 验证可开票订单列表不返回已开纸质发票订单
        res = self.invoice_client.api_invoice_order_list()['data']['content']
        order_list = [order['orderNo'] for order in res]
        assert order_no not in order_list
        # 验证已开纸质发票订单无法提交电子发票开票申请
        res = self.invoice_client.api_invoice_apply(orderNos=[order_no])
        assert res['code'] == 42002
        assert res['msg'] == '选中订单部分不可开票, 请重新选择'


