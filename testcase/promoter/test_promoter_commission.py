# coding=utf-8
# @Time    : 2021/3/30 5:25 下午
# @Author  : jerry
# @File    : test_promoter_commission.py
import time
import pytest

from config.env.domains import Domains
from business.promoter.ApiRefund import ApiRefund
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth
from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from business.zero.dataTool.ApiPromoterData import ApiPromoterData
from utils.enums.businessEnums import PromoterOperationEnum, EshopLevelEnum, \
    EshopItemPartnerEnum, EshopItemPromoterEnum
from business.common.UserProperty import UserProperty
from business.common.PromoterProperty import PromoterProperty
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.Trade.eshopClient.V2.ApiV2Commodity import ApiV2Commodity
from business.promoter.ApiPromoterLogin import ApiPromoterLogin
from business.promoter.ApiHome import ApiHome
from business.businessQuery import promoterQuery, pingxxorderQuery, wcuserQuery


@pytest.mark.promoter
@pytest.mark.promoterCommission
class TestPromoterCommission:
    """推广人分佣相关用例"""
    promoterQuery = promoterQuery()
    oid = []
    state = None

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.promoterUser = PromoterProperty(cls.config['promoter']['promoter1'])
        cls.user = UserProperty(cls.config['promoter']['promoter1'])
        cls.promoterUser8 = PromoterProperty(cls.config['promoter']['promoter8'])
        cls.user8 = UserProperty(cls.config['promoter']['promoter8'])
        cls.promoterUser9 = PromoterProperty(cls.config['promoter']['promoter9'])
        cls.user9 = UserProperty(cls.config['promoter']['promoter9'])
        # 推广人作为粉丝拓科的上级推广人
        cls.promoterUser5 = PromoterProperty(cls.config['promoter']['promoter5'])
        cls.user5 = UserProperty(cls.config['promoter']['promoter5'])
        cls.promoter = ApiPromoterLogin(wechat_token=cls.user.encryptWechatToken_promoter,
                                        basic_auth=cls.user.basic_auth)
        cls.fan6 = UserProperty(cls.config['promoter']['fan6'])
        # #推广人作为粉丝拓科
        cls.fan7 = UserProperty(cls.config['promoter']['fan7'])
        cls.promoterUser7 = PromoterProperty(cls.config['promoter']['fan7'])
        cls.fan8 = UserProperty(cls.config['promoter']['fan8'])
        cls.home = ApiHome(wechat_token=cls.user.encryptWechatToken_promoter, basic_auth=cls.user.basic_auth)
        cls.commodity = ApiV2Commodity(cls.fan6.basic_auth)
        cls.promoter_dataTool = ApiPromoterData()
        cls.pro_refund = ApiRefund()  # 创建一个用于退款的实例
        cls.pingxxorderQuery = pingxxorderQuery()
        cls.wcuserQuery = wcuserQuery()

    def teardown(self):
        if self.oid:
            for id in self.oid:
                res = self.pro_refund.api_refund(id)
                if res["code"] == 200:
                    self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                                 operation=PromoterOperationEnum.get_chinese(
                                                                     "删除粉丝购买的课程记录"),
                                                                 orderId=id)
            self.oid = []
        if self.state:
            self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                         operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
                                                         mobile=self.user.mobile, content={'state': 'active'})
            self.state = None

    def update_level(self, level, mobile):
        """修改推广人的级别"""
        self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                     operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
                                                     mobile=mobile, content={'level': level})

    # 粉丝和推广人创建订单方法
    def create_order(self, fan, promoter, channel=None, guadou_num=None, sp2xu_id=None, promoter_id=None,
                     pay_price=None,
                     pay_total=None):
        """下单，用于分佣前预置条件"""
        result = {}
        fan_order = ApiNewOrders(token=fan.basic_auth)
        eshop_res = fan_order.api_order_create(sp2xuId=sp2xu_id, payPrice=pay_price, guaDouNum=guadou_num,
                                               promoterId=promoter_id)
        charge_res = fan_order.api_charge_create(oid=eshop_res['data']['orderNo'], channel=channel,
                                                 payTotal=pay_total, guadouDiscount=guadou_num)
        result['charge_res'] = charge_res
        time.sleep(2)
        # 获取最新的推广人金额数据
        promoter_login = ApiPromoterLogin(wechat_token=promoter.encryptWechatToken_promoter,
                                          basic_auth=promoter.basic_auth)

        new_promoter_info = promoter_login.api_check_bind()
        home = ApiHome(wechat_token=promoter.encryptWechatToken_promoter, basic_auth=promoter.basic_auth)
        income_detail_first = home.api_income_detail()
        new_income_over = home.api_income_overview()
        # 还原数据，先退款，后删除所有新增表数据
        self.oid.append(eshop_res["data"]["orderNo"])
        result['new_promoter_info'] = new_promoter_info['data']['userInfo']
        result['income_detail_first'] = income_detail_first
        result['new_income_over'] = new_income_over
        return result

    @staticmethod
    def judge_case(result, old_info, commodity_no, level, price):
        """分佣共用断言"""
        # 判断冻结金额，累计金额，月收益是否按对应比例增加
        if level == "promoter":
            assert result['new_income_over']['data']['frozenRevenue'] == (
                    price * EshopItemPromoterEnum.get_chinese(commodity_no)) * EshopLevelEnum.get_chinese(level) + \
                   old_info['old_income_over']['data']['frozenRevenue']
            assert result['new_income_over']['data']['totalRevenue'] == (
                    price * EshopItemPromoterEnum.get_chinese(commodity_no)) * EshopLevelEnum.get_chinese(level) + \
                   old_info['old_income_over']['data']['totalRevenue']
            assert result['new_income_over']['data']['monthlyRevenue'] == (
                    price * EshopItemPromoterEnum.get_chinese(commodity_no)) * EshopLevelEnum.get_chinese(level) + \
                   old_info['old_income_over']['data']['monthlyRevenue']
        else:
            assert result['new_income_over']['data']['frozenRevenue'] == (
                    price * EshopItemPartnerEnum.get_chinese(commodity_no)) * EshopLevelEnum.get_chinese(level) + \
                   old_info['old_income_over']['data']['frozenRevenue']
            assert result['new_income_over']['data']['totalRevenue'] == (
                    price * EshopItemPartnerEnum.get_chinese(commodity_no)) * EshopLevelEnum.get_chinese(level) + \
                   old_info['old_income_over']['data']['totalRevenue']
            assert result['new_income_over']['data']['monthlyRevenue'] == (
                    price * EshopItemPartnerEnum.get_chinese(commodity_no)) * EshopLevelEnum.get_chinese(level) + \
                   old_info['old_income_over']['data']['monthlyRevenue']

    @pytest.fixture(scope='class')
    def get_old_info(self):
        """事先获取初始推广人相关信息"""
        old_info = {}
        old_promoter_info = self.promoter.api_check_bind()
        old_income_over = self.home.api_income_overview()
        old_info["old_promoter_info"] = old_promoter_info['data']['userInfo']
        old_info["old_income_over"] = old_income_over
        return old_info

    @pytest.fixture(scope='class')
    def get_commodity_detail(self):
        """获取商品详情"""
        commodity_detail = {}
        # C类课程商品详情
        c_course = self.commodity.api_get_v2_commodity_detail(spuNo="CRM_H5_BundleCDS002_SPU")
        # 纯课程商品详情
        pure_course = self.commodity.api_get_v2_commodity_detail(spuNo="K3GE_SPU")
        # 呱呱阅读商品详情
        read_course = self.commodity.api_get_v2_commodity_detail(spuNo="CRM_H5_ReadingVIPLifetime_0")
        # 不分佣课程
        no_commission_course = self.commodity.api_get_v2_commodity_detail(spuNo="CC_ST_K1_6_5")
        # 英语正价课
        english_course = self.commodity.api_get_v2_commodity_detail(spuNo="BST_DS_K1_6_01SPU")
        # 思维正价课
        mind_course = self.commodity.api_get_v2_commodity_detail(spuNo="SST_K1_6_01_SPU")

        commodity_detail['c_course'] = c_course
        commodity_detail['pure_course'] = pure_course
        commodity_detail['read_course'] = read_course
        commodity_detail['no_commission_course'] = no_commission_course
        commodity_detail['english_course'] = english_course
        commodity_detail['mind_course'] = mind_course
        return commodity_detail

    @pytest.fixture(scope="class")
    def get_mind_teach_tool_price_mind(self):
        """获取思维教具的价格"""
        a_token = ApiAdminAuth().api_login(username=self.config['sso']['email_address'],
                                           password=self.config['sso']['pwd']).get('data').get('token')
        eshop_admin_commodity = ApiCommodity(token=a_token)
        spu = eshop_admin_commodity.api_get_spu_list(commodityNo="SST_K1_6_01_SPU")
        sgu = eshop_admin_commodity.api_get_spu_detail(spuId=spu['data']['content'][0]['id'])
        price = eshop_admin_commodity.api_get_sxu_detail(sxuId=sgu['data']['skuSpecBriefList'][0]['id'])
        return price['data']['priceTeachingTool']

    @pytest.fixture(scope="class")
    def get_mind_teach_tool_price_english(self):
        """获取英语教具的价格"""
        a_token = ApiAdminAuth().api_login(username=self.config['sso']['email_address'],
                                           password=self.config['sso']['pwd']).get('data').get('token')
        eshop_admin_commodity = ApiCommodity(token=a_token)
        spu = eshop_admin_commodity.api_get_spu_list(commodityNo="BST_DS_K1_6_01SPU")
        sgu = eshop_admin_commodity.api_get_spu_detail(spuId=spu['data']['content'][0]['id'])
        price = eshop_admin_commodity.api_get_sxu_detail(sxuId=sgu['data']['skuSpecBriefList'][0]['id'])
        return price['data']['priceTeachingTool']

    """-----------------------------------------------------分佣比例相关的case---------------------------------------------"""

    @pytest.mark.parametrize('promoter_level,fan_level,type', [("promoter", "promoter", "mind"),
                                                               ("partner", "promoter", "mind"),
                                                               ("promoter", "partner", "mind"),
                                                               ("partner", "partner", "mind")])
    def test_promoter_commission_read_mind(self, get_old_info, get_commodity_detail, promoter_level, fan_level, type,
                                           get_mind_teach_tool_price_mind):
        '''
        15480000001 推广人作为粉丝拓科购买思维课程
        JLGL_TEST_MISSION 15502180495 作为上级推广人分佣
        佣金=（粉丝拓科订单实际支付金额-教具金额*65%）* 推广人等级（推广人20%，合伙人30%）
        粉丝拓科订单实际支付金额=商品售价-（商品售价-教具金额*65% ）*粉丝等级（推广人20%，合伙人30%）
        '''
        """推广人扩科后，上级推广人分佣；"""
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user5.user_id)
        course = get_commodity_detail['mind_course']
        # 预置推广人等级
        if promoter_level == "promoter":
            self.promoterQuery.update_promoter_accounts(self.promoterUser5.promoter_accounts_id, level="promoter",
                                                        totalAmount=0)
            promoter_rate = 0.2
        if fan_level == "promoter":
            self.promoterQuery.update_promoter_accounts(self.promoterUser7.promoter_accounts_id, level="promoter",
                                                        totalAmount=0)
            fan_rate = 0.2
        # 预置推广人和粉丝等级
        if promoter_level == "partner":
            self.promoterQuery.update_promoter_accounts(self.promoterUser5.promoter_accounts_id, level="partner",
                                                        totalAmount=2000000)
            promoter_rate = 0.3
        if fan_level == "partner":
            self.promoterQuery.update_promoter_accounts(self.promoterUser7.promoter_accounts_id, level="partner",
                                                        totalAmount=2000000)
            fan_rate = 0.3
        # 粉丝购买课程
        if type == "mind":
            sp2xuId = course['data']['skuSpecBriefList'][0]['sp2xuId']
            guadou_num = int(course['data']['skuSpecBriefList'][0]['priceRmb'])
        result = self.create_order(self.fan7, self.user5, channel="wx_pub",
                                   promoter_id=self.promoterUser5.promoter_accounts_id,
                                   pay_price=0,
                                   sp2xu_id=sp2xuId, pay_total=0,
                                   guadou_num=guadou_num)
        db_promoter_record = self.promoterQuery.get_promoter_order(_id=result['charge_res']['data']['order_no'])
        product_price = course['data']['priceRmb']
        teaching_tool_price = get_mind_teach_tool_price_mind

        # 粉丝拓科时间支付金额
        fan_acturely_paid_amount = product_price - (product_price - teaching_tool_price * 0.65) * fan_rate

        # 粉丝拓科时间支付金额
        promoter_commission = str((fan_acturely_paid_amount - teaching_tool_price * 0.65) * promoter_rate)
        position = promoter_commission.find('.')
        expect_commission = promoter_commission[0:position]

        for x in db_promoter_record:
            assert x['revenue'] == int(expect_commission)

    @pytest.mark.parametrize('level,type', [("promoter", "mind"), ("partner", "english")])
    def test_promoter_commission_extention_english_mind(self, get_commodity_detail, level, type,
                                                        get_mind_teach_tool_price_mind,
                                                        get_mind_teach_tool_price_english):
        """
        推广人拓课英语和思维，拓科的订单算业绩
        返现金额：返现金额= 商品售价-教具金额*65%）*20%-商品折扣金额
        测试推广人账号 15460000021推广人已经购买了英语正价课,推广人扩课思维
        扩课英语，推广人先退款思维，再购买思维课程
        """
        english_course = get_commodity_detail['english_course']
        mind_course = get_commodity_detail['mind_course']
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user8.user_id)
        # 预置推广人等级
        if level == 'promoter':
            self.promoterQuery.update_promoter_accounts(self.promoterUser8.promoter_accounts_id, level="promoter",
                                                        totalAmount=0)
        if level == 'partner':
            self.promoterQuery.update_promoter_accounts(self.promoterUser8.promoter_accounts_id, level="partner",
                                                        totalAmount=2000000)

        sp2xuId_mind = mind_course['data']['skuSpecBriefList'][0]['sp2xuId']
        guadou_num_mind = int(mind_course['data']['skuSpecBriefList'][0]['priceRmb'])

        sp2xuId_english = english_course['data']['skuSpecBriefList'][0]['sp2xuId']
        guadou_num_english = int(english_course['data']['skuSpecBriefList'][0]['priceRmb'])

        # 推广人购拓科思维课程
        # 先下单思维正价课再下单英语正价课
        if type == "mind":
            result_english = self.create_order(self.user8, self.user8, channel="wx_pub",
                                               pay_price=0,
                                               sp2xu_id=sp2xuId_english, pay_total=0,
                                               guadou_num=guadou_num_english)
            result_mind = self.create_order(self.user8, self.user8, channel="wx_pub",
                                            pay_price=0,
                                            sp2xu_id=sp2xuId_mind, pay_total=0,
                                            guadou_num=guadou_num_mind)
            mind_order_id = result_mind['charge_res']['data']['order_no']
            english_order_id = result_english['charge_res']['data']['order_no']
            order_change = self.pingxxorderQuery.get_pingxxorder(_id=mind_order_id)
            teaching_tool_price = get_mind_teach_tool_price_mind
        # 先下单思维正价课再下单英语正价课
        if type == "english":
            result_mind = self.create_order(self.user8, self.user8, channel="wx_pub",
                                            pay_price=0,
                                            sp2xu_id=sp2xuId_mind, pay_total=0,
                                            guadou_num=guadou_num_mind)
            result_english = self.create_order(self.user8, self.user8, channel="wx_pub",
                                               pay_price=0,
                                               sp2xu_id=sp2xuId_english, pay_total=0,
                                               guadou_num=guadou_num_english)
            mind_order_id = result_mind['charge_res']['data']['order_no']
            english_order_id = result_english['charge_res']['data']['order_no']
            order_change = self.pingxxorderQuery.get_pingxxorder(_id=english_order_id)
            teaching_tool_price = get_mind_teach_tool_price_english

        order_change_guadou = order_change['guadouAmount']
        total_change = order_change['total']
        discount_charge = total_change - order_change_guadou

        # 计算期望返现金额
        if level == "promoter":
            expect_commission = str((total_change - teaching_tool_price * 0.65) * 0.2 - discount_charge)
        if level == "partner":
            expect_commission = str((total_change - teaching_tool_price * 0.65) * 0.3 - discount_charge)

        postion = expect_commission.find('.')
        expect_commission = expect_commission[0:postion]

        if type == "mind":
            db_promoter_record = self.promoterQuery.get_promoter_own_order(_id=mind_order_id)
        if type == "english":
            db_promoter_record = self.promoterQuery.get_promoter_own_order(_id=english_order_id)

        for x in db_promoter_record:
            assert x['revenue'] == int(expect_commission)

    @pytest.mark.parametrize('level,type', [("promoter", "mind")])
    def test_promoter_commission_promoter_extention_promoter_to_partner(self, get_commodity_detail, level, type,
                                                                        get_mind_teach_tool_price_mind,
                                                                        get_mind_teach_tool_price_english):
        """
        推广人拓课思维升级到合伙人，拓科的订单算业绩
        返现金额：返现金额= 商品售价-教具金额*65%）*30%-商品折扣金额
        测试推广人账号 15460000021推广人已经购买了英语正价课,推广人扩课思维
        """
        english_course = get_commodity_detail['english_course']
        mind_course = get_commodity_detail['mind_course']
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user8.user_id)
        # 预置推广人等级
        if level == 'promoter':
            self.promoterQuery.update_promoter_accounts(self.promoterUser8.promoter_accounts_id, level="promoter",
                                                        totalAmount=900000)

        sp2xuId_mind = mind_course['data']['skuSpecBriefList'][0]['sp2xuId']
        guadou_num_mind = int(mind_course['data']['skuSpecBriefList'][0]['priceRmb'])

        sp2xuId_english = english_course['data']['skuSpecBriefList'][0]['sp2xuId']
        guadou_num_english = int(english_course['data']['skuSpecBriefList'][0]['priceRmb'])

        # 推广人购拓科思维课程
        # 先下单思维正价课再下单英语正价课
        if type == "mind":
            result_english = self.create_order(self.user8, self.user8, channel="wx_pub",
                                               pay_price=0,
                                               sp2xu_id=sp2xuId_english, pay_total=0,
                                               guadou_num=guadou_num_english)
            result_mind = self.create_order(self.user8, self.user8, channel="wx_pub",
                                            pay_price=0,
                                            sp2xu_id=sp2xuId_mind, pay_total=0,
                                            guadou_num=guadou_num_mind)
            mind_order_id = result_mind['charge_res']['data']['order_no']
            english_order_id = result_english['charge_res']['data']['order_no']
            order_change = self.pingxxorderQuery.get_pingxxorder(_id=mind_order_id)
            teaching_tool_price = get_mind_teach_tool_price_mind

        order_change_guadou = order_change['guadouAmount']
        total_change = order_change['total']
        discount_charge = total_change - order_change_guadou

        # 计算期望返现金额
        if level == "promoter":
            expect_commission = str((total_change - teaching_tool_price * 0.65) * 0.3 - discount_charge)
        postion = expect_commission.find('.')
        expect_commission = expect_commission[0:postion]

        if type == "mind":
            db_promoter_record = self.promoterQuery.get_promoter_own_order(_id=mind_order_id)

        for x in db_promoter_record:
            assert x['revenue'] == int(expect_commission)

    @pytest.mark.parametrize('level,type,promoter_to_partner', [("promoter", "english", "yes")])
    def test_promoter_commission_fans_extention_promoter_to_partner(self, get_commodity_detail, level, type,
                                                                    promoter_to_partner,
                                                                    get_mind_teach_tool_price_english):
        """
        粉丝拓科升级佣金计算，升级补发奖励
        测试推广人账号 15420000001 粉丝账号15420000003，粉丝已经购买了思维正价课,粉丝扩课英语，粉丝再购买正价课
        """
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user9.user_id)
        course = get_commodity_detail['english_course']
        if promoter_to_partner == "yes":
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="promoter",
                                                        totalAmount=900000)
        # 粉丝购买英语课程
        if type == "english":
            sp2xuId = course['data']['skuSpecBriefList'][0]['sp2xuId']
            guadou_num = int(course['data']['skuSpecBriefList'][0]['priceRmb'])

        result = self.create_order(self.fan8, self.user9, channel="wx_pub",
                                   pay_price=0,
                                   sp2xu_id=sp2xuId, pay_total=0,
                                   guadou_num=guadou_num)
        order_id = result['charge_res']['data']['order_no']
        order_change = self.pingxxorderQuery.get_pingxxorder(_id=order_id)
        order_change_total = order_change['guadouAmount']
        teaching_tool_price = get_mind_teach_tool_price_english
        commision_20 = (order_change_total - teaching_tool_price * 0.65) * ((1000000 - 900000) / order_change_total)
        comission_30 = (order_change_total - teaching_tool_price * 0.65) - commision_20
        # 计算期望返佣金额
        if level == "promoter":
            expect_commission = str(commision_20 * 0.2 + comission_30 * 0.3)
            postion = expect_commission.find('.')
            expect_commission = expect_commission[0:postion]

        db_promoter_record = self.promoterQuery.get_promoter_order(_id=order_id)

        for x in db_promoter_record:
            assert x['revenue'] == int(expect_commission)

    @pytest.mark.parametrize('level', ["promoter", "partner"])
    def test_promoter_commission_crm(self, get_old_info, get_commodity_detail, level):
        """新推广人：购买普通呱美课分佣,课程正常按推广人级别比例分佣；
        测试推广人账号 15420000001 粉丝账号15420000003
        """
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user9.user_id)
        course = get_commodity_detail['pure_course']
        # 预置推广人等级
        if level == "promoter":
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="promoter",
                                                        totalAmount=0)
        else:
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="partner",
                                                        totalAmount=2000000)
        # 粉丝购买课程
        result = self.create_order(self.fan8, self.user9, channel="wx_pub", pay_price=0,
                                   sp2xu_id=course['data']['skuSpecBriefList'][0]['sp2xuId'], pay_total=0,
                                   guadou_num=int(course['data']['skuSpecBriefList'][0]['priceRmb']))
        # 判断是否按分佣比例分佣
        order_id = result['charge_res']['data']['order_no']
        order_change = self.pingxxorderQuery.get_pingxxorder(_id=order_id)
        order_change_total = order_change['guadouAmount']
        # 计算期望返佣金额
        if level == "promoter":
            expect_commission = str(order_change_total * 0.2)
        else:
            expect_commission = str(order_change_total * 0.3)
        postion = expect_commission.find('.')
        expect_commission = expect_commission[0:postion]

        db_promoter_record = self.promoterQuery.get_promoter_order(_id=order_id)

        for x in db_promoter_record:
            assert x['revenue'] == int(expect_commission)

    @pytest.mark.parametrize('level', ["promoter", "partner"])
    def test_partner_commission_read(self, get_old_info, get_commodity_detail, level):
        """新推广人：购买呱呱阅读分佣,课程正常按推广人级别比例分佣；
        测试推广人账号 15420000001 粉丝账号15420000003
        """
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user9.user_id)
        course = get_commodity_detail['read_course']
        # 预置推广人等级
        if level == "promoter":
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="promoter",
                                                        totalAmount=0)
        else:
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="partner",
                                                        totalAmount=2000000)
        # 粉丝购买课程
        result = self.create_order(self.fan8, self.user9, channel="wx_pub", pay_price=0,
                                   sp2xu_id=course['data']['skuSpecBriefList'][0]['sp2xuId'], pay_total=0,
                                   guadou_num=int(course['data']['skuSpecBriefList'][0]['priceRmb']))
        # 判断是否按分佣比例分佣
        order_id = result['charge_res']['data']['order_no']
        order_change = self.pingxxorderQuery.get_pingxxorder(_id=order_id)
        order_change_total = order_change['guadouAmount']
        # 计算期望返佣金额
        expect_commission = str(order_change_total * 0.3)
        postion = expect_commission.find('.')
        expect_commission = expect_commission[0:postion]

        db_promoter_record = self.promoterQuery.get_promoter_order(_id=order_id)

        for x in db_promoter_record:
            assert x['revenue'] == int(expect_commission)

    @pytest.mark.parametrize('level', ["promoter", "partner"])
    def test_partner_commission_disney_course(self, get_old_info, get_commodity_detail, level):
        """新推广人：购买迪斯尼分佣,课程正常按推广人级别比例分佣；
        测试推广人账号 15420000001 粉丝账号15420000003
        """
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user9.user_id)
        course = get_commodity_detail['c_course']
        # 预置推广人等级
        if level == "promoter":
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="promoter",
                                                        totalAmount=0)
        else:
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="partner",
                                                        totalAmount=2000000)
        # 粉丝购买课程
        result = self.create_order(self.fan8, self.user9, channel="wx_pub", pay_price=0,
                                   sp2xu_id=course['data']['skuSpecBriefList'][0]['sp2xuId'], pay_total=0,
                                   guadou_num=int(course['data']['skuSpecBriefList'][0]['priceRmb']))
        # 判断是否按分佣比例分佣
        order_id = result['charge_res']['data']['order_no']
        order_change = self.pingxxorderQuery.get_pingxxorder(_id=order_id)
        order_change_total = order_change['guadouAmount']
        # 计算期望返佣金额
        if level == "promoter":
            expect_commission = str(order_change_total * 0.5 * 0.2)
        else:
            expect_commission = str(order_change_total * 0.5 * 0.3)
        postion = expect_commission.find('.')
        expect_commission = expect_commission[0:postion]

        db_promoter_record = self.promoterQuery.get_promoter_order(_id=order_id)

        for x in db_promoter_record:
            assert x['revenue'] == int(expect_commission)

    @pytest.mark.parametrize('level', ["promoter", "partner"])
    def test_partner_no_commission(self, get_old_info, get_commodity_detail, level):
        """新推广人：购买不分佣课程,；
        测试推广人账号 15420000001 粉丝账号15420000003
        """
        # 设置wc_users 为当前当前用户uid
        self.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=self.user9.user_id)
        course = get_commodity_detail['no_commission_course']
        # 预置推广人等级
        if level == "promoter":
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="promoter",
                                                        totalAmount=0)
        else:
            self.promoterQuery.update_promoter_accounts(self.promoterUser9.promoter_accounts_id, level="partner",
                                                        totalAmount=2000000)
        # 粉丝购买课程
        result = self.create_order(self.fan8, self.user9, channel="wx_pub", pay_price=0,
                                   sp2xu_id=course['data']['skuSpecBriefList'][0]['sp2xuId'], pay_total=0,
                                   guadou_num=int(course['data']['skuSpecBriefList'][0]['priceRmb']))

        order_id = result['charge_res']['data']['order_no']
        db_promoter_record = self.promoterQuery.get_promoter_order(_id=order_id)
        # 判断分拥金额是否是0
        for x in db_promoter_record:
            assert x['revenue'] == 0

    @pytest.mark.parametrize('level', ["promoter", "partner"])
    def test_invalid_fan_buy_lesson(self, get_old_info, get_commodity_detail, level):
        """
        推广人无效粉丝购买正价课，不分佣
        """
        course = get_commodity_detail["pure_course"]
        # 预置推广人等级
        if level == "promoter":
            self.promoterQuery.update_promoter_accounts(self.promoterUser.promoter_accounts_id, level="promoter")
        else:
            self.promoterQuery.update_promoter_accounts(self.promoterUser.promoter_accounts_id, level="partner")
        # 无效锁粉用户购买正价课
        result = self.create_order(self.fan6, self.user, channel="wx_pub", pay_price=0,
                                   sp2xu_id=course['data']['skuSpecBriefList'][0]['sp2xuId'], pay_total=0,
                                   guadou_num=int(course['data']['skuSpecBriefList'][0]['priceRmb']))

        assert result['new_promoter_info']['totalAmount'] == get_old_info['old_promoter_info']['totalAmount']
