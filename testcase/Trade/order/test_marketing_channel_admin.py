#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 3:48 下午
# @Author : liang_li
# @Site : 
# @File : test_marketing_channel_admin.py
# @Software: PyCharm

import pytest
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiMarketingChannels import ApiMarketingChannels
from business.mysqlQuery import EshopQuery


@pytest.mark.Trade
@pytest.mark.EshopAdmin
@pytest.mark.TradeCommodity
class TestMarketingChannelAdmin:
    """后台订单渠道管理相关用例"""
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_marketingChannel = ApiMarketingChannels(token=a_token)
        cls.EshopQuery = EshopQuery()

    def test_create_level1_MarketingChannel(self):
        """
        新增各级渠道
        """
        # 新增一级渠道
        channelNo1 = 'level1'
        name1 = '自动化测试一级渠道'
        level1 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=channelNo1, name=name1,
                                                                                parentId=0)
        print('level:', level1)
        assert level1['code'] == 0
        assert level1['data']['channelNo'] == channelNo1
        # 新增二级渠道
        level1_id = level1['data']['id']
        channelNo2 = 'level2'
        name2 = '自动化测试二级渠道'
        level2 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=channelNo2, name=name2,
                                                                                parentId=level1_id)
        assert level2['code'] == 0
        assert level2['data']['channelNo'] == channelNo2
        # 新增三级渠道
        level2_id = level2['data']['id']
        channelNo3 = 'level3'
        name3 = '自动化测试三级渠道'
        level3 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=channelNo3, name=name3,
                                                                                parentId=level2_id)
        assert level3['code'] == 0
        assert level3['data']['channelNo'] == channelNo3
        # 新增四级渠道
        level3_id = level3['data']['id']
        channelNo4 = 'level4'
        name4 = '自动化测试四级渠道'
        level4 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=channelNo4, name=name4,
                                                                                parentId=level3_id)
        assert level4['code'] == 0
        assert level4['data']['channelNo'] == channelNo4

    def test_get_level4_MarketingChannel(self):
        """
        查询各级渠道
        """
        # 查询出所有一级渠道
        level1 = self.eshop_admin_marketingChannel.api_get_marketing_channel()
        assert level1['code'] == 0
        level1_id = level1['data']['content'][0]['id']
        # 查询出一级渠道下所有二级渠道
        level2 = self.eshop_admin_marketingChannel.api_get_marketing_channel(parentId=level1_id)
        assert level2['code'] == 0
        level2_id = level2['data']['content'][0]['id']
        # 查询出一级渠道下所有三级渠道
        level3 = self.eshop_admin_marketingChannel.api_get_marketing_channel(parentId=level2_id)
        assert level3['code'] == 0
        level3_id = level3['data']['content'][0]['id']
        # 查询出一级渠道下所有四级渠道
        level4 = self.eshop_admin_marketingChannel.api_get_marketing_channel(parentId=level3_id)
        assert level4['code'] == 0

    def test_create_repeat_MarketingChannel(self):
        """
        新增已有渠道
        """
        # 新增已有一级渠道
        level1 = self.eshop_admin_marketingChannel.api_get_marketing_channel()
        level1_channelNo = level1['data']['content'][0]['channelNo']
        level1_name = level1['data']['content'][0]['name']
        level1_id = level1['data']['content'][0]['id']
        repeat_level1 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=level1_channelNo,
                                                                                       name=level1_name, parentId=0)
        assert repeat_level1['code'] == 30003
        assert repeat_level1['msg'] == '渠道 code 重复！'
        # 新增已有二级渠道
        level2 = self.eshop_admin_marketingChannel.api_get_marketing_channel(parentId=level1_id)
        level2_channelNo = level2['data']['content'][0]['channelNo']
        level2_name = level2['data']['content'][0]['name']
        level2_id = level2['data']['content'][0]['id']
        repeat_level2 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=level2_channelNo,
                                                                                       name=level2_name,
                                                                                       parentId=level1_id)
        assert repeat_level2['code'] == 30003
        assert repeat_level2['msg'] == '渠道 code 重复！'
        # 新增已有三级渠道
        level3 = self.eshop_admin_marketingChannel.api_get_marketing_channel(parentId=level2_id)
        level3_channelNo = level3['data']['content'][0]['channelNo']
        level3_name = level3['data']['content'][0]['name']
        level3_id = level3['data']['content'][0]['id']
        repeat_level3 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=level3_channelNo,
                                                                                       name=level3_name,
                                                                                       parentId=level2_id)
        assert repeat_level3['code'] == 30003
        assert repeat_level3['msg'] == '渠道 code 重复！'
        # 新增已有四级渠道
        level4 = self.eshop_admin_marketingChannel.api_get_marketing_channel(parentId=level3_id)
        level4_channelNo = level4['data']['content'][0]['channelNo']
        level4_name = level4['data']['content'][0]['name']
        repeat_level4 = self.eshop_admin_marketingChannel.api_create_marketing_channel(channelNo=level4_channelNo,
                                                                                       name=level4_name,
                                                                                       parentId=level3_id)
        assert repeat_level4['code'] == 30003
        assert repeat_level4['msg'] == '渠道 code 重复！'
    @pytest.mark.parametrize("channel_no", ['level1', 'level2', 'level3', 'level4'])
    def test_delete_marketing_channel(self, channel_no):
        """
        删除新增的渠道
        """
        # 删除新增的渠道
        self.EshopQuery.delete_marketing_channel_channel_no(channel_no=channel_no)