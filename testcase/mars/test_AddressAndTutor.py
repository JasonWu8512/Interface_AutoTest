# coding=utf-8
# @Time    : 2021-4-13 13:39 
# @Author  : jing_zhang
# @File    : test_AddressAndTutor.py
# @Software: PyCharm

import pytest
import pytest_check as check
from business.common.UserProperty import UserProperty
from business.mars.ApiMyOrderListAndAddressAndTutor import ApiPostAddress, ApiTutorInfo
from business.mars.ApiOrder import ApiOrder
from config.env.domains import Domains
from business.zero.mock.ApiMock import ApiMock
from business.businessQuery import xshareQuery, pingxxorderQuery, lessonQuery
from utils.format.format import now_timeStr
from business.mysqlQuery import EshopQuery
from business.CrmQuery import CrmThrallQuery
import time
from business.Trade.tradeOrder.ApiRefundOpenFeign import ApiRefund


@pytest.mark.xShare
@pytest.mark.Mars
@pytest.mark.AddressAndTutor
class TestAddressAndTutor(object):
    dm = Domains()
    mock = ApiMock()

    @classmethod
    def setup_class(cls):
        # print('@' * 25 + 'setup_print' + '@' * 25)
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['url'])
        cls.purchase_user_one = UserProperty(cls.config['xshare_99_user']['purchase_user_one'])  # 买单科走流程的user
        cls.purchase_user_two = UserProperty(cls.config['xshare_99_user']['purchase_user_two'])  # 买双科走流程的user
        cls.db_xshare = xshareQuery()
        cls.db_pingxxorder = pingxxorderQuery()
        cls.eshop_db = EshopQuery()
        cls.db_lesson = lessonQuery()
        cls.crm_db = CrmThrallQuery()
        # 开个mock
        cls.mock = ApiMock()
        cls.mock.api_update_mock_status(status=True, env=cls.config['env'], server_list=['交易中台'],
                                        user_email='jing_zhang@jiliguala.com')
        time.sleep(150)
        cls.sp2xuId_list_value = cls.config['sp2xuId_list_value']


    @classmethod
    def teardown_class(cls):
        # 关个mock
        cls.mock.api_update_mock_status(status=False, env=cls.config['env'], server_list=['交易中台'],
                                        user_email='jing_zhang@jiliguala.com')

    def address_resp(self, user, oid=None):
        """
        @param user: 用户
        @param oid: 要填地址的订单号
        @return: response
        """
        auth_token = user.basic_auth
        address = ApiPostAddress(auth_token=auth_token)
        resp = address.post_address(oid=oid)
        return resp

    def tutor_resp(self, user, oid=None):
        """
        @param user: 用户
        @param oid: 要查班主任添加情况的订单号
        @param uid: 要查班主任添加情况的uid
        @return:
        """
        auth_token = user.basic_auth
        uid = user.user_id
        tutor = ApiTutorInfo(auth_token=auth_token)
        resp = tutor.get_tutor_info(oid=oid, uid=uid)
        return resp

    def purchase(self, user, sp2xuIds: list):
        """
        这个只是站外H5商城的购买，微信、小程序的都没写
        @param user:
        @return:
        """
        auth_token = user.basic_auth
        ord = ApiOrder(basic_auth=auth_token)
        res = ord.api_create_v2(item_id='H5_Sample_OutsideH5', nonce=now_timeStr(), source="ORGANIC_USER",
                                xshare_initiator=None,
                                sharer=None, sp2xuIds=sp2xuIds)
        check.equal(res['status_code'], 200)
        # print(res)
        re = ord.api_charge_v2(oid=res['data']['orderNo'], channel='wx_wap',
                               result_url="https://devt.jiliguala.com/test")
        time.sleep(1)
        check.equal(re['status_code'], 200)
        oid = res['data']['orderNo']
        return oid

    def delete_user_orders(self, user):
        """
        根据uid删除mongo和eshop,crm mysql相关数据，包括所有订单表、lessonbuy、班主任绑定、短信任务
        """
        uid = user.user_id
        self.eshop_db.delete_order_by_user_no(uid)
        self.crm_db.delete_leadsbind(uid)
        self.db_pingxxorder.delete_many_pingxxorder(uid)
        self.db_xshare.delete_tutor_bind_subject(uid)
        self.db_lesson.delete_lessonbuy(_id=uid)
        self.db_xshare.delete_sms_task(uid)


    def test_notpaid_post_address(self):
        """
        未支付订单填写地址
        """
        self.delete_user_orders(self.purchase_user_one)
        auth_token = self.purchase_user_one.basic_auth
        ord = ApiOrder(basic_auth=auth_token)
        res = ord.api_create_v2(item_id='H5_Sample_OutsideH5', nonce=now_timeStr(), source="ORGANIC_USER",
                                xshare_initiator=None,
                                sharer=None, sp2xuIds=self.sp2xuId_list_value['K1MATC_99'])
        check.equal(res['status_code'], 200)
        oid = res['data']['orderNo']
        resp = self.address_resp(self.purchase_user_one, oid)
        # print(resp)
        check.equal(resp['status_code'], 200)
        check.equal(resp['code'], 44104)
        check.equal(resp['msg'], '您还未支付订单，无法填写地址')

    def test_post_address_success(self):
        """已支付待填写地址单笔订单填写地址，可以正常填写成功"""
        self.delete_user_orders(self.purchase_user_one)
        oid = self.purchase(self.purchase_user_one, self.sp2xuId_list_value['K1MATC_99'])
        time.sleep(5)
        resp = self.address_resp(self.purchase_user_one, oid)
        check.equal(resp['status_code'], 200)
        db_res = self.db_pingxxorder.get_pingxxorder(_id=oid)
        address = db_res['receiver']
        print(address)
        check.equal(address['name'], '接口自动化测试')
        check.equal(address['tel'], '11111111111')
        check.equal(address['region'], '北京市 北京市 东城区')
        check.equal(address['addr'], '测试-接口自动化测试case地址')

    def test_already_post_address(self):
        """已支付已填写地址单笔订单填写地址，有错误提示"""
        # 这一块购买填地址
        self.delete_user_orders(self.purchase_user_one)
        oid = self.purchase(self.purchase_user_one, self.sp2xuId_list_value['K1MATC_99'])
        time.sleep(5)
        resp = self.address_resp(self.purchase_user_one, oid)
        # 这块再填一次
        resp = self.address_resp(self.purchase_user_one, oid)
        # print(resp)
        check.equal(resp['status_code'], 200)
        check.equal(resp['code'], 44106)
        check.equal(resp['msg'], '地址已填写，请勿重复提交')

    def test_one_tutor_info_show(self):
        """
        单科单订单paid状态，未加班主任，绑定状态断言
        """
        # 这一块购买填地址
        self.delete_user_orders(self.purchase_user_one)
        oid = self.purchase(self.purchase_user_one, self.sp2xuId_list_value['K1MATC_99'])
        time.sleep(5)
        self.address_resp(self.purchase_user_one, oid)
        resp = self.tutor_resp(self.purchase_user_one)
        check.equal(resp['status_code'], 200)
        check.equal(resp['data']['tutorList'][0]['subjectType'], 'LOGIC')
        check.equal(resp['data']['tutorList'][0]['tutorBindSet'], False)

    def test_one_tutor_bind(self):
        """
        单科单订单paid状态，未加班主任，把库改了，改成加班主任了，再断言
        """
        # 这一块购买填地址
        self.delete_user_orders(self.purchase_user_one)
        oid = self.purchase(self.purchase_user_one, self.sp2xuId_list_value['K1MATC_99'])
        time.sleep(5)
        self.address_resp(self.purchase_user_one, oid)
        time.sleep(2)
        self.db_xshare.update_tutor_bind_subject(self.purchase_user_one.user_id)
        resp = self.tutor_resp(self.purchase_user_one)
        # print(resp)
        check.equal(resp['status_code'], 200)
        check.equal(resp['data']['tutorList'][0]['subjectType'], 'LOGIC')
        check.equal(resp['data']['tutorList'][0]['tutorBindSet'], True)

    def test_refunded_post_address(self):
        """refunded状态再填地址"""
        # 这一块购买填地址
        self.delete_user_orders(self.purchase_user_one)
        oid = self.purchase(self.purchase_user_one, self.sp2xuId_list_value['K1MATC_99'])
        print(oid)
        time.sleep(5)
        self.address_resp(self.purchase_user_one, oid)
        # userid = self.purchase_user_one.user_id
        # db_res = self.db_pingxxorder.get_pingxxorder(uid=userid)
        # print(db_res['chargeid'], db_res['_id'])
        # chargeid = db_res['chargeid']
        # resp_refund = self.mock.api_refund_mock(chargeid)
        resp_refund = ApiRefund().api_order_refund(oid)
        check.equal(resp_refund['status_code'], 200)
        time.sleep(5)
        resp = self.address_resp(self.purchase_user_one, oid)
        check.equal(resp['status_code'], 200)
        check.equal(resp['code'], 44105)
        check.equal(resp['msg'], '您的订单已退款，无法填写地址')

    def test_post_address_two_success(self):
        """已支付待填写地址两笔订单填写地址，不传oid，地址一次写入两个订单成功"""
        self.delete_user_orders(self.purchase_user_two)
        oid1 = self.purchase(self.purchase_user_two, self.sp2xuId_list_value['K1GETC_99'])
        oid2 = self.purchase(self.purchase_user_two, self.sp2xuId_list_value['K1MATC_99'])
        time.sleep(5)
        resp = self.address_resp(self.purchase_user_two)
        check.equal(resp['status_code'], 200)
        oid_list = []
        oid_list.append(oid1)
        oid_list.append(oid2)
        for oid in oid_list:
            db_res = self.db_pingxxorder.get_pingxxorder(_id=oid)
            address = db_res['receiver']
            # print(address)
            check.equal(address['name'], '接口自动化测试')
            check.equal(address['tel'], '11111111111')
            check.equal(address['region'], '北京市 北京市 东城区')
            check.equal(address['addr'], '测试-接口自动化测试case地址')

    def test_two_tutor_bind_show(self):
        """
        两笔订单paid状态，未加班主任，绑定状态断言
        """
        # 买两个订单，填地址
        self.delete_user_orders(self.purchase_user_two)
        oid1 = self.purchase(self.purchase_user_two, self.sp2xuId_list_value['K1GETC_99'])
        oid2 = self.purchase(self.purchase_user_two, self.sp2xuId_list_value['K1MATC_99'])
        time.sleep(5)
        self.address_resp(self.purchase_user_two)
        # 再看班主任接口
        resp = self.tutor_resp(self.purchase_user_two)
        check.equal(resp['status_code'], 200)
        # print(resp)
        tutorList = resp['data']['tutorList']
        check.equal(len(tutorList), 2)
        for x in tutorList:
            assert x['subjectType'] == 'LOGIC' or x['subjectType'] == 'ENG'
            check.equal(resp['data']['tutorList'][0]['tutorBindSet'], False)

