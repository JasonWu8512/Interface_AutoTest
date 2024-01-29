# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 15:22 下午
# @Author  : jerry_wan
# @Software: PyCharm

from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.tradeAccount.ApiGuadou import ApiGuadou
import pytest


@pytest.mark.Trade
@pytest.mark.EshopAdmin
@pytest.mark.TradeAccount
class TestGuaDouAccount:
    """后台呱豆账户管理相关用例"""
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_trade_account = ApiGuadou(token=a_token)

    @pytest.mark.parametrize("account_type, search", [('GUADOU', None)])
    def test_gua_dou_account_list_none(self, account_type, search):
        """
        查询呱豆列表,关键字为空
        :return:
        """
        res = self.eshop_admin_trade_account.api_account_list(account_type=account_type, search=search)
        # 断言获取结算列表是否正确
        assert res['code'] == 0

    @pytest.mark.parametrize("account_type, search", [('GUADOU', '1503177')])
    def test_gua_dou_account_list_gua_id(self, account_type, search):
        """
        查询呱豆列表,关键字为guaid
        :return:
        """
        res = self.eshop_admin_trade_account.api_account_list(account_type=account_type, search=search)
        # 断言获取结算列表是否正确
        assert res['code'] == 0
        # 断言guaid与关键字一致
        assert res['data']['data'][0]['guaid'] == '1503177'

    @pytest.mark.parametrize("account_type, search", [('GUADOU', '15921992382')])
    def test_gua_dou_account_list_mobile(self, account_type, search):
        """
        查询呱豆列表,关键字为手机号
        :return:
        """
        res = self.eshop_admin_trade_account.api_account_list(account_type=account_type, search=search)
        # 断言获取结算列表是否正确
        assert res['code'] == 0
        # 断言该字典对象不为空
        assert res['data']['data'] != []

    @pytest.mark.parametrize("account_type, search", [('GUADOU', '***！！！！&&')])
    def test_gua_dou_account_list_other(self, account_type, search):
        """
        查询呱豆列表,关键字为其他不合法的字符
        :return:
        """
        res = self.eshop_admin_trade_account.api_account_list(account_type=account_type, search=search)
        # 断言获取结算列表是否正确
        assert res['code'] == 0
        # 断言返回结果为空list
        assert res['data']['data'] == []

    @pytest.mark.parametrize("account_type, search", [('GUADOU', None)])
    def test_gua_dou_account_list_page(self, account_type, search):
        """
        列表翻页查询
        :return:
        """
        res = self.eshop_admin_trade_account.api_account_list(account_type=account_type, search=search, page=2)
        # 断言获取结算列表是否正确
        assert res['code'] == 0
        # 断言返回结果页数一致
        assert res['data']['page'] == 2

    @pytest.mark.parametrize("balance_type", [None, 'AVAILABLE', 'FREEZE'])
    @pytest.mark.parametrize("operate_type", [None, 'ADD', 'SUB'])
    @pytest.mark.parametrize("account_type, start_create_time, end_create_time", [('GUADOU', '2021-05-01', '2021-06-01')])
    def test_gua_dou_account_detail_list(self, account_type, balance_type, operate_type, start_create_time,
                                         end_create_time):
        """
        查询呱豆明细列表,不同查询条件的结果
        """
        user_info = self.eshop_admin_trade_account.api_account_list(account_type='GUADOU', search='15921992382')
        user_no = user_info['data']['data'][0]['userNo']
        res = self.eshop_admin_trade_account.api_account_detail_list(account_type=account_type,
                                                                     operate_type=operate_type, user_no=user_no,
                                                                     start_create_time=start_create_time,
                                                                     balance_type=balance_type,
                                                                     end_create_time=end_create_time)
        # 将当前列表包含的账户类型balance_type值组合成一个集合
        balance_type_set = set([balanceType['balanceType'] for balanceType in res['data']['data']])
        # 将当前列表包含的变动类型operate_type值组合成一个集合
        operate_type_set = set([operateType['operateType'] for operateType in res['data']['data']])

        if balance_type is not None:
            # 断言获取呱豆明细列表接口返回成功
            assert res['code'] == 0
            # 断言账户类型是否正确
            assert balance_type_set in [{balance_type}, set()]
        else:
            # 断言获取呱豆明细列表接口返回成功
            assert res['code'] == 0
            # 断言账户类型是否正确
            assert balance_type_set.issubset({'AVAILABLE', 'FREEZE'})

        if operate_type is not None:
            # 断言获取呱豆列表是否正确
            assert res['code'] == 0
            # 断言操作类型是否正确
            assert operate_type_set in [{operate_type}, set()]
        else:
            # 断言获取呱豆列表是否正确
            assert res['code'] == 0
            # 断言操作类型是否正确
            assert operate_type_set.issubset({'ADD', 'SUB'})

    @pytest.mark.parametrize("account_type", ['GUADOU'])
    def test_gua_dou_account_detail_list_page(self, account_type):
        """
        明细翻页查询
        :return:
        """
        # 先查询到手机号为15921992382的呱豆账号
        user_info = self.eshop_admin_trade_account.api_account_list(account_type='GUADOU', search='15921992382')
        user_no = user_info['data']['data'][0]['userNo']
        # 查看该手机号的呱豆明细并翻页
        res = self.eshop_admin_trade_account.api_account_detail_list(account_type=account_type, user_no=user_no, page=2)
        # 断言获取明细列表是否正确
        assert res['code'] == 0
        # 断言返回结果页数一致
        assert res['data']['page'] == 2

    @pytest.mark.parametrize("adjust_type", ['LEAK_ORDER', 'COMPLAINOF_AWAY', 'ADDITIONAL_GIFTS'])
    @pytest.mark.parametrize("account_type, operate_type, adjust_amount, remark", [('GUADOU', 'ADD', 1800,
                                                                                    '自动化测试增加呱豆')])
    def test_add_gua_dou(self, account_type, adjust_type, operate_type, adjust_amount, remark):
        """
        根据不同方式给该账号充值18个呱豆，LEAK_ORDER-漏单，COMPLAINOF_AWAY-投诉赠送，ADDITIONAL_GIFTS-额外赠送
        """

        user_info = self.eshop_admin_trade_account.api_account_list(account_type='GUADOU', search='15921992382')
        user_no = user_info['data']['data'][0]['userNo']

        res_detail = self.eshop_admin_trade_account.api_account_detail_list(account_type=account_type,
                                                                            operate_type=operate_type, user_no=user_no)

        res_add = self.eshop_admin_trade_account.api_manual_adjust_account(account_type=account_type, user_no=user_no,
                                                                           operate_type=operate_type,
                                                                           adjust_type=adjust_type, remark=remark,
                                                                           adjust_amount=adjust_amount)
        # 断言增加呱豆成功
        assert res_add['code'] == 0
        # 断言呱豆明细列表最新的一条操作类型是新增
        assert res_detail['data']['data'][0]['operateType'] == 'ADD'

    @pytest.mark.parametrize("adjust_type", ['COMPLAINRE_REFUND', 'OTHER_SUB'])
    @pytest.mark.parametrize("account_type, operate_type, adjust_amount, remark", [('GUADOU', 'SUB', 1700,
                                                                                    '自动化测试扣减呱豆')])
    def test_sub_gua_dou(self, account_type, adjust_type, operate_type, adjust_amount, remark):
        """
        根据不同方式给该账号减少17个呱豆，COMPLAINRE_REFUND-投诉退款，OTHER_SUB-其他扣减
        """

        user_info = self.eshop_admin_trade_account.api_account_list(account_type='GUADOU', search='15921992381')
        user_no = user_info['data']['data'][0]['userNo']

        res_detail = self.eshop_admin_trade_account.api_account_detail_list(account_type=account_type,
                                                                            operate_type=operate_type, user_no=user_no)

        res_sub = self.eshop_admin_trade_account.api_manual_adjust_account(account_type=account_type, user_no=user_no,
                                                                           operate_type=operate_type,
                                                                           adjust_type=adjust_type, remark=remark,
                                                                           adjust_amount=adjust_amount)
        # 断言扣减呱豆成功
        assert res_sub['code'] == 0
        # 断言呱豆明细列表最新的一条操作类型是扣减
        assert res_detail['data']['data'][0]['operateType'] == 'SUB'







