# coding=utf-8 
# @File     :   test_GroupPurchase.py
# @Time     :   2021/4/7 5:48 下午
# @Author   :   austin
# @Update   :   zhangjing 2021/4/29

import pytest
from business.Jiliguala.user.ApiUserInfo import ApiUserInfo
from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains
from business.businessQuery import usersQuery, xshareQuery, pingxxorderQuery
from business.xshare.ApiGroupPurchase import ApiGroupPurchase
from business.common.UserProperty import UserProperty
from random import choice
from business.mars.ApiOrder import ApiOrder
from business.zero.mock.ApiMock import ApiMock
from utils.format.format import now_timeStr
from business.mars.ApiPurchasepage import ApiPurchasepage
import time
import pytest_check as check
from business.mars.ApiMyOrderListAndAddressAndTutor import ApiPostAddress
from business.xshare.ApiDiamond import ApiDiamond
import threading
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.mysqlQuery import EshopQuery


@pytest.mark.xShare
class TestGroupPurchase:
    """
    拼团用例，执行用例前注意下是否在活动时间内
    """

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.mock = ApiMock()
        cls.user = ApiUser()
        cls.db_user = usersQuery()
        cls.db_purchase = xshareQuery()
        cls.mock.api_update_mock_status(status=True,
                                        env=cls.config['env'],
                                        server_list='交易中台',
                                        user_email='jing_zhang@jiliguala.com')
        time.sleep(150)
        # 开启mock，user_email如果注销了需重新添加
        cls.purchase_user_inviter1 = UserProperty(cls.config['xshare_group_purchase']['inviter1'])
        # 构建团长实例，用于后续团长auth。没开团资格
        cls.purchase_user_inviter2 = UserProperty(cls.config['xshare_group_purchase']['inviter2'])
        # 构建团长实例，用于后续团长auth。有开团资格
        cls.purchase_user_invitee1 = UserProperty(cls.config['xshare_group_purchase']['invitee1'])
        # 构建团长实例，用于后续团长auth。没参团资格
        cls.purchase_user_invitee2 = UserProperty(cls.config['xshare_group_purchase']['invitee2'])
        # 构建团长实例，用于后续团长auth。有参团资格
        cls.purchase_auth_inviter1 = cls.purchase_user_inviter1.basic_auth
        cls.purchase_auth_inviter2 = cls.purchase_user_inviter2.basic_auth
        cls.purchase_auth_invitee1 = cls.purchase_user_invitee1.basic_auth
        cls.purchase_auth_invitee2 = cls.purchase_user_invitee2.basic_auth
        cls.group_purchase_inviter1 = ApiGroupPurchase(token=cls.purchase_auth_inviter1)
        cls.group_purchase_inviter2 = ApiGroupPurchase(token=cls.purchase_auth_inviter2)
        cls.group_purchase_invitee1 = ApiGroupPurchase(token=cls.purchase_auth_invitee1)
        cls.group_purchase_invitee2 = ApiGroupPurchase(token=cls.purchase_auth_invitee2)
        cls.user_info = ApiUserInfo(token=cls.purchase_auth_inviter1)
        cls.old_user_order1 = ApiOrder(basic_auth=cls.purchase_auth_invitee1)
        cls.old_user_order2 = ApiOrder(basic_auth=cls.purchase_auth_invitee2)
        cls.old_user_commodity = ApiPurchasepage(basic_auth=cls.purchase_auth_invitee1)
        cls.gp_id1 = cls.config['xshare_group_purchase']['gpid1']  # 构建活动id实例，奖励为钻石的团
        cls.gp_id2 = cls.config['xshare_group_purchase']['gpid2']  # 构建活动id实例，奖励为实体的团
        cls.purchase_inviter1 = cls.config['xshare_group_purchase']['inviter1']  # 构建团长手机号实例，用于数据库操作
        cls.purchase_inviter2 = cls.config['xshare_group_purchase']['inviter2']  # 构建团长手机号实例，用于数据库操作
        cls.purchase_invitee2 = cls.config['xshare_group_purchase']['invitee2']  # 构建团员手机号实例，用于数据库操作
        cls.purchase_invitee1 = cls.config['xshare_group_purchase']['invitee1']  # 构建团员手机号实例，用于数据库操作
        cls.db_pingxxorder = pingxxorderQuery()  # 查pingxxorder表
        cls.sp2xuId_list_value = cls.config['sp2xuId_list_value']
        cls.gp_id3 = cls.config['xshare_group_purchase']['gpid3']  # 2人团
        cls.new_user_mobile = cls.config['xshare_group_purchase']['new_user']  # 每次会注销成为新用户
        cls.sp2xuId_Normal = cls.config["xshare"]["sp2xuId"]["sp2xuId_Normal"]  # 呱呱思维正价课
        cls.db_eshop = EshopQuery()
        price = cls.db_eshop.eshop.query(
            'select price_rmb from commodity where commodity_no ="Ian-Test-MA"'
        )  # 呱呱思维正价课价格
        cls.sp2xuId_pay_price = int(price[0]["price_rmb"])

    @classmethod
    def teardown_class(cls):
        """
        关闭mock
        """
        cls.mock.api_update_mock_status(status=False,
                                        env=cls.config['env'],
                                        server_list='交易中台',
                                        user_email='jing_zhang@jiliguala.com')  # 关闭mock

    def delete_db_inviter(self, mobile):
        """
        用于团长清数据,默认清inviter2的数据
        """
        get_uid = self.db_user.get_users(mobile=mobile)["_id"]
        # 根据手机号查询用户uid
        get_db_purchase = self.db_purchase
        get_purchase_order = get_db_purchase.get_xshare_group_purchase(inviterId=get_uid)
        # 根据uid查询团单
        while True:
            if get_purchase_order is not None:
                get_db_purchase.delete_xshare_group_purchase(inviterId=get_uid)
                # 删除团单
            break

    def create_phone(self):
        """
        随机生成有效手机号
        """
        area_num = ['187', '186', '186', '158', '155', '156', '138', '135', '136', '177', '176', '144', '147']
        # 获取手机号码区域号
        area_number = choice(area_num)
        # 生成后8位手机号码
        seed = "1234567890"
        sa = []
        for i in range(8):
            sa.append(choice(seed))
        last_eightnumber = ''.join(sa)
        phonen_number = area_number + last_eightnumber
        # 拼接生成完整手机号码
        return phonen_number

    def create_user(self):
        """
        用于造新用户
        """
        phone_number = self.create_phone()
        get_uid = self.db_user.get_users(mobile=phone_number)
        # 根据手机号查询用户uid
        while True:
            if get_uid is None:
                ApiUserInfo('').api_get_websms(mobile=phone_number)
                # 注册
            return phone_number

    @pytest.mark.parametrize("typ,u,p", [("mobilecode", "1871786771", "123")])
    def test_login_fail1(self, typ, u, p):
        """
        错误手机号错误验证码，登陆失败
        ps:手机号和验证码都为写死的错误手机号&错误验证码
        """
        login_res = self.user.api_app_login(typ=typ, u=u, p=p)
        assert login_res["code"] == 269
        # 判断登陆接口调用是否成功
        assert login_res["msg"] == "验证码错误"
        # 判断是否登陆成功

    @pytest.mark.parametrize("typ,p", [("mobilecode", "123")])
    def test_login_fail2(self, typ, p):
        """
        正确手机号错误验证码，登陆失败
        ps:p为写死的错误验证码
        """
        login_res = self.user.api_app_login(typ=typ, u=self.purchase_inviter2, p=p)
        assert login_res["code"] == 269
        # 判断登陆接口调用是否成功
        assert login_res["msg"] == "验证码错误"
        # 判断是否登陆成功

    @pytest.mark.parametrize("typ", [("mobilecode")])
    def test_login_success(self, typ):
        """
        正确手机号正确验证码，登陆成功
        """
        sms_post = self.user_info.api_get_websms(mobile=self.purchase_inviter2)
        # 发送验证码
        sms = self.db_user.get_users(mobile=self.purchase_inviter2)["sms"]["code"]
        # 查询验证码
        login_res = self.user.api_app_login(typ=typ, u=self.purchase_inviter2, p=sms)
        # 登陆
        assert login_res["code"] == 0
        # 判断登陆接口调用是否成功
        assert login_res["data"]["mobile"] == self.purchase_inviter2
        # 判断是否登陆成功

    # @pytest.mark.parametrize("gpid", [("gp_id")])
    def test_create_group_faild(self):
        """
        用户不符合开团资格，开团失败
        """
        create_group_faild = self.group_purchase_inviter1.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        # print(self.gp_id1)
        # print(create_group)
        assert create_group_faild["code"] == 0
        # 判断登陆接口调用是否成功
        assert create_group_faild["data"]["inviterQualified"] is False
        # 判断是否符合开团资格
        assert create_group_faild["data"]["gpOid"] == "NA"
        # 判断是否创建了团单

    def test_create_group_success(self):
        """
        用户符合开团资格，开团成功
        """
        get_uid = self.db_user.get_users(mobile=self.purchase_inviter2)["_id"]
        # 根据手机号查询用户uid
        delete = self.db_purchase.delete_xshare_group_purchase(inviterId=get_uid)
        # 根据uid删除团单
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        get_groupid = self.db_purchase.get_xshare_group_purchase(inviterId=get_uid)["_id"]
        # 获取刚创建的团id
        # print(test_create_group_success)
        assert create_group_success["code"] == 0
        # 判断登陆接口调用是否成功
        assert create_group_success["data"]["inviterQualified"] is True
        # 判断是否符合开团资格
        assert create_group_success["data"]["gpOid"] == get_groupid
        # 判断创建的团单是否和数据库查询的一致

    def test_create_group_faild2(self):
        """
        用户有该活动id下进行中的团，不能再次开团
        """
        get_uid = self.db_user.get_users(mobile=self.purchase_inviter2)["_id"]
        # 根据手机号查询用户uid
        delete = self.db_purchase.delete_xshare_group_purchase(inviterId=get_uid)
        # 根据uid删除团单
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        create_group_faild2 = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 再次创建团单
        # print(create_group_faild2)
        assert create_group_faild2["code"] == 0
        # 判断登陆接口调用是否成功
        assert create_group_faild2["data"]["inviterQualified"] is False
        # 判断是否符合开团资格
        assert create_group_faild2["data"]["gpOid"] == "NA"
        # 判断创建的团单是否和数据库查询的一致

    def test_create_group_success2(self):
        """
        用户该活动id下最新的团为拼团成功，能再次开团
        """
        get_uid = self.db_user.get_users(mobile=self.purchase_inviter2)["_id"]
        # 根据手机号查询用户uid
        delete = self.db_purchase.delete_xshare_group_purchase(inviterId=get_uid)
        # 根据uid删除团单
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        get_groupid = self.db_purchase.get_xshare_group_purchase(inviterId=get_uid)["_id"]
        # 获取刚创建的团id
        update_group_status = self.db_purchase.update_xshare_group_purchase(get_groupid, {'status': 'completed'})
        # 把之前创建的团单状态改成已完成
        create_group_success2 = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 再次开团
        # print(create_group_success2)
        get_groupid2 = self.db_purchase.get_many_xshare_group_purchase(inviterId=get_uid)[1]['_id']
        # 再次获取刚创建的团id
        # print(get_groupid2)
        assert create_group_success2["code"] == 0
        # 判断登陆接口调用是否成功
        assert create_group_success2["data"]["inviterQualified"] == True
        # 判断是否符合开团资格
        assert create_group_success2["data"]["gpOid"] == get_groupid2
        # 判断创建的团单是否和数据库查询的一致

    def test_create_group_success3(self):
        """
        用户该活动id下最新的团为已过期，能再次开团
        """
        get_uid = self.db_user.get_users(mobile=self.purchase_inviter2)["_id"]
        # 根据手机号查询用户uid
        delete = self.db_purchase.delete_xshare_group_purchase(inviterId=get_uid)
        # 根据uid删除团单
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        get_group = self.db_purchase.get_xshare_group_purchase(inviterId=get_uid)
        # 获取刚创建的团单
        update_group_status = self.db_purchase.update_xshare_group_purchase(get_group["_id"], {'ets': get_group["cts"]})
        # 把刚创建的团单改成：结束时间=创建时间
        create_group_success3 = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 再次开团
        # print(create_group_success2)
        get_groupid2 = self.db_purchase.get_many_xshare_group_purchase(inviterId=get_uid)[1]['_id']
        # 再次获取刚创建的团id
        # print(get_groupid2)
        assert create_group_success3["code"] == 0
        # 判断登陆接口调用是否成功
        assert create_group_success3["data"]["inviterQualified"] is True
        # 判断是否符合开团资格
        assert create_group_success3["data"]["gpOid"] == get_groupid2
        # 判断创建的团单是否和数据库查询的一致

    def test_pag_config(self):
        """
        用户登陆后，能查询到开团页图片配置
        """
        get_pag_config = self.group_purchase_inviter2.api_page_config(gpid=self.gp_id1)
        # 获得页面配置
        get_db_config = self.db_purchase.get_pintuan_config(gpid=self.gp_id1)
        # 获取数据库配置
        # print(get_pag_config)
        # print(get_db_config)
        assert get_pag_config["code"] == 0
        # 判断接口是否调用成功
        assert get_pag_config["data"]['gpid'] == get_db_config['gpid']
        # 判断返回的gpid是否正确
        assert get_pag_config["data"]['size'] == get_db_config['size']
        # 判断此团参团人数是否和数据库一致
        assert get_pag_config['data']['purchasePageSpu'] == get_db_config['purchasePageSpu']
        # 判断spu是否一致

    def test_inviter_order(self):
        """
        用户开团成功后，团长能查询到所开团的团详情
        """
        self.delete_db_inviter(mobile=self.purchase_inviter2)
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        print(create_group_success)
        create_groupid = create_group_success['data']['gpOid']
        # 获取创建团单的团单编号
        get_uid = self.db_user.get_users(mobile=self.purchase_inviter2)["_id"]
        # 根据手机号查询用户uid
        get_group = self.db_purchase.get_xshare_group_purchase(inviterId=get_uid)
        # 数据库获取刚创建的团单
        # print(get_group)
        get_inviter = self.group_purchase_inviter2.api_get_inviter_order(gpid=self.gp_id1, gpoid=create_groupid)
        # 团长查询团单
        print(get_inviter)
        assert get_inviter["code"] == 0
        # 判断接口是否调用成功
        assert get_inviter['data']["status"] == get_group['status']
        # 判断团单状态是否一致
        assert get_inviter['data']["gpOid"] == get_group['_id']
        # 判断团单是否一致
        assert get_inviter['data']["inviter"]['uid'] == get_group['inviterId']
        # 判断团长是否一致

    def test_invitee_order(self):
        """
        用户开团成功后，团员能查询到所开团的团详情
        """
        self.delete_db_inviter(mobile=self.purchase_inviter2)
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        # print(create_group_success)
        create_groupid = create_group_success['data']['gpOid']
        # 获取创建团单的团单编号
        get_uid = self.db_user.get_users(mobile=self.purchase_inviter2)["_id"]
        # 根据手机号查询用户uid
        get_group = self.db_purchase.get_xshare_group_purchase(inviterId=get_uid)
        # 数据库获取刚创建的团单
        # print(get_group)
        get_inviter = self.group_purchase_invitee2.api_get_invitee_order(gpid=self.gp_id1, gpoid=create_groupid)
        # 团员查询团单
        # print(get_inviter)
        assert get_inviter["code"] == 0
        # 判断接口是否调用成功
        assert get_inviter['data']["status"] == get_group['status']
        # 判断团单状态是否一致
        assert get_inviter['data']["gpOid"] == get_group['_id']
        # 判断团单是否一致
        assert get_inviter['data']["inviter"]['uid'] == get_group['inviterId']
        # 判断团长是否一致

    def test_join_faild1(self):
        """
        用户不符合参团资格且符合下单资格，不能参团成功
        """
        self.delete_db_inviter(mobile=self.purchase_inviter2)
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        # print(create_group_success)
        gpoid1 = create_group_success['data']['gpOid']
        gpid1 = self.db_purchase.get_xshare_group_purchase(_id=gpoid1)['gpid']
        # 数据库查询团单
        join_qualification = self.group_purchase_invitee1.api_invitee_qualification(gpid=gpid1, gpoid=gpoid1)
        # 请求参团资格接口
        assert join_qualification["code"] == 0
        # 判断接口是否调用成功
        assert join_qualification['data']['inviteeQualified'] is False
        # 判断是否有参团资格

    def test_join_faild2(self):
        """
        用户不符合参团资格且不符合下单资格，不能参团成功
        """
        self.delete_db_inviter(mobile=self.purchase_inviter2)
        create_group_success = self.group_purchase_inviter2.api_invite_order(gpid=self.gp_id1)
        # 创建团单
        # print(create_group_success)
        gpoid1 = create_group_success['data']['gpOid']
        gpid1 = self.db_purchase.get_xshare_group_purchase(_id=gpoid1)['gpid']
        # 数据库查询团单
        join_qualification = self.group_purchase_invitee2.api_invitee_qualification(gpid=gpid1, gpoid=gpoid1)
        # 请求参团资格接口
        get_uid = self.db_user.get_users(mobile=self.purchase_inviter2)["_id"]
        # 查询团长uid
        # print(get_uid)
        create_order_faild2 = self.old_user_order2.api_create_v2(
            item_id='H5_Sample_Pintuan',
            nonce=now_timeStr(),
            source='NA',
            xshare_initiator=get_uid,
            sharer=get_uid,
            sp2xuIds=self.sp2xuId_list_value['K1GETC_99'],
            gpid=gpid1,
            gpoid=gpoid1
        )
        # 创建订单
        # print(create_order_faild1)
        assert join_qualification["code"] == 0
        # 判断接口是否调用成功
        assert join_qualification['data']['inviteeQualified'] == False
        # 判断是否有参团资格
        print(create_order_faild2)
        assert create_order_faild2['code'] == 44301
        # 判断接口是否调用成功
        assert create_order_faild2['msg'] == '您已购买过英语科目的体验课，请重新选择'

    def test_join_success(self):
        """
        用户符合参团资格且符合下单资格，能参团成功,size=2的团，直接成团
        """
        # 开团
        gpoid = self.kaituan(gpid=self.gp_id3, tz_mobile=self.purchase_inviter2)
        # 新用户参团
        mobile = self.create_user()
        print(mobile)
        inviter2_uid = self.purchase_user_inviter2.user_id
        total_before = ApiDiamond(auth_token=self.purchase_auth_inviter2).api_get_Diamond_user()['data']['total']
        print("新用户参团前团长💎总数：", total_before)
        self.cantuan(self.gp_id3, gpoid, mobile, inviter2_uid)
        time.sleep(5)
        total_after = ApiDiamond(auth_token=self.purchase_auth_inviter2).api_get_Diamond_user()['data']['total']
        tuan_order = self.db_purchase.get_xshare_group_purchase(_id=gpoid)
        # print(tuan_order)
        print("新用户参团后团长💎总数：", total_after)
        assert tuan_order['invitee'][0]['mobile'] == mobile
        assert total_after - total_before > 500

    def test_commodity(self):
        """
        用户登陆后能获取商品详情
        """
        get_commodity = self.old_user_commodity.get_stock_v2(spuId='99_WXStore')
        print(get_commodity)
        assert get_commodity["code"] == 0
        # 判断接口是否调用成功
        # assert get_commodity["data"]['defaultIndex']['sp2xuId'] == 2143
        assert get_commodity["data"]['defaultIndex']['sp2xuId'] is not None
        # 判断是否能获得商品信息
        assert get_commodity["data"]['spuSubjectTypes'][0] == 'ENG'

    def create_order(self, gpid, gpoid, auth, tz_uid):
        """
        创建团员参团订单
        @param gpid: 活动id
        @param gpoid: 团单号
        @param auth: 参团用户auth
        @param tz_uid: 团长uid
        @return:create接口的response
        """
        create_order_success = ApiOrder(basic_auth=auth).api_create_v2(
            item_id='H5_Sample_Pintuan',
            nonce=now_timeStr(),
            source='NA',
            xshare_initiator=tz_uid,
            sharer=tz_uid,
            sp2xuIds=self.sp2xuId_list_value['H5_XX_Sample'],
            gpid=gpid,
            gpoid=gpoid
        )
        # 创建订单
        # print(create_order_success['data']['orderNo'])
        return create_order_success

    def kaituan(self, gpid, tz_mobile):
        """
        团长开团：创建团单
        @param gpid: 活动ID
        @param tz_mobile: 团长手机号
        @return: 团单号gpoid
        """
        # 先删除团长已有团单数据
        self.delete_db_inviter(tz_mobile)
        time.sleep(4)
        tz_auth = UserProperty(mobile=tz_mobile).basic_auth  # 团长的auth
        # 开团
        res = ApiGroupPurchase(token=tz_auth).api_invite_order(gpid=gpid)
        print(res)
        gpoid = self.db_purchase.get_xshare_group_purchase(inviterId=UserProperty(mobile=tz_mobile).user_id)["_id"]
        return gpoid

    def cantuan(self, gpid, gpoid, mobile, tz_uid):
        """
        团员参团正向流程：
        1.资格校验
        2.创建订单
        3.支付订单
        @param gpoid: 团单号
        @param mobile: 参团用户手机号
        @param tz_uid: 团长uid
        @return: 参团用户手机号、生成的用户订单oid
        """
        user_auth = UserProperty(mobile=mobile).basic_auth
        # 参团资格校验
        join_qualification = ApiGroupPurchase(token=user_auth).api_invitee_qualification(gpid=gpid, gpoid=gpoid)
        # print(join_qualification)
        assert join_qualification['data']['inviteeQualified'] is True
        res = self.create_order(gpid, gpoid, user_auth, tz_uid)
        oid = res['data']['orderNo']
        # 支付订单
        re = ApiOrder(basic_auth=user_auth).api_charge_v2(oid=oid, channel='wx_wap',
                                                          result_url="https://devt.jiliguala.com/test")
        check.equal(re['status_code'], 200)
        return mobile, oid

    def test_real_reward_address(self):
        """
        奖励为实物的团，能成功填地址
        inviter1不是正价课用户，不是推广人，算是新用户，可以开实物团jlglpintuan202104_Omo1
        """
        # 用inviter1开一个实物团gpid2
        gpoid = self.kaituan(gpid=self.gp_id2, tz_mobile=self.purchase_inviter1)
        # 新用户参团
        mobile = self.create_user()
        print(mobile)
        user_auth = UserProperty(mobile).basic_auth
        inviter1_uid = self.purchase_user_inviter1.user_id
        mobile1, oid = self.cantuan(self.gp_id2, gpoid, mobile, inviter1_uid)
        # 填地址
        time.sleep(5)
        address = ApiPostAddress(auth_token=user_auth)
        resp = address.post_address(oid=oid)
        # 对填地址的断言
        time.sleep(1)
        check.equal(resp['status_code'], 200)
        db_res = self.db_pingxxorder.get_pingxxorder(_id=oid)
        address = db_res['receiver']
        print(address)
        check.equal(address['name'], '接口自动化测试')
        check.equal(address['tel'], '11111111111')
        check.equal(address['region'], '北京市 北京市 东城区')
        check.equal(address['addr'], '测试-接口自动化测试case地址')

    def test_tuanzhang_bottom_reward(self):
        """
        团员参团成功后，转介绍底层奖励发放正确
        inviter2开一个三人团，一个新用户参团，团长得到的奖励=500（没成团奖励）
        """
        # 开团
        gpoid = self.kaituan(gpid=self.gp_id1, tz_mobile=self.purchase_inviter2)
        # 新用户参团
        mobile = self.create_user()
        print(mobile)
        inviter2_uid = self.purchase_user_inviter2.user_id
        # 参团前查一下钻石数
        total_before = ApiDiamond(auth_token=self.purchase_auth_inviter2).api_get_Diamond_user()['data']['total']
        print("新用户参团前团长💎总数：", total_before)
        self.cantuan(self.gp_id1, gpoid, mobile, inviter2_uid)
        time.sleep(5)
        # 参团后查一下钻石数
        total_after = ApiDiamond(auth_token=self.purchase_auth_inviter2).api_get_Diamond_user()['data']['total']
        print("新用户参团后团长💎总数：", total_after)
        assert total_after - total_before >= 500  # 如果团size=2，奖励就包括成团奖励了，就是1500+500；如果size>2，一个人参团就只发500

    def test_cantuan_once(self):
        """
        同一团单下&同一用户只能参一次团
        inviter2开一个团，一个用户参团后再次参团
        """
        # 开团
        gpoid = self.kaituan(gpid=self.gp_id1, tz_mobile=self.purchase_inviter2)
        # 新用户参团
        mobile = self.create_user()
        print(mobile)
        inviter2_uid = self.purchase_user_inviter2.user_id
        self.cantuan(self.gp_id1, gpoid, mobile, inviter2_uid)
        time.sleep(3)
        # 该用户再创建订单
        create_order_again = self.create_order(self.gp_id1, gpoid, UserProperty(mobile).basic_auth, inviter2_uid)
        # print(create_order_again)
        assert create_order_again['code'] == 44301
        assert '您已购买过' in create_order_again['msg'] and '请重新选择' in create_order_again['msg']


    def test_pintuan_concurrent(self):
        """
        两个用户同时参团，size=2的团，会自动再开一团
        """
        # 开团
        gpoid = self.kaituan(gpid=self.gp_id3, tz_mobile=self.purchase_inviter2)
        # 新用户参团
        mobile1 = self.create_user()
        mobile2 = self.create_user()
        print(mobile1)
        print(mobile2)
        mobile_list = []
        mobile_list.append(mobile1)
        mobile_list.append(mobile2)
        inviter2_uid = self.purchase_user_inviter2.user_id
        print('starting at:', now_timeStr())
        threads = []
        for mobile in mobile_list:
            t = threading.Thread(target=self.cantuan, args=(self.gp_id3, gpoid,mobile,inviter2_uid))
            threads.append(t)
        for i in range(2):
            threads[i].start()
        for i in range(2):
            # wait for all
            # join()会等到线程结束，或者在给了 timeout 参数的时候，等到超时为止。
            # 使用 join()看上去 会比使用一个等待锁释放的无限循环清楚一些(这种锁也被称为"spinlock")
            threads[i].join()
        print('all DONE at:', now_timeStr())

        tuan_order = self.db_purchase.get_xshare_group_purchase(_id=gpoid)
        print(tuan_order)

    def logout_user(self, mobile):
        """
        注销用户
        :param mobile: 注销手机号
        :return:
        """
        new_user_token = UserProperty(mobile=mobile).basic_auth
        logout_user = ApiUserInfo(token=new_user_token)
        logout_user.api_sms_logout()
        smsCode = usersQuery().get_users(mobile=mobile)["sms"]["code"]
        logout_user.api_users_security_info(mobile=mobile, smsCode=smsCode)

    def buy_normal_lesson(self, token, channel, sp2xu_id, pay_price, pay_total, useGuadou=False):
        """购买正价课"""
        normal_order = ApiNewOrders(token)
        create_order = normal_order.api_order_create(sp2xuId=sp2xu_id, payPrice=pay_price, useGuadou=useGuadou)
        print(create_order)
        purchase_res = normal_order.api_charge_create(
            oid=create_order["data"]["orderNo"], channel=channel, payTotal=pay_total
        )
        return purchase_res

    # def test_selfPurchase(self):
    #     """
    #     团长自购：团长每次先注销，再注册成新用户,买正价课，再开团
    #     """
    #     ApiUserInfo().api_get_websms(mobile=self.new_user_mobile)
    #     self.logout_user(self.new_user_mobile)
    #     ApiUserInfo().api_get_websms(mobile=self.new_user_mobile)
    #     new_inviter = UserProperty(self.new_user_mobile)
    #     new_inviter_uid = new_inviter.user_id
    #     token = new_inviter.basic_auth
    #     pur_math_res = self.buy_normal_lesson(
    #         token=token,
    #         channel="wx_pub",
    #         sp2xu_id=self.sp2xuId_Normal,
    #         pay_price=self.sp2xuId_pay_price,
    #         pay_total=self.sp2xuId_pay_price,
    #     )
    #     time.sleep(3)
    #     # 开团
    #     gpoid = self.kaituan(gpid=self.gp_id3, tz_mobile=self.new_user_mobile)
    #     # 自己参团
    #     self.cantuan(self.gp_id3, gpoid, self.new_user_mobile, new_inviter_uid)
    #     time.sleep(3)

