# @Time    : 2021/4/1 5:07 下午
# @Author  : ygritte
# @File    : test_client

import pytest
import datetime
import time

from config.env.domains import Domains
from business.mysqlQuery import SaturnQuery
from business.common.UserProperty import UserProperty
from business.saturn.ApiChannel import ApiChannel
from business.saturn.ApiProduct import ApiProduct
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.zero.mock.ApiMock import ApiMock
from business.saturn.ApiPlanner import ApiPlanner


class TestClient:
    """
    下沉-c端业务
    """

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.satutnquery = SaturnQuery()
        cls.mock = ApiMock()
        cls.mock.api_update_mock_status(status=True, env=cls.config['env'], server_list=["交易中台"], user_email="ygritte_cao@jiliguala.com")  # 开启mock
        time.sleep(30)
        cls.user1 = UserProperty(cls.config['saturn']['user1'])  # 构建还未与成员锁粉的用户user实例，用于测试锁粉场景
        # cls.user2 = UserProperty(cls.config['saturn']['user2'])  # 构建还未购买正价课的锁粉用户user实例，用于测试购买正价课场景
        cls.user3 = UserProperty(cls.config['saturn']['user3'])  # 构建还未购买正价课的锁粉用户user实例，用于测试分配规划师的场景
        cls.channel1 = ApiChannel(authorization=cls.user1.basic_auth)  # 构建用户与员工锁粉的channel实例，用于锁粉场景
        cls.product = ApiProduct(authorization=cls.user1.basic_auth)  # 构建用户锁粉后进入商品列表的实例,用户商品列表展示场景
        cls.planner = ApiPlanner()  # 构建分配规划师的实例，用于测试锁粉用户购买正价课后分配规划师的场景

    @classmethod
    def teardown_class(cls):
        """
        恢复已锁粉数据并关闭mock
        """
        cls.mock.api_update_mock_status(status=False, env=cls.config['env'], server_list=["交易中台"], user_email="ygritte_cao@jiliguala.com")  # 关闭mock
        cls.satutnquery.delete_data("DELETE from saturn_user_account_fans where fan_mobile = '17777766666'")  # 删除锁粉表里的数据

    @pytest.fixture(scope="class")
    def get_channel_token(self):
        channel3 = ApiChannel()
        re = channel3.api_admin_login(username="autoTest", password="1234567")
        yield re['data']['token']

    def buy_lesson(self, sp2xuId, payPrice, channel, payTotal):
        """锁粉用户购买正价课"""
        fan_token = self.user3.basic_auth
        fan_purchase = ApiNewOrders(token=fan_token)
        fan_purchase_create_order = fan_purchase.api_order_create(sp2xuId=sp2xuId, payPrice=payPrice, useGuadou=False)
        order_no = fan_purchase_create_order['data']['orderNo']
        fan_purchase_charge = fan_purchase.api_charge_create(oid=order_no, channel=channel, payTotal=payTotal)
        return fan_purchase_charge

    @staticmethod
    def get_cur_month(self):
        """
        获取当前的年月日
        """
        month = datetime.datetime.now().strftime('%Y-%m')
        return month

    @pytest.mark.parametrize("staff_channel", ["424231e5d4184b17898612f03eefabac"])
    def test_bind_success(self, staff_channel, get_channel_token):
        """
        下沉渠道的锁粉条件：
        用户未与转推测锁粉，
        未拥有正价课，
        未与其他下沉成员锁粉
        """
        channel2 = ApiChannel(token=get_channel_token)  # 构建代理商管理系统获取线索管理的channel实例，用于获取粉丝列表
        res = self.channel1.api_bind(channel=staff_channel)
        res1 = channel2.api_employee_fans()  # B端的线索管理员工粉丝接口
        li = res1['data']['list']
        li.sort(key=lambda x: x['lockTime'], reverse=True)  # 将线索管理接口得到的列表按照锁粉时间倒序展示
        assert self.config['saturn']['user1'] == li[0]['mobile']  # 将线索管理接口里最新锁粉成功的用户手机号和锁粉手机号对比
        assert res["msg"] == "ok"

    def test_list(self):
        """
        锁粉成功的用户进入c端商品列表页
        """
        res = self.product.api_product_list()
        total = self.satutnquery.query_tables("SELECT COUNT(*) from saturn_product_col_item_map")  # 查询商品集合与商品映射表里的数据
        assert res["msg"] == "ok"
        assert res["data"]["total"] == total[0]["COUNT(*)"]

    # @pytest.mark.parametrize("sp2xuId, payPrice, channel, payTotal", [(2143, 48800, "wx_pub", 48800)])
    # def test_fan_revenue(self, sp2xuId, payPrice, channel, payTotal, get_channel_token):
    #     """
    #     已锁粉用户购买正价课获得50%的分佣
    #     """
    #     self.channel4 = ApiChannel(token=get_channel_token)  # 构建代理商管理系统获取业绩查询的channel实例，用于获取业绩列表
    #     res = self.buy_lesson(sp2xuId, payPrice, channel, payTotal)  # 锁粉用户购买正价课
    #     查询商品集合与商品映射表里的数据
    #     revenue = self.satutnquery.query_tables("SELECT revenue_amount from saturn_account_achievements where fan_mobile = '17777799999'")
    #     res1 = self.channel4.api_achievement_monthly_query(self.get_cur_month())
    #     li = res1['data']['list']['detail']
    #     li.sort(key=lambda x: x['dealTime'], reverse=True)  # 将业绩查询接口得到的列表按照成交时间倒序展示
    #     assert li[0]['revenue'] == revenue[0]["revenue_amount"]  # 将业绩查询接口里最新交易成功的用户佣金和数据库查询到的佣金对比
    #     assert res1["code"] == 0
    #     assert res1["msg"] == "ok"
    #     # # 退款购买记录，还原测试数据
    #     # self.mock.api_refund_mock(chargeid=res['data']['id'])

    @pytest.mark.parametrize("sp2xuId, payPrice, channel, payTotal, uid, subject",
                             [(2302, 48800, "wx_pub", 48800, "1d37b5825a804c22a6b684f63e6167a4", "english")])
    def test_get_planner(self, sp2xuId, payPrice, channel, payTotal, uid, subject):
        """
        已锁粉用户购买正价课后分配下沉规划师
        """
        # 锁粉用户购买正价课
        res_user_buy_lesson = self.buy_lesson(sp2xuId, payPrice, channel, payTotal)
        # 下沉侧查询购买正价课的用户分配的下沉规划师
        res_user_get_planner = self.planner.api_planner_get(uid, subject)
        # crm侧查询购买正价课的用户分配的下沉规划师
        res_crm_get_user_planner = self.planner.api_crm_get_planner(uid=uid, subject_type=subject)
        assert res_user_get_planner['data']['ghsId'] == res_crm_get_user_planner['data']['ghs_id']
        assert res_user_get_planner['data']['group'] == res_crm_get_user_planner['data']['group']
        assert res_user_get_planner['msgCode'] == '200'
        # 退款购买记录，还原测试数据
        self.mock.api_refund_mock(chargeid=res_user_buy_lesson['data']['id'])









