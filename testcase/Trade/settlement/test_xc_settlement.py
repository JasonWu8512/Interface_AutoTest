# -*- coding: utf-8 -*-
# @Time    : 2021/3/11 10:22 上午
# @Author  : jerry_wan
# @Software: PyCharm

from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.tradeSettlement.ApiSubmergedAdminController import ApiSubmergedAdminController
import pytest
import time


@pytest.mark.Trade
@pytest.mark.TradeSettlement
class TestXcSettlement:
    """后台下沉代理结算相关用例"""
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_trade = ApiSubmergedAdminController(token=a_token)

    @pytest.mark.parametrize("check_bill_status", [None, 'UN_COMMIT', 'UN_AUDIT', 'PASS', 'REFUND'])
    @pytest.mark.parametrize("settlement_bill_status", [None, 'WAIT', 'HAD'])
    @pytest.mark.parametrize("invoice_status", [None, 'WAIT', 'HAD'])
    def test_settlement_page_list(self, check_bill_status, invoice_status, settlement_bill_status):
        """
        查询结算列表,不同查询条件的结果
        :param check_bill_status: 对账单状态/对应界面 账单状态
        :param settlement_bill_status: 结算状态
        :param invoice_status: 发票状态
        :return:
        """
        res = self.eshop_admin_trade.api_settlement_page_list(check_bill_status=check_bill_status,
                                                              settlement_bill_status=settlement_bill_status,
                                                              invoice_status=invoice_status)
        # 将当前列表包含的账单状态check_bill_status值组合成一个集合
        check_bill_status_set = set([checkBillStatus['checkBillStatus'] for checkBillStatus in res['data']['data']])
        # 将当前列表包含的结算状态settlement_bill_status值组合成一个集合
        settlement_bill_status_set = set([settlementBillStatus['settlementBillStatus'] for settlementBillStatus in
                                          res['data']['data']])
        # 将当前列表包含的发票状态invoice_status值组合成一个集合
        invoice_status_set = set([invoiceStatus['invoiceStatus'] for invoiceStatus in
                                  res['data']['data']])
        if check_bill_status is not None:
            # 断言获取结算列表是否正确
            assert res['code'] == 0
            # 断言账单状态是否正确
            assert check_bill_status_set in [{check_bill_status}, set()]
        else:
            # 断言获取结算列表是否正确
            assert res['code'] == 0
            # 断言账单状态是否正确
            assert check_bill_status_set.issubset({'UN_COMMIT', 'UN_AUDIT', 'PASS', 'REFUND'})

        if settlement_bill_status is not None:
            # 断言获取结算列表是否正确
            assert res['code'] == 0
            # 断言结算状态是否正确
            assert settlement_bill_status_set in [{settlement_bill_status}, set()]
        else:
            # 断言获取结算列表是否正确
            assert res['code'] == 0
            # 断言结算状态是否正确
            assert settlement_bill_status_set.issubset({'WAIT', 'HAD'})

        if invoice_status is not None:
            # 断言获取结算列表是否正确
            assert res['code'] == 0
            # 断言发票状态是否正确
            assert invoice_status_set in [{invoice_status}, set()]
        else:
            # 断言获取结算列表是否正确
            assert res['code'] == 0
            # 断言发票状态是否正确
            assert invoice_status_set.issubset({'WAIT', 'HAD'})

    def test_broker_age_bill_list(self):
        """
        查询代理商当月所有对账单
        :return:
        """
        # 获取结算列表所有信息
        settlement_list = self.eshop_admin_trade.api_settlement_page_list()
        # 获取结算列表第一个代理商
        submerged_agent_no = settlement_list['data']['data'][0]['submergedAgentNo']
        # 获取结算列表第一个代理商的结算月份
        settlement_month = settlement_list['data']['data'][0]['settlementMonth']
        # 查看代理商的所有对账单
        broker_age_bill_list = self.eshop_admin_trade.api_broker_age_bill_list(submerged_agent_no, settlement_month)

        assert broker_age_bill_list['code'] == 0
        time.sleep(5)
        # 断言列表的代理商和对账单的代理商是否一致
        assert settlement_list['data']['data'][0]['submergedAgentNo'] == broker_age_bill_list['data'][0]['submergedAgentNo']

    def test_adjust_bill_add(self, adjust_amount=1400, remark=None):
        """
        调整账单-新增14元佣金
        """
        # 获取待提交的代理商
        settlement_list = self.eshop_admin_trade.api_settlement_page_list(check_bill_status='UN_COMMIT')
        # 获取结算列表第一个代理商
        submerged_agent_no = settlement_list['data']['data'][0]['submergedAgentNo']
        # 获取结算列表第一个代理商的结算月份
        settlement_month = settlement_list['data']['data'][0]['settlementMonth']
        # 查看代理商的所有对账单
        broker_age_bill_list = self.eshop_admin_trade.api_broker_age_bill_list(submerged_agent_no, settlement_month)
        # 获取该代理商对账单的第一个对账单号
        broker_age_bill_list_no = broker_age_bill_list['data'][0]['billNo']
        # 获取调整类型为新增
        adjust_type_add = self.eshop_admin_trade.api_adjust_type_list()['data'][0]['key']

        # 新增佣金1400
        adjust_bill_add = self.eshop_admin_trade.api_adjust_bill(bill_no=broker_age_bill_list_no,
                                                                 adjust_type=adjust_type_add,
                                                                 adjust_amount=adjust_amount, remark=remark)
        # 断言接口返回成功
        assert adjust_bill_add['code'] == 0
        # 断言调整佣金与查询到的金额一致
        time.sleep(5)
        assert broker_age_bill_list['data'][0]['adjustAmount'] == 1400

    def test_adjust_bill_sub(self, adjust_amount=2200, remark=None):
        """
        调整账单-减少22元佣金
        """
        # 获取待提交的代理商
        settlement_list = self.eshop_admin_trade.api_settlement_page_list(check_bill_status='UN_COMMIT')
        # 获取结算列表第二个代理商
        submerged_agent_no = settlement_list['data']['data'][1]['submergedAgentNo']
        # 获取结算列表第一个代理商的结算月份
        settlement_month = settlement_list['data']['data'][1]['settlementMonth']
        # 查看代理商的所有对账单
        broker_age_bill_list = self.eshop_admin_trade.api_broker_age_bill_list(submerged_agent_no, settlement_month)
        # 获取该代理商对账单的第一个对账单号
        broker_age_bill_list_no = broker_age_bill_list['data'][0]['billNo']
        # 获取调整类型为减少
        adjust_type_sub = self.eshop_admin_trade.api_adjust_type_list()['data'][1]['key']

        # 减少佣金2200
        adjust_bill_sub = self.eshop_admin_trade.api_adjust_bill(bill_no=broker_age_bill_list_no,
                                                                 adjust_type=adjust_type_sub,
                                                                 adjust_amount=adjust_amount, remark=remark)
        # 断言接口返回成功
        assert adjust_bill_sub['code'] == 0
        # 断言调整佣金与查询到的金额一致
        time.sleep(5)
        assert broker_age_bill_list['data'][0]['adjustAmount'] == -2200

