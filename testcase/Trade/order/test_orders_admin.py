#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/8 5:52 下午
# @Author : liang_li
# @Site : 
# @File : test_orders_admin.py
# @Software: PyCharm

import pytest
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from utils.enums.businessEnums import EshopOrderStateEnum
from business.Trade.eshopAdmin.ApiOrders import ApiOrders
from utils.format.format import dateToTimeStamp, time
import time
import datetime


@pytest.mark.Trade
@pytest.mark.EshopAdmin
@pytest.mark.TradeOrder
class TestOrdersAdmin:
    """后台订单管理相关用例"""
    promotionId = None

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_order = ApiOrders(token=a_token)

    @pytest.fixture(scope='class')
    def get_query_time(self):
        """
        前置获取订单查询时间
        """
        query_time = []
        # 获取当前时间
        nowtime = datetime.datetime.now()
        # 将当前时间转换成毫秒级时间戳
        nowtime_stamp = int(round(time.mktime(nowtime.timetuple()) * 1000))
        # 当前时间-3天
        after_nowtime3 = nowtime + datetime.timedelta(days=-3)
        # 当前时间-3天后的毫秒级时间戳
        after_nowtime3_stamp = int(round(time.mktime(after_nowtime3.timetuple()) * 1000))
        query_time.append(after_nowtime3_stamp)
        query_time.append(nowtime_stamp)
        return query_time

    @pytest.fixture(scope='class')
    def get_one_order(self, get_query_time):
        """
        获取一个订单号
        """
        res = self.eshop_admin_order.api_get_orders(createAtAfter=get_query_time[0], createAtBefore=get_query_time[1])
        return res['data']['content'][0]['orderNo']

    @pytest.mark.parametrize("orderState", ['', 1, 2, 3, 4, 5, 6])
    @pytest.mark.parametrize("payChannel", ['', 'alipay_scan', 'alipay_lite', 'guadou', 'alipay_wap', 'iap', 'alipay_qr',
                                            'wx_pub_scan', 'wx_pub', 'alipay_pc_direct', 'wx_lite', 'free', 'wx_pub_qr',
                                            'alipay', 'huawei_iap', 'magika', 'diamond', 'wx', 'wx_wap'])
    def test_order_list(self, orderState, payChannel, get_query_time):
        """
        获取订单列表，不同的查询条件不同的结果
        """
        # 初始化支付方式
        payChannel_set = set()
        # 获取订单列表
        if payChannel == '':
            res = self.eshop_admin_order.api_get_orders(orderState=orderState, createAtAfter=get_query_time[0], createAtBefore=get_query_time[1])
        else:
            res = self.eshop_admin_order.api_get_orders(orderState=orderState, payChannel=payChannel,
                                                        createAtAfter=get_query_time[0],
                                                        createAtBefore=get_query_time[1])
            payChannel_set = set([order['payChannel'] for order in res['data']['content']])
        # 订单列表包含的orderState订单状态
        orderState_set = set([order['state'] for order in res['data']['content']])
        if orderState != '':
            assert orderState_set in [{EshopOrderStateEnum.get_chinese(orderState)}, set()]
            if orderState in (1, 6):
                assert payChannel_set in [set()]
        if payChannel != '':
            assert payChannel_set in [{payChannel}, set()]
        else:
            assert orderState_set.issubset({1, 2, 3, 4, 5, 6})
            assert payChannel_set.issubset({'alipay_scan', 'alipay_lite', 'guadou', 'alipay_wap', 'iap', 'alipay_qr',
                                            'wx_pub_scan', 'wx_pub', 'alipay_pc_direct', 'wx_lite', 'free', 'wx_pub_qr',
                                            'alipay', 'huawei_iap', 'magika', 'diamond', 'wx', 'wx_wap'})

    def test_order_detail(self, get_one_order):
        """
        查看订单详情
        """
        # 通过获取订单列表接口获取订单号
        orderNo = get_one_order
        # 查看该订单详情
        res = self.eshop_admin_order.api_get_orders_detail(orderNo=orderNo)
        # 断言调用查看详情接口是否成功
        assert res['code'] == 0
        # 断言查看详情获取的订单号是否与输入订单号一致
        assert orderNo == res['data']['orderNo']

    def test_again_orders_semester(self):
        """
        重新开课
        """
        # 查询订单
        orderNo_list = self.eshop_admin_order.api_get_orders(user='17521157698')
        # 遍历查询到的订单列表，如果有包含课程的订单，就重新开课
        for orderNo in orderNo_list['data']['content']:
            if orderNo['commodityCategory'] != 2:
                res = self.eshop_admin_order.api_again_orders_semester(orderNo=orderNo['orderNo'])
                assert res['code'] == 0
                break
            else:
                assert 0 == 1

