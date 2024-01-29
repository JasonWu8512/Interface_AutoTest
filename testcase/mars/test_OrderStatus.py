# coding=utf-8
# @Time    : 2021/4/01
# @Author  : jing_zhang
# @File    : test_OrderStatus.py

import pytest
import pytest_check as check
from business.common.UserProperty import UserProperty
from business.mars.ApiMyOrderListAndAddressAndTutor import ApiMyOrderList
from config.env.domains import Domains
from datetime import date, timedelta, datetime
from business.zero.mock.ApiMock import ApiMock
from business.businessQuery import xshareQuery,pingxxorderQuery


@pytest.mark.xShare
@pytest.mark.Mars
@pytest.mark.OrderList
class TestOrderList(object):
    dm = Domains()
    mock = ApiMock()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['url'])
        cls.zjk_user = UserProperty(cls.config['xshare_99_user']['zjk_user'])  # 买过正价课
        cls.two_orders_user = UserProperty(cls.config['xshare_99_user']['two_orders_user'])  # 两个体验课订单
        cls.lb_order_user = UserProperty(cls.config['xshare_99_user']['lb_order_user'])  # 联报订单
        cls.refund_user = UserProperty(cls.config['xshare_99_user']['refund_user'])  # 退款订单
        cls.needaddress_user = UserProperty(cls.config['xshare_99_user']['needaddress_user'])  # needaddress订单
        cls.no_tutor_bind_user = UserProperty(cls.config['xshare_99_user']['no_tutor_bind_user'])  # 没加班主任订单
        cls.order_sort_user = UserProperty(cls.config['xshare_99_user']['order_sort_user'])  # 测排序的用户
        cls.fill_address_user = UserProperty(cls.config['xshare_99_user']['fill_address_user']) # 测填地址的用户
        cls.db_xshare = xshareQuery()


    def get_resp(self, user):
        auth_token = user.basic_auth
        myorderlist = ApiMyOrderList(auth_token=auth_token)
        resp = myorderlist.get_order_list()
        return resp



    def test_zjk_user_orderlist(self):
        """"
        买过正价课呱美和思维课，我的订单列表是空的
        """
        resp = self.get_resp(self.zjk_user)
        check.equal(resp['status_code'], 200)
        check.equal(resp['data'], [])

    def test_orderlist_status(self):
        """"
        订单状态列表的订单状态paid或refund、needaddress
        """
        resp1 = self.get_resp(self.two_orders_user)
        check.equal(resp1['status_code'], 200)
        resp2 = self.get_resp(self.lb_order_user)
        check.equal(resp2['status_code'], 200)
        resp3 = self.get_resp(self.refund_user)
        check.equal(resp3['status_code'], 200)
        order_list = resp1['data'] + resp2['data'] + resp3['data']
        # if order_list!=[]:
        for order in order_list:
            # print(order['status'])
            assert order['status'] in ['paid', 'refunded', 'needaddress']

    def test_two_orders_bind_tutor(self):
        """"
        18812340001，两个体验课订单，一个已支付已填地址已加班主任，另一个已加班主任未填地址
        """
        resp = self.get_resp(self.two_orders_user)
        check.equal(resp['status_code'], 200)
        # print(resp['data'])
        for order in resp['data']:
            check.equal(order['tutorBindSet'], True)
            if order['oid'] == 'O44195710496935936':
                check.equal(order['status'], 'needaddress')
                check.equal(order['payPrice'], '6.0')
                check.equal(order['skuList'][0]['ttl'], '呱呱思维趣味AI互动课K1')
            else:
                check.equal(order['status'], 'paid')
                check.equal(order['payPrice'], '9.9')
                check.equal(order['skuList'][0]['ttl'], '呱呱美语趣味AI互动课K1')

    def test_lb_order_bind_tutor(self):
        """"
        18812340002，联报订单，已支付已填地址已加班主任
        """
        resp = self.get_resp(self.lb_order_user)
        check.equal(resp['status_code'], 200)
        # print(resp['data'])
        for order in resp['data']:
            check.equal(order['tutorBindSet'], True)
            # print(order)
            check.equal(order['oid'], 'O44195914801483776')
            check.equal(order['status'], 'needaddress')
            check.equal(order['payPrice'], '15.9')
            check.equal(order['skuList'][0]['ttl'], '呱呱英语+思维趣味AI互动课')



    def is_period_end(self, period):
        """
        判断当前时间运营期是否已结束，
        True：已结束，false：未结束
        """
        today = date.today().strftime("%Y%m%d")
        today = datetime.strptime(today, "%Y%m%d")
        end_time = datetime.strptime(period, "%Y%m%d") + timedelta(days=7)
        # print(today>end_time)
        if end_time >= today:
            return False
        else:
            return True

    def test_needaddress_after_endtime(self):
        """"
        18812340004，未填地址（两笔体验课订单），运营期已结束，断言填地址状态
        判断运营期是否已结束
        1.已结束，直接断言
        2.未结束，更新字段成已结束
        """
        uid = '82bb4f8d38ad4e1e96452304a9ab43df'
        data = self.db_xshare.get_tutor_bind_period(uid)
        subjectlist = []
        period_list = []
        for x in data:
            subjectlist.append(x['subjectType'])
            period_list.append(x['performance_period'])
        # print(subjectlist,period_list)
        for i in range(len(subjectlist)):
            period = period_list[i]
            subjectType = subjectlist[i]
            if self.is_period_end(period) == False:  # 运营期未结束
                period = (date.today() + timedelta(days=-8)).strftime("%Y%m%d")
                self.db_xshare.update_tutor_bind_period(uid, period, subjectType)  # 运营期变成结束
        resp = self.get_resp(self.needaddress_user)
        check.equal(resp['status_code'], 200)
        # print(resp['data'])
        for order in resp['data']:
            check.equal(order['status'], 'needaddress')

    def test_needaddress_before_endtime(self):
        """"
        18812340004，未填地址（两笔体验课订单），运营期未结束，断言填地址状态
        判断运营期是否已结束
        1.未结束，直接断言
        2.已结束，更新字段成未结束
        """
        uid = '82bb4f8d38ad4e1e96452304a9ab43df'
        data = self.db_xshare.get_tutor_bind_period(uid)
        subjectlist = []
        period_list = []
        for x in data:
            subjectlist.append(x['subjectType'])
            period_list.append(x['performance_period'])
        # print(subjectlist,period_list)
        for i in range(len(subjectlist)):
            period = period_list[i]
            subjectType = subjectlist[i]
            if self.is_period_end(period) == True:  # 运营期已结束
                period = (date.today() + timedelta(days=8)).strftime("%Y%m%d")
                self.db_xshare.update_tutor_bind_period(uid, period, subjectType)  # 运营期变成未结束
        resp = self.get_resp(self.needaddress_user)
        check.equal(resp['status_code'], 200)
        # print(resp['data'])
        for order in resp['data']:
            check.equal(order['status'], 'needaddress')

    def test_orderlist_sort(self):
        """"
        P2，订单列表按时间倒序排序，相同时间的已支付>已退款，用户
        """
        resp = self.get_resp(self.order_sort_user)
        check.equal(resp['status_code'], 200)
        payTime_list = []
        for x in resp['data']:
            payTime_list.append(x['payTime'])
        # print(payTime_list)
        if len(payTime_list) > 1:
            assert resp['data'][0]['payTime'] > resp['data'][1]['payTime']

    def test_tutorNotBind_before_endtime(self):
        """"
        18812340005，未加班主任（两笔体验课订单），运营期未结束，断言可以加班主任
        判断运营期是否已结束
        1.未结束，直接断言
        2.已结束，更新字段成未结束
        """
        uid = '0d15defb53dc4bfd843ad1a632e81316'
        data = self.db_xshare.get_tutor_bind_period(uid)
        subjectlist = []
        period_list = []
        for x in data:
            subjectlist.append(x['subjectType'])
            period_list.append(x['performance_period'])
        # print(subjectlist,period_list)
        for i in range(len(subjectlist)):
            period = period_list[i]
            subjectType = subjectlist[i]
            if self.is_period_end(period) == True:  # 运营期已结束
                period = (date.today() + timedelta(days=8)).strftime("%Y%m%d")
                self.db_xshare.update_tutor_bind_period(uid, period, subjectType)  # 运营期变成未结束
        resp = self.get_resp(self.no_tutor_bind_user)
        check.equal(resp['status_code'], 200)
        # print(resp['data'])
        for order in resp['data']:
            check.equal(order['tutorBindSet'], False)

    def test_tutorNotBind_after_endtime(self):
        """"
        18812340005，未加班主任（两笔体验课订单），运营期已结束，断言不可以加班主任
        判断运营期是否已结束
        1.已结束，直接断言
        2.未结束，更新字段成已结束
        """
        uid = '0d15defb53dc4bfd843ad1a632e81316'
        data = self.db_xshare.get_tutor_bind_period(uid)
        subjectlist = []
        period_list = []
        for x in data:
            subjectlist.append(x['subjectType'])
            period_list.append(x['performance_period'])
        # print(subjectlist,period_list)
        for i in range(len(subjectlist)):
            period = period_list[i]
            subjectType = subjectlist[i]
            if self.is_period_end(period) == False:  # 运营期未结束
                period = (date.today() + timedelta(days=-8)).strftime("%Y%m%d")
                self.db_xshare.update_tutor_bind_period(uid, period, subjectType)  # 运营期变成结束
        resp = self.get_resp(self.no_tutor_bind_user)
        check.equal(resp['status_code'], 200)
        # print(resp['data'])
        for order in resp['data']:
            check.equal(order['tutorBindSet'], True)
