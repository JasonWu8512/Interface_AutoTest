# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2022/7/26  6:36 下午
@Author   : Anna
@File     : ApiSuper.py
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSuper():
    def __init__(self, token, agent):
        self.host = Domains.config.get('url')
        self.root = '/api/super'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "User-Agent": agent
        }

    def api_get_lessonbuy(self, source, type):
        """
        购买详情页
        @param source:来源
        @param type：课程类型
        @return：
        """
        api_url = f"{self.host}{self.root}/lesson/buy"
        body = {
            "source": source,
            "type": type
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_paydetail(self, itemid, couponTypActivity=None):
        """
        收银台
        @param itemid:课程id
        @param couponTypActivity:优惠券信息
        @return：
        """
        api_url = f"{self.host}{self.root}/paydetail"
        body = {
            "itemid": itemid
        }
        if couponTypActivity:
            body['couponTypActivity'] = couponTypActivity

        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_post_purchase(self, bid, itemid, physical, channel, extendMap=None, couponid=None):
        """
        客服端下单接口
        @param bid:宝贝id
        @param itemid：课程id
        @param physical：是否包含实体
        @param channel：渠道
        @param extendMap:会场信息
        @param couponid: 活动信息
        @return:
        """
        api_url = f"{self.host}/api/pingpp/purchase"
        body = {
            "bid": bid,
            "itemid": itemid,
            "physical": physical,
            "channel": channel
        }
        if extendMap:
            body['extendMap'] = extendMap
        if couponid:
            body['couponid'] = couponid

        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_post_purchase01(self, bid, itemid, physical, channel, couponid):
        """
        客服端下单接口
        @param bid:宝贝id
        @param itemid：课程id
        @param physical：是否包含实体
        @param channel：渠道
        @param couponid:优惠券--可选参数
        @return:
        """
        api_url = f"{self.host}/api/pingpp/purchase"
        body = {
            "bid": bid,
            "itemid": itemid,
            "physical": physical,
            "channel": channel,
            "couponid": couponid
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_get_order(self, oid):
        """
        订单轮询
        @param oid:订单id
        @return:
        """
        api_url = f"{self.host}/api/pingpp/order"
        body = {
            "oid": oid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_Corder(self, bid, channel, guadou, itemid):
        """
        C类课程生成订单
        @param bid:宝贝id
        @param channel:购买方式
        @param guadou:C类订单金额
        @param itemid:课程id
        @return:
        """
        api_url = f"{self.host}/api/pingpp/charge"
        body = {
            "bid": bid,
            "channel": channel,
            "guadou": guadou,
            "itemid": itemid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_post_result(self, oid):
        """
        订单轮询
        @param oid:订单id
        @return:
        """
        api_url = f"{self.host}/api/pingpp/charge/result"
        body = {
            "oid": oid
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_post_refund(self, orderNo):
        """
        mock退款
        @param oid:订单id
        @return:
        """
        api_url = f"{self.host}/api/trade-order/refund"
        body = {
            "orderNo": orderNo
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_post_coupon(self, type, couponTyp):
        """
        领取优惠券
        @param type:课程类型
        @param couponTyp:优惠券类型
        @return:
        """
        api_url = f"{self.host}/api/ab/v86/coupon"
        body = {
            "type": type,
            "couponTyp": couponTyp
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_post_mock(self, id, time_paid, order_no, transaction_no):
        """
        mock支付
        @param id:付款单
        @param time_paid:支付时间
        @param order_no:订单编号
        @param transaction_no:支付id
        @return:
        """
        api_url = f"{self.host}/api/mock/pingpp/charge/callback"
        body = {
            "type": "charge.succeeded",
            "data": {
                "object": {
                    "id": id,
                    "time_paid": time_paid,
                    "order_no": order_no,
                    "transaction_no": transaction_no
                }
            }
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19393123455")
    token = user.basic_auth
    agent = config['agent']['ios_11.12.3']
    buy = ApiSuper(token, agent)
    # resp = buy.api_get_lessonbuy("shopping_tab", "S1GE_W1-6")
    # print(resp)
    # resp01 = buy.api_get_paydetail("K3MATC_99")
    # print(resp01)

    # resp01 = buy.api_get_paydetail("L3XX")
    # print(resp01)

    # resp02 = buy.api_post_purchase("2d47d1f9e702483d95510f86f8c833e6", "L3XX", "false", "guadou")
    # print(resp02)
    # oid = resp02['data']["oid"]
    resp = buy.api_post_mock(id='ch_101231110595063797760019', time_paid='1699603711', order_no='OT89231080501571584',
                             transaction_no='MOCK4200001986202311086580233366')
    print(resp)

    # resp03 = buy.api_get_order(oid)
    # print(resp03)
    # resp04 = buy.api_post_result(oid)
    # print(resp04)
    # # 还原数据
    # resp05 = buy.api_post_refund(oid)
    # print(resp05)
