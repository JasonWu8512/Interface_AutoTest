#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/5/11 1:38 下午
# @Author : liang_li
# @Site : 
# @File : test_redeem_admin.py
# @Software: PyCharm

import pytest
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from utils.enums.businessEnums import EshopRedeemStateEnum
from business.Trade.eshopAdmin.ApiRedeem import ApiRedeem


@pytest.mark.Trade
@pytest.mark.EshopAdmin
@pytest.mark.TradeCommodity
@pytest.mark.TradeRedeem
class TestRedeemAdmin:
    """后台兑换码管理相关用例"""
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_commodity = ApiCommodity(token=a_token)
        cls.eshop_admin_redeem = ApiRedeem(token=a_token)

    @pytest.fixture(scope='class')
    def get_sgu_one_commodity(self):
        """获取一个SGU商品"""
        res = self.eshop_admin_commodity.api_get_sxu_list(sxuType=2, state=1)
        print("res:", res)
        sgu = res['data']['content'][0]
        return sgu

    def test_create_redeem(self, get_sgu_one_commodity):
        """
        生成兑换码
        """
        # 生成兑换码获取生成兑换码的SGU商品sguId与sguCommodityNo
        sguId = get_sgu_one_commodity['id']
        print("sguId:", sguId)
        sguCommodityNo = get_sgu_one_commodity['commodityNo']
        print("sguCommodityNo:", sguCommodityNo)
        # 生成兑换码
        create_redeem_list = self.eshop_admin_redeem.api_create_redeem(sguId=sguId)
        print("create_redeem_list:", create_redeem_list)
        # 断言调用生成兑换码接口是否成功
        assert create_redeem_list['code'] == 0
        # 断言生成兑换码的商品是否与所选商品一致
        assert create_redeem_list['data']['sguCommodityNo'] == sguCommodityNo

    def test_get_redeem_batch_list(self):
        """
        获取兑换码批次列表
        """
        # 获取兑换码批次列表
        redeem_batch_list = self.eshop_admin_redeem.api_get_redeem_batch_list()
        # 断言调用生成兑换码接口是否成功
        assert redeem_batch_list['code'] == 0

    def test_get_redeem_batches_detail(self, get_sgu_one_commodity):
        """
        获取兑换码批次详情
        """
        # 生成兑换码获取生成兑换码的SGU商品sguId与sguCommodityNo
        sguId = get_sgu_one_commodity['id']
        # 生成兑换码
        create_redeem_list = self.eshop_admin_redeem.api_create_redeem(sguId=sguId, num=10)
        # 获取生成兑换码批次id
        batchId = create_redeem_list['data']['id']
        # 获取生成兑换码的兑换码编号list
        redeemNo_list = create_redeem_list['data']['detailList']
        # 获取兑换码批次详情
        redeem_batches_detail = self.eshop_admin_redeem.api_get_redeem_batches_detail(batchId=batchId)
        # 断言获取兑换码批次详情接口是否成功
        assert redeem_batches_detail['code'] == 0
        # 断言生成兑换码时返回的兑换码编号与获取该批次兑换码详情时获取到的兑换码编号是否一致
        assert redeemNo_list == redeem_batches_detail['data']['detailList']

    @pytest.mark.parametrize("stateList", ['', 1, 2, 3])
    def test_get_redeem_info_state(self, stateList):
        """
        获取兑换码信息-根据使用状态查询
        """
        # 获取兑换码详细列表
        redeemNo_list = self.eshop_admin_redeem.api_get_redeem_info(stateList=stateList)
        # 兑换码详细列表包含的redeem兑换码状态
        redeemState_set = set([redeem['state'] for redeem in redeemNo_list['data']['list']])
        if stateList != '':
            assert redeemState_set in [{EshopRedeemStateEnum.get_chinese(stateList)}, set()]
        else:
            assert redeemState_set.issubset({1, 2, 3})

    def test_get_redeem_info_batchId(self):
        """
        获取兑换码信息-根据生成批次ID查询
        """
        # 获取兑换码批次列表并从其中拿出一个兑换码批次ID：batchId
        redeem_batch_list = self.eshop_admin_redeem.api_get_redeem_batch_list()
        batchId = redeem_batch_list['data']['list'][0]['id']
        # 获取兑换码批次详情
        redeem_batches_detail = self.eshop_admin_redeem.api_get_redeem_batches_detail(batchId=batchId)
        # 获取兑换码详细列表
        redeemNo_list = self.eshop_admin_redeem.api_get_redeem_info(batchId=batchId)
        redeemNo_info = set([redeemNo['redeemNo'] for redeemNo in redeemNo_list['data']['list']])
        # 断言根据生成批次ID查询出来的兑换码编号是否正确
        assert redeemNo_info == set(redeem_batches_detail['data']['detailList'])

    @pytest.mark.parametrize("redeemNoList", ['9e2XvrxnHxaWDn'])
    def test_get_redeem_info_redeemNo(self, redeemNoList):
        """
        获取兑换码信息-根据兑换码编号查询（另一账号的兑换码）
        """
        # 根据兑换码编号查询兑换码信息
        res = self.eshop_admin_redeem.api_get_redeem_info(redeemNoList=redeemNoList)
        # 断言根据兑换码编号查询出来的兑换码信息是否正确
        assert res['code'] == 0
        assert res['data']['list'][0]['redeemNo'] == redeemNoList

    def test_destroy_redeem(self):
        """
        销毁兑换码
        """
        # 获取兑换码详细列表
        redeemNo_list = self.eshop_admin_redeem.api_get_redeem_info(stateList=1)
        # 未使用的兑换码详细列表
        redeemState_set = list([redeem['redeemNo'] for redeem in redeemNo_list['data']['list']])
        # 取未使用兑换码详细列表list的前两个元素
        redeemState_set_list = redeemState_set[0:2]
        # 销毁兑换码
        destroy_redeem = self.eshop_admin_redeem.api_destroy_redeem(redeemNoList=redeemState_set_list)
        # 断言兑换码是否销毁成功
        assert destroy_redeem['code'] == 0
        # 断言销毁的兑换码是否正确
        assert destroy_redeem['data']['succeedList'] == redeemState_set_list
