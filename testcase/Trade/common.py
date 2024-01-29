# -*- coding: utf-8 -*-
# @Time: 2021/5/21 4:44 下午
# @Author: ian.zhou
# @File: common
# @Software: PyCharm

from business.zero.mock.ApiMock import ApiMock
from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from business.Trade.eshopAdmin.ApiPromotionActivity import ApiPromotionActivity
from business.Trade.eshopClient.V2.ApiV2Commodity import ApiV2Commodity
from business.Trade.eshopClient.V2.ApiNewOrders import ApiNewOrders
from business.common.UserProperty import UserProperty
from business.Trade.tradeOrder.ApiRefundOpenFeign import ApiRefund
from business.businessQuery import pingxxorderQuery
from business.mysqlQuery import EshopQuery
from utils.format.format import dateToTimeStamp, time
import shortuuid


class CommodityCommon:

    def __init__(self, a_token):
        self.a_commodity = ApiCommodity(token=a_token)
        self.a_promotion = ApiPromotionActivity(token=a_token)

    def create_sgu(self, subject, sku_list: list, price_rmb=1000):
        """
        新建一个SGU
        :param sku_list: 需要包含的SKU的编号，列表，支持传入多个
        :param subject: sgu科目 英语：1 思维：3
        :param price_rmb: sgu售价
        :return sgu_id: sgu id
        :return sgu_id: sgu编号
        """
        # 构造SKUList
        skus = []
        for sku_no in sku_list:
            sku_id = self.a_commodity.api_get_sxu_list(commodityNo=sku_no, priceBy=0)['data']['content'][0]['id']
            skus.append({'id': sku_id, 'free': 0, 'num': 1})
        # 手动构造一个SGU的payload
        sgu_payload = {
            'title': '接口自动化测试',
            'state': 1,
            'stockNum': 10000,
            'priceRmb': price_rmb,
            'priceGuaDouPp': 100,
            'purchaseLimit': 10,
            'priceTeachingTool': 0,
            'type': 2,
            'commodityNo': f'{shortuuid.uuid()}',
            'subCategoryId': subject,
            'skuList': skus
        }
        # 新建sgu
        sgu_detail = self.a_commodity.api_create_edit_sxu(sxuBody=sgu_payload)['data']
        sgu_id, sgu_no = sgu_detail['id'], sgu_detail['commodityNo']
        return sgu_id, sgu_no

    def create_spu(self, sgu_list: list):
        """
        新建一个SPU
        :param sgu_list: 需要包含的sgu的编号，列表，支持传入多个
        :return spu_id: spu id
        :return spu_id: spu编号
        """
        # 构造SGUList和spec
        included_sgu_list = []
        spec_value_list = []
        for sgu_no in sgu_list:
            sgu_id = self.a_commodity.api_get_sxu_list(commodityNo=sgu_no, sxuType=2,
                                                       priceBy=0)['data']['content'][0]['id']
            spec_value_list.append(f'{sgu_id}')
            included_sgu_list.append({'id': sgu_id, 'specValues': [f'{sgu_id}']})
        spec_name_list = [{'name': 'subject', 'specValueList': spec_value_list}]
        # 手动构造一个SPU的payload
        spu_payload = {
            'title': '接口自动化测试',
            'hbfqId': 8,
            'state': 1,
            'commodityNo': f'{shortuuid.uuid()}',
            'priceBy': 0,
            'specNameList': spec_name_list,
            'skuSpecBriefList': included_sgu_list
        }
        # 新建spu
        spu_detail = self.a_commodity.api_create_edit_spu(spuBody=spu_payload)['data']
        spu_id, spu_no = spu_detail['id'], spu_detail['commodityNo']
        return spu_id, spu_no

    def create_promotion(self, spu_no, pro_price=800, auto_complete=True):
        """
        新建一个拼团活动
        :param auto_complete: 活动类型 true：真拼团 false：假拼团
        :param spu_no: 活动SPU的编号
        :param pro_price: 活动价格（分）
        :return pro_id: 拼团活动id
        """
        # 获取SPU中包含的SXU
        spu_id = self.a_commodity.api_get_spu_list(commodityNo=spu_no)['data']['content'][0]['id']
        spu_detail = self.a_commodity.api_get_spu_detail(spuId=spu_id)['data']
        spu_no, sxu_list = spu_detail['commodityNo'], spu_detail['skuSpecBriefList']
        sxu_no = [sxu['commodityNo'] for sxu in sxu_list]
        item_ids = []
        for sxu in sxu_no:
            item_ids.append({'sxuNo': sxu, 'promotionPriceRmb': pro_price})
        # 手动构造一个SPU的payload
        pro_body = {
            'spuNo': spu_no,
            'intro': '接口自动化测试',
            'startAt': dateToTimeStamp(),
            'endAt': dateToTimeStamp(day=1),
            'autoComplete': auto_complete,
            'enable': True,
            'instantShip': True,
            'groupDuration': 3600,
            'groupSize': 3,
            'itemIds': item_ids,
            'type': 'groupon'
        }
        # 新建活动
        pro_detail = self.a_promotion.api_create_v2_promotion_activity(promotionActivityV2Body=pro_body)
        pro_id = pro_detail['data']['id']
        return pro_id


