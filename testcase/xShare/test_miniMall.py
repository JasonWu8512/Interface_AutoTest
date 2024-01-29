# coding=utf-8
# @Time    : 2020/9/10 1:18 下午
# @Author  : keith
# @File    : test99

import time
import pytest
import pytest_check as check

from business.Jiliguala.pay.ApiPingppOrder import ApiPingppOrder, Domains
from business.xshare.ApiMiniMall import ApiMiniMall
from business.Jiliguala.user.ApiUser import ApiUser
from business.common.UserProperty import UserProperty
from business.zero.mock.ApiMock import ApiMock
from business.zero.dataTool.ApiPromoterData import ApiPromoterData


@pytest.mark.xShare
@pytest.mark.minimall
class TestMiniMall(object):

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.account = cls.config["account"]
        cls.users = UserProperty(cls.account["mobile"])
        # user实例
        cls.user = ApiUser()
        cls.uid = cls.users.openuser_uid
        cls.pay_token = cls.users.basic_auth
        cls.sp99_token = cls.users.sp99_token
        # 转介绍小程序实例
        cls.mini = ApiMiniMall(token=cls.sp99_token)
        # 支付实例
        cls.pay = ApiPingppOrder(token=cls.pay_token)
        # Mock实例
        cls.mock = ApiMock()
        # 打开mock
        cls.mock.api_update_mock_status(status=True, env=cls.config["env"])
        # zero数据初始化实例
        cls.promoter_dataTool = ApiPromoterData()
        cls.wx_app_99_item = {
            "itemid": "H5_XX_Sample_XCX",
            "openapp": "sp99",
            "campaign": "NA",
            "purchaseType": "A"
        }
        # 退款99实例
        #cls.refund_pay = ApiPingppOrder(token=cls.config['refund_token'])

    @classmethod
    def teardown_class(cls):
        cls.mock.api_update_mock_status(status=True, env=cls.config["env"])

    def __delete_user_buy(self, oid, mobile):
        """删除用户购买记录"""
        # self.refund_pay.api_order_refund(oid)  # 对订单进行退款
        self.promoter_dataTool.api_set_promoter_data(env=self.config['env'], operation='delete_user_purchase_record',
                                                     mobile=mobile)  # 删除订单记录

    @pytest.fixture(scope='class')
    def create_physical_order(self):
        """创建订单"""
        order = self.pay.api_put_physical_order(itemid=self.wx_app_99_item["itemid"], openuid=self.users.openuser_uid,
                                                purchaseType=self.wx_app_99_item["purchaseType"],
                                                openapp=self.wx_app_99_item["openapp"],
                                                campaign=self.wx_app_99_item["campaign"])
        return order

    def test_wechat_bind_status(self):
        """
        微信和手机已绑定账号，测试绑定状态
        :return:
        """
        resp = self.mini.api_get_mobile_bind_status()
        check.equal(resp['data']['success'], True)

    def test_wechat_app_create_99_order(self, create_physical_order):
        """测试成功创建9.9订单"""
        try:
            oid = create_physical_order["data"]['_id']
            time.sleep(2)
            # 断言订单
            check.equal(create_physical_order["data"]['amount'], 990)
            check.equal(create_physical_order["data"]['openapp'], "sp99")
            check.equal(create_physical_order["data"]['status'], "notpaid")
            check.equal(create_physical_order["data"]['itemid'], self.wx_app_99_item["itemid"])
            check.equal(create_physical_order["data"]['openuid'], self.users.openuser_uid)
            # 获取订单详情
            order_info = self.mini.api_get_order_info()['data']
            # 断言订单详情
            check.equal(order_info['uid'], self.uid)
            check.equal(order_info['itemid'], self.wx_app_99_item["itemid"])
            check.equal(order_info['openapp'], self.wx_app_99_item["openapp"])
        finally:
            self.__delete_user_buy(oid, self.users.mobile)

    def test_wechat_app_charge_order(self, create_physical_order):
        """测试小程序成功支付9.9"""
        try:
            oid = create_physical_order["data"]['_id']
            time.sleep(2)
            # 支付小程序9.9订单
            print(time.asctime(time.localtime(time.time())))
            resp = self.pay.api_physical_order_charge(oid=oid, channel="wx_lite", openid=self.users.sp99_openid)["data"]
            check.equal(resp["order_no"], oid)
            check.equal(resp["amount"], 990)
            check.equal(resp["paid"], True)
            check.equal(resp["channel"], "wx_lite")
        finally:
            self.__delete_user_buy(oid, self.users.mobile)

    def test_wechat_app_charge_order_failed(self, create_physical_order):
        """测试已购9.9体验课后再次购买"""
        try:
            oid = create_physical_order["data"]['_id']
            # 支付小程序9.9订单
            payment = self.pay.api_physical_order_charge(oid=oid, channel="wx_lite", openid=self.users.sp99_openid)["data"]
            check.equal(payment["paid"], True)
            time.sleep(3)
            order = self.pay.api_put_physical_order(itemid=self.wx_app_99_item["itemid"],
                                                    openuid=self.users.openuser_uid,
                                                    purchaseType=self.wx_app_99_item["purchaseType"],
                                                    openapp=self.wx_app_99_item["openapp"],
                                                    campaign=self.wx_app_99_item["campaign"])
            check.equal(order["msg"], "已购买过体验课")
        finally:
            self.__delete_user_buy(oid, self.users.mobile)


if __name__ == '__main__':
    a = TestMiniMall()
    a.setup_class()
    a.test_wechat_app_create_99_order()
