# -*- coding: utf-8 -*-
# @Time    : 2020/10/12 4:26 下午
# @Author  : zoey
# @File    : test_eshop_order.py
# @Software: PyCharm

from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiPromotionActivity import ApiPromotionActivity
from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from business.Trade.eshopAdmin.ApiGroup import ApiGroup
from business.Trade.eshopAdmin.ApiRedeem import ApiRedeem
from business.Trade.eshopClient.ApiRedeem import ApiRedeem as c_ApiRedeem
from business.Trade.eshopClient.V2.ApiV2Commodity import ApiV2Commodity as c_ApiV2Commodity
from business.Trade.eshopClient.ApiGroup import ApiGroup as c_ApiGroup
from business.Trade.eshopClient.V2.ApiNewPurchase import ApiNewPurchase
from business.Trade.eshopClient.ApiGhs import ApiGhs
from business.Trade.eshopClient.ApiOrder import ApiOrder
from business.Trade.tradeOrder.ApiOrderApi import ApiOrderApi
from testcase.Trade.common import CommodityCommon, OrderCommon
from business.common.UserProperty import UserProperty
from utils.format.format import time
from business.mysqlQuery import EshopQuery
from business.businessQuery import xshareQuery, ghsQuery
import pytest


@pytest.mark.Trade
@pytest.mark.eshop
@pytest.mark.TradeCommodity
@pytest.mark.TradeOrder
@pytest.mark.TradeRedeem
# @pytest.mark.usefixtures('mock_toggle')
class TestEshopOrder:
    """Eshop H5流程相关用例"""
    order_no = None
    charge_id = None

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        # 获取管理后台用户token
        a_user = cls.config['eshop']['admin']['user']
        a_pwd = cls.config['eshop']['admin']['pwd']
        a_token = ApiAdminAuth().api_login(username=a_user, password=a_pwd).get('data').get('token')
        # 获取C端用户token
        c_user = cls.config['eshop']['user']
        basic_auth = UserProperty(mobile=c_user).basic_auth
        cls.uid = UserProperty(mobile=c_user).user_id
        cls.eshop_admin_promotion = ApiPromotionActivity(token=a_token)
        cls.eshop_admin_commodity = ApiCommodity(token=a_token)
        cls.eshop_admin_group = ApiGroup(token=a_token)
        cls.eshop_admin_redeem = ApiRedeem(token=a_token)
        cls.c_eshop_redeem = c_ApiRedeem(token=basic_auth)
        cls.c_eshop_commodity = c_ApiV2Commodity(token=basic_auth)
        cls.c_eshop_group = c_ApiGroup(token=basic_auth)
        cls.c_eshop_old_order = ApiOrder(token=basic_auth)
        cls.c_eshop_new_purchase = ApiNewPurchase(token=basic_auth)
        cls.c_eshop_ghs = ApiGhs(token=basic_auth)
        cls.orders = ApiOrderApi(token=basic_auth)
        cls.xshare_query, cls.ghs_query, cls.eshop_query = xshareQuery(), ghsQuery(), EshopQuery()
        cls.commodity_common = CommodityCommon(a_token=a_token)
        cls.order_common = OrderCommon(c_user=c_user)

    def teardown(self):
        self.order_common.order_refund_and_remove(self.charge_id, self.order_no)
        self.order_no = None
        self.charge_id = None

    def test_entity_shop_home_banner(self):
        """
        实体商城：查看首页banner图片
        :return:
        """
        tag_name = 'STSC'
        banner = self.c_eshop_commodity.api_get_v2_commodity_banner(tagName=tag_name)
        assert banner['code'] == 0
        assert banner['data']['tagName'] == tag_name
        assert isinstance(banner['data']['bannerList'], list)

    def test_entity_shop_home_commodity(self):
        """
        实体商城：查看首页商品列表
        :return:
        """
        tag_name = 'STSC'
        comm_list = self.c_eshop_commodity.api_get_v2_commodity_list_by_tag(tagName=tag_name)
        assert comm_list['code'] == 0
        assert isinstance(comm_list['data']['spuList'], list)

    @pytest.mark.parametrize('state', [2, 1])
    def test_commodity_detail_enable(self, get_commodity, state):
        """
        Eshop：SPU状态为已启用或者已下架，可以正确查看商品详情
        :param state: 商品状态 1已启用 2已下架
        :return:
        """
        spu_id, spu_no = get_commodity['spu']['id'], get_commodity['spu']['no']
        # 获取SPU的请求body
        spu_detail = self.eshop_admin_commodity.api_get_spu_detail(spuId=spu_id)['data']
        # 更新body中的状态字段并修改SPU
        spu_detail['state'] = state
        self.eshop_admin_commodity.api_create_edit_spu(spu_detail)
        # C端获取SPU详情
        detail = self.c_eshop_commodity.api_get_v2_commodity_detail(spuNo=spu_no)
        assert detail['code'] == 0
        assert detail['data']['state'] == state

    @pytest.mark.parametrize('state', [0, 3])
    def test_commodity_detail_disable(self, get_commodity, state):
        """
        Eshop：SPU状态为编辑中或者已禁用，无法查看商品详情
        :param state: 商品状态 0编辑中 3已禁用
        :return:
        """
        spu_id, spu_no = get_commodity['spu']['id'], get_commodity['spu']['no']
        # 获取SPU的请求body
        spu_detail = self.eshop_admin_commodity.api_get_spu_detail(spuId=spu_id)['data']
        # 更新body中的状态字段并修改SPU
        spu_detail['state'] = state
        self.eshop_admin_commodity.api_create_edit_spu(spu_detail)
        # C端获取SPU详情
        detail = self.c_eshop_commodity.api_get_v2_commodity_detail(spuNo=spu_no)
        # 将SPU状态还原为已启用
        spu_detail['state'] = 1
        self.eshop_admin_commodity.api_create_edit_spu(spu_detail)
        assert detail['code'] == 12001
        assert detail['msg'] == '商品不存在'

    @pytest.mark.parametrize('pro_type', [True, False])
    def test_promotion_detail_enable(self,  get_commodity, pro_type):
        """
        Eshop：拼团活动已启用，可以正确查看活动信息
        :param pro_type: 真拼团：true 假拼团：false
        :return:
        """
        pro_id, spu_no = get_commodity['promotion']['fake_id'], get_commodity['spu']['no']
        if pro_type:
            pro_id = get_commodity['promotion']['real_id']
        # 更新活动启用状态
        self.eshop_admin_promotion.api_edit_promotion_activity_detail(promotionId=pro_id, enable=True)
        # C端获取商品活动详情
        detail = self.c_eshop_commodity.api_get_v2_commodity_detail(spuNo=spu_no, promotionId=pro_id)
        assert detail['code'] == 0
        assert detail['data']['promotion']['id'] == pro_id

    @pytest.mark.parametrize('pro_type', [True, False])
    def test_promotion_detail_disable(self, get_commodity, pro_type):
        """
        Eshop：拼团活动已禁用，无法查看活动信息
        :param pro_type: 真拼团：true 假拼团：false
        :return:
        """
        pro_id, spu_no = get_commodity['promotion']['fake_id'], get_commodity['spu']['no']
        if pro_type:
            pro_id = get_commodity['promotion']['real_id']
        # 更新活动启用状态
        self.eshop_admin_promotion.api_edit_promotion_activity_detail(promotionId=pro_id, enable=False)
        # C端获取商品活动详情
        detail = self.c_eshop_commodity.api_get_v2_commodity_detail(spuNo=spu_no, promotionId=pro_id)
        # 将活动状态还原为已启用
        self.eshop_admin_promotion.api_edit_promotion_activity_detail(promotionId=pro_id, enable=True)
        assert detail['code'] == 0
        assert 'promotion' not in detail['data']

    @pytest.mark.parametrize('pro_type', [True, False])
    def test_promotion_groups(self, get_commodity, pro_type):
        """
        Eshop：拼团活动，正确返回10个正在进行中的团
        :param pro_type: 真拼团：true 假拼团：false
        :return:
        """
        pro_id, spu_no = get_commodity['promotion']['fake_id'], get_commodity['spu']['no']
        if pro_type:
            pro_id = get_commodity['promotion']['real_id']
        # 获取活动下正在进行的团
        groups = self.c_eshop_commodity.api_get_v2_commodity_groups_detail(spuNo=spu_no, promotionId=pro_id)
        assert isinstance(groups['data']['groups'], list)
        assert len(groups['data']['groups']) == 10
        assert isinstance(groups['data']['buyingCount'], int)

    @pytest.mark.parametrize('channel, number, guadou_num', [('wx_pub', 1, 0), ('wx_wap', 2, 100)])
    def test_purchase_non_pro(self, get_commodity, channel, number, guadou_num):
        """
        Eshop：测试非活动购买：微信支付
        :param channel: 支付方式
        :param number: 购买数量
        :param guadou_num: 呱豆数量
        :return:
        """
        # 创建订单并支付
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_phy']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no, channel=channel, num=number,
                                            guadou_num=guadou_num)
        self.order_no, self.charge_id = detail[0], detail[1]
        # 查看订单状态
        time.sleep(10)
        status = self.c_eshop_old_order.api_get_order_status(oid=self.order_no)
        assert status['code'] == 0
        assert status['data']['status'] == 'paid'

    @pytest.mark.parametrize('channel, number, guadou_num', [('alipay_wap', 1, 100), ('alipay_qr', 2, 0)])
    def test_purchase_fake_pro(self, get_commodity, channel, number, guadou_num):
        """
        Eshop：测试假拼团活动购买：支付宝支付
        :param channel: 支付方式
        :param number: 购买数量
        :param guadou_num: 呱豆数量
        :return:
        """
        # 创建订单并支付
        pro_id, spu_no = get_commodity['promotion']['fake_id'], get_commodity['spu']['no']
        sgu_no = get_commodity['sgu_phy']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no, pro_id=pro_id, channel=channel, num=number,
                                            guadou_num=guadou_num)
        self.order_no, self.charge_id = detail[0], detail[1]
        # 查看订单状态
        time.sleep(10)
        status = self.c_eshop_old_order.api_get_order_status(oid=self.order_no)
        assert status['code'] == 0
        assert status['data']['status'] == 'paid'

    @pytest.mark.parametrize('channel, number, guadou_num', [('alipay_wap', 1, 0), ('alipay_qr', 2, 100)])
    def test_purchase_real_pro_launch(self, get_commodity, channel, number, guadou_num):
        """
        Eshop：测试真拼团活动开团购买：花呗分期支付
        :param channel: 支付方式
        :param number: 购买数量
        :param guadou_num: 呱豆数量
        :return:
        """
        # 创建订单的并支付
        pro_id, spu_no = get_commodity['promotion']['real_id'], get_commodity['spu']['no']
        sgu_no = get_commodity['sgu_phy']['ge']['no']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no, pro_id=pro_id, channel=channel, hbfq_num=3,
                                            num=number, guadou_num=guadou_num)
        self.order_no, self.charge_id = detail[0], detail[1]
        # 查看订单状态
        time.sleep(10)
        status = self.c_eshop_old_order.api_get_order_status(oid=self.order_no)
        assert status['code'] == 0
        assert status['data']['status'] == 'paid'
        # 获取新开的团的id
        group = self.c_eshop_group.api_get_my_groups(promotionId=pro_id, itemId=sgu_no)
        assert group['code'] == 0
        assert group['data'][0].get('id', 0) != 0
        assert group['data'][0]['status'] == 'notcompleted'
        # 查看团详情
        group_id = group['data'][0]['id']
        group_detail = self.c_eshop_group.api_get_group_detail(groupId=group_id)
        # 删除团
        self.xshare_query.delete_xshare_group_purchase(_id=group_id)
        assert group_detail['code'] == 0
        assert group_detail['data']['id'] == group_id
        assert group_detail['data']['isSelf']
        assert not group_detail['data']['allowJoin']

    def test_purchase_real_pro_join(self, get_commodity):
        """
        Eshop：测试真拼团活动参团购买：呱豆全额抵扣支付
        :return:
        """
        # 获取一个团ID
        pro_id, spu_no = get_commodity['promotion']['real_id'], get_commodity['spu']['no']
        sgu_no = get_commodity['sgu_phy']['ge']['no']
        group_id = self.c_eshop_commodity.api_get_v2_commodity_groups_detail(spu_no, pro_id)['data']['groups'][0]['id']
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no, pro_id=pro_id, group_id=group_id)
        self.order_no = detail[0]
        assert detail[1] == 'free'
        # 查看团详情
        time.sleep(10)
        group_detail = self.c_eshop_group.api_get_group_detail_v2(groupId=group_id)
        # 删除团
        self.xshare_query.delete_xshare_group_purchase(_id=group_id)
        assert group_detail['code'] == 0
        assert group_detail['data']['id'] == group_id
        assert group_detail['data']['isSelf']
        assert not group_detail['data']['allowJoin']

    @pytest.mark.parametrize('subject, planner', [('GE', 'wh_planner'), ('MA', 'sh_planner')])
    def test_ghs_assignment_and_limitation(self, get_commodity, subject, planner):
        """
        Eshop：测试规划师分配、购买限制
        :param subject: 科目 英语：GE  思维：MA
        :param planner: 规划师参数类型  wh_planner：武汉规划师  sh_planner：上海规划师
        :return:
        """
        # 获取SGU信息
        spu_no, sgu_no = get_commodity['spu']['no'], get_commodity['sgu_system']['ge']['no']
        if subject == 'MA':
            sgu_no = get_commodity['sgu_system']['ma']['no']
        sp2xuid = self.order_common.get_sp2xuid_and_price(spu_no=spu_no, sgu_no=sgu_no)[0]
        # 删除用户规划师
        self.ghs_query.delete_ghs_user(_id=self.uid)
        self.ghs_query.delete_math_ghs_user(uid=self.uid)
        # 验证用户未绑定规划师，无法通过规划师链接购买对应科目
        res = self.c_eshop_new_purchase.api_new_purchase_validation(sp2xuId=sp2xuid, source=planner)
        assert res['code'] == 11104
        assert f'您当前登录的手机号不可购买' in res['msg']
        # 购买正价课
        detail = self.order_common.purchase(spu_no=spu_no, sgu_no=sgu_no)
        self.order_no = detail[0]
        time.sleep(10)
        # 验证用户首购正价课，应分配对应科目规划师
        res = self.c_eshop_ghs.api_get_ghs(orderId=self.order_no)
        assert res['code'] == 0
        assert res['data']['eshopFirst']
        assert res['data']['url']
        # 验证用户已分配规划师，可以通过规划师链接购买对应商品
        res = self.c_eshop_new_purchase.api_new_purchase_validation(sp2xuId=sp2xuid, source=planner)
        assert res['code'] == 0














