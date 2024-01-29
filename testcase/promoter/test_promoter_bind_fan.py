#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> test_promoter_bind_fan.py
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/6/4 5:06 下午
@Desc   ：
=================================================="""
import time

import pytest

from business.mars.ApiOrder import ApiOrder
from business.promoter.ApiPromoter import ApiPromoter
from business.zero.mock.ApiMock import ApiMock
from config.env.domains import Domains
from business.zero.dataTool.ApiPromoterData import ApiPromoterData
from utils.enums.businessEnums import PromoterOperationEnum
from utils.format.format import now_timeStr
from business.common.UserProperty import UserProperty
from business.businessQuery import promoterQuery,wcuserQuery


@pytest.mark.promoter
@pytest.mark.promoterBindFans
class TestPromoterBindFan:
    """推广人锁粉相关用例"""
    oid = []
    mock_charge_id = []
    promoterQuery = promoterQuery()
    wcuserQuery=wcuserQuery()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        # 用来锁粉的新用户
        cls.fan = UserProperty(cls.config['promoter']['fan4'])
        cls.promoter = UserProperty(cls.config['promoter']['promoter7'])
        # 用于锁粉的推广人实例
        # 设置wc_users 为当前当前用户uid
        cls.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=cls.promoter.user_id)
        cls.promoter_bind_fan = ApiPromoter(wechat_token=cls.promoter.encryptWechatToken_promoter,
                                            basic_auth=cls.promoter.basic_auth)
        cls.promoter_dataTool = ApiPromoterData()
        cls.update_promoter_account(cls)

        cls.mock = ApiMock()
        cls.mock.api_update_mock_status(status=True, env=cls.config['env'], server_list=["交易中台"],
                                          user_email="jack_wu@jiliguala.com")
        time.sleep(150)

    # @classmethod
    # def teardown_class(cls):
    #     cls.mock.api_update_mock_status(status=False, env=cls.config['env'], server_list=["交易中台"],
    #                                       user_email="jack_wu@jiliguala.com")

    def update_promoter_account(self):
        """
        查询推广人账号是否unionid 和openid，没有的插入一下
        查询推广人promoter_wechat 是否有记录，没有的话插入一下，
        这2个条件不满足查询粉丝数量的时候，查询不到数据
        """

        # promoter_account 是否有unionId和openid
        res = self.promoterQuery.get_promoter_accounts(uid=self.promoter.user_id)
        unionId = self.promoter.wc_users_unionId
        openId = self.promoter.wc_openusers_by_promoter_openId
        promoterId = res['_id']
        uid = self.promoter.user_id
        if res['openid'] == '' and res['unionId'] == '':
            self.promoterQuery.update_promoter_accounts(res['_id'],
                                                        openid=openId,
                                                        unionId=unionId)

        # promoter_wechat是否有记录没有插入一条
        res_wechat = self.promoterQuery.get_promoter_wechat(uid=uid,
                                                            _id=unionId)
        content = {
            "_id": unionId,
            "uid": uid,
            "promoterId": promoterId
        }
        if res_wechat is None:
            self.promoterQuery.insert_promoter_wechat(content)

    def teardown(self):
        # mock支付订单退款
        if self.mock_charge_id:
            for index in range(len(self.mock_charge_id)):
                res = self.mock.api_refund_mock(self.mock_charge_id[index])
                # 退款成功后，删除pingxxorder,promoter_order,xshare_relationship表恢复数据
                if res["succeed"]:
                    self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                                 operation=PromoterOperationEnum.get_chinese(
                                                                     "删除粉丝购买的课程记录"),
                                                                 orderId=self.oid[index])
                    self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                                 operation=PromoterOperationEnum.get_chinese("删除锁粉信息"),
                                                                 mobile=self.config['promoter']['fan4'])
            # 清空list
            self.mock_charge_id = []
            self.oid = []

    def buy_h5_sample_diamond_activity(self, sp2xuIds, sharer, fan):
        """买9.9"""
        # 生成9.9订单记录
        fan_order = ApiOrder(basic_auth=fan.basic_auth)
        order_res = fan_order.api_create_v2(item_id='H5_Sample_DiamondActivity', nonce=now_timeStr(),
                                            source="AppHomeView", xshare_initiator=sharer,
                                            sharer=sharer, sp2xuIds=sp2xuIds)
        # 支付订单
        charge_res = fan_order.api_charge_v2(oid=order_res['data']['orderNo'], channel='wx_wap',
                                             result_url="https://devt.jiliguala.com/test")
        return charge_res

    """-------------------------------------------------锁粉相关用例---------------------------------------------------"""

    def test_english_math_valid_fan(self):
        # 新用户购买9.9英语体验课有效锁粉
        english_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2819], sharer=self.promoter.user_id,
                                                                 fan=self.fan)
        # 把英语订单的mock_charge_id和oid加到list里
        self.mock_charge_id.append(english_charge_res['data']['id'])
        self.oid.append(english_charge_res['data']['order_no'])
        # 等待5秒，否则校验时可能锁粉关系还未写入导致失败
        time.sleep(5)
        # 查询推广人最新的一个英语粉丝
        englishfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=1, pageIndex=0, pageSize=1)
        # englishfan = self.promoter_bind_fan.api_promoter_invitees_fans(1)
        # 校验英语是否锁粉成功
        assert englishfan['data']['fansList'][0]['guaid'] == '1503309'
        # assert englishfan['data']['fansList'][0]['guaid'] == '1510867'
        # 新用户购买9.9思维体验课有效锁粉
        math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2821], sharer=self.promoter.user_id,fan=self.fan)
        # math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[1111], sharer=sharer)
        time.sleep(5)
        # 查询推广人最新的一个思维粉丝
        mathfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=3, pageIndex=0, pageSize=1)
        # 把思维订单的mock_charge_id和oid加到list里
        self.mock_charge_id.append(math_charge_res['data']['id'])
        self.oid.append(math_charge_res['data']['order_no'])
        # 校验思维是否锁粉成功
        assert mathfan['data']['fansList'][0]['guaid'] == '1503309'
        # assert mathfan['data']['fansList'][0]['guaid'] == '1510867'

    def test_math_english_valid_fan(self):
        math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2821], sharer=self.promoter.user_id,
                                                              fan=self.fan)
        # math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[1111], sharer=sharer)
        # 等待5秒拿不到粉丝数据
        time.sleep(5)
        mathfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=3, pageIndex=0, pageSize=1)
        self.mock_charge_id.append(math_charge_res['data']['id'])
        self.oid.append(math_charge_res['data']['order_no'])
        assert mathfan['data']['fansList'][0]['guaid'] == '1503309'
        # assert mathfan['data']['fansList'][0]['guaid'] == '1510867'
        english_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2819], sharer=self.promoter.user_id,
                                                                 fan=self.fan)
        # english_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[1112], sharer=sharer)
        self.mock_charge_id.append(english_charge_res['data']['id'])
        self.oid.append(english_charge_res['data']['order_no'])
        time.sleep(5)
        englishfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=1, pageIndex=0, pageSize=1)
        assert englishfan['data']['fansList'][0]['guaid'] == '1503309'
        # assert englishfan['data']['fansList'][0]['guaid'] == '1510867'

    @pytest.mark.parametrize("sp2xuIds", [[2820]])
    # @pytest.mark.parametrize("sp2xuIds,sharer", [[1110]])
    def test_english_and_math_valid_fan(self, sp2xuIds):
        # 新用户购买9.9英语+思维联报体验课有效锁粉
        english_and_math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=sp2xuIds,
                                                                          sharer=self.promoter.user_id, fan=self.fan)
        self.mock_charge_id.append(english_and_math_charge_res['data']['id'])
        self.oid.append(english_and_math_charge_res['data']['order_no'])
        time.sleep(5)
        englishfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=1, pageIndex=0, pageSize=1)
        mathfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=3, pageIndex=0, pageSize=1)
        assert englishfan['data']['fansList'][0]['guaid'] == '1503309'
        # assert englishfan['data']['fansList'][0]['guaid'] == '1510867'
        assert mathfan['data']['fansList'][0]['guaid'] == '1503309'
        # assert mathfan['data']['fansList'][0]['guaid'] == '1510867'

    @pytest.mark.parametrize("validsharer", ["7843698d4ea34917be41fb46274e8205"])
    def test_english_invalid_fan(self, validsharer):
        # 先通过其他推广人的邀请购买思维，有效锁粉
        # math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[1111],sharer=validsharer)
        math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2821], sharer=validsharer, fan=self.fan)
        self.mock_charge_id.append(math_charge_res['data']['id'])
        self.oid.append(math_charge_res['data']['order_no'])
        # 再通过推广人的邀请购买英语，无效锁粉
        # english_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[1112], sharer=self.promoter.user_id)
        english_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2819], sharer=self.promoter.user_id,
                                                                 fan=self.fan)
        self.mock_charge_id.append(english_charge_res['data']['id'])
        self.oid.append(english_charge_res['data']['order_no'])
        time.sleep(5)
        invalidenglishfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=1, pageIndex=0, pageSize=1,
                                                                              tags=[3])
        # assert invalidenglishfan['data']['fansList'][0]['guaid'] == '1510867'
        assert invalidenglishfan['data']['fansList'][0]['guaid'] == '1503309'

    @pytest.mark.parametrize("validsharer", ["7843698d4ea34917be41fb46274e8205"])
    def test_math_invalid_fan(self, validsharer):
        # 先通过其他推广人的邀请购买英语，有效锁粉
        # english_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[1112], sharer=validsharer)
        english_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2819], sharer=validsharer, fan=self.fan)
        self.mock_charge_id.append(english_charge_res['data']['id'])
        self.oid.append(english_charge_res['data']['order_no'])
        # 再通过推广人的邀请购买思维，无效锁粉
        # math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[1111], sharer=self.promoter.user_id)
        math_charge_res = self.buy_h5_sample_diamond_activity(sp2xuIds=[2821], sharer=self.promoter.user_id,
                                                              fan=self.fan)
        self.mock_charge_id.append(math_charge_res['data']['id'])
        self.oid.append(math_charge_res['data']['order_no'])
        time.sleep(5)
        invalidmathfan = self.promoter_bind_fan.api_promoter_invitees_fans(orderSubject=3, pageIndex=0, pageSize=1,
                                                                           tags=[3])
        # assert invalidmathfan['data']['fansList'][0]['guaid'] == '1510867'
        assert invalidmathfan['data']['fansList'][0]['guaid'] == '1503309'