class OrderCommon:

    def __init__(self, c_user):
        c_token = UserProperty(mobile=c_user).basic_auth
        self.wechat_token = UserProperty(mobile=c_user).encryptWechatToken
        self.c_commodity = ApiV2Commodity(token=c_token)
        self.c_orders = ApiNewOrders(token=c_token)
        self.mock, self.refund = ApiMock(), ApiRefund()
        self.pingxxorder_query, self.eshop_query = pingxxorderQuery(), EshopQuery()

    def get_sp2xuid_and_price(self, spu_no, sgu_no, pro_id=None):
        """
        获取sp2xuid、当前售价
        :param spu_no: spu编号
        :param sgu_no: sgu编号
        :param pro_id: 活动id
        :return sp2xuid: spu和sgu的关联id
        :return price: 当前售价（活动时为活动价格）
        """
        detail = self.c_commodity.api_get_v2_commodity_detail(spuNo=spu_no, promotionId=pro_id)
        included_sgu_list = detail['data']['skuSpecBriefList']
        sp2xuid, price = 0, 0
        for sgu in included_sgu_list:
            if sgu['commodityNo'] == sgu_no:
                sp2xuid = sgu['sp2xuId']
                price = sgu['promotionPriceRmb'] if 'promotionPriceRmb' in sgu else sgu['priceRmb']
        return sp2xuid, price

    def purchase(self, spu_no, sgu_no, channel='wx_pub', num=1, pro_id=None, group_id=None, hbfq_num=None,
                 guadou_num=None):
        """
        创建订单支付
        :param spu_no: spu编号
        :param sgu_no: sgu编号
        :param pro_id: 活动id
        :param group_id: 团id（参团时传）
        :param channel: 支付方式
        :param hbfq_num: 花呗分期期数（支付宝支付时可选3、6、12）
        :param num: 购买数量
        :param guadou_num: 呱豆使用数量
        :return order_no: 订单号
        :return charge_id:
        """
        # 获取sp2xuid和支付价格
        sgu_info = self.get_sp2xuid_and_price(spu_no=spu_no, sgu_no=sgu_no, pro_id=pro_id)
        sp2xuid, sgu_price = sgu_info[0], sgu_info[1]
        pay_info = self.c_orders.api_order_verify(sp2xuId=sp2xuid, promotionId=pro_id, number=num,
                                                        guaDouNum=guadou_num)['data']
        price_total = pay_info['priceTotal']
        assert price_total == sgu_price * num
        pay_price, guadou_discount = pay_info['payTotal'], pay_info['guadouDiscount']
        discount = pay_info['discountDetailList'][0]['discount'] if pay_info['discountDetailList'] else 0
        assert pay_price == price_total - guadou_discount - discount
        # 创建订单
        order_no = self.c_orders.api_order_create(sp2xuId=sp2xuid, payPrice=pay_price, promotionId=pro_id,
                                                        groupId=group_id, guaDouNum=guadou_num,
                                                        number=num)['data']['orderNo']
        # 支付
        charge = self.c_orders.api_charge_create(oid=order_no, channel=channel, payTotal=pay_price,
                                                       payWechatToken=self.wechat_token, hbFqNum=hbfq_num,
                                                       guadouDiscount=guadou_num)
        charge_id = charge['data']['id']
        return order_no, charge_id

    def order_refund_and_remove(self, charge_id=None, order_no=None):
        """
        订单退款并删除
        :param order_no: 订单号
        :param charge_id: charge_id
        :return:
        """
        # 如果传入了charge_id，认为是mock订单，走mock退款接口
        if charge_id:
            res = self.mock.api_refund_mock(chargeid=charge_id)
            if res["status"] == 'succeeded':
                # 防止订单还未完成退款已将订单删除
                time.sleep(5)
                self.pingxxorder_query.delete_pingxxorder(_id=order_no)
                self.eshop_query.delete_order_by_order_no(order_no=order_no)
            order_no = None
        # 如果只传入order_no，认为是非mock订单，走真实退款接口
        if order_no:
            res = self.refund.api_order_refund(orderNo=order_no)
            if res["code"] == 200:
                # 防止订单还未完成退款已将订单删除
                time.sleep(5)
                self.pingxxorder_query.delete_pingxxorder(_id=order_no)
                self.eshop_query.delete_order_by_order_no(order_no=order_no)





