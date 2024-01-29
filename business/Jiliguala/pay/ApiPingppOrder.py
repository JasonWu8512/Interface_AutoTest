# coding=utf-8
# @Time    : 2020/8/11 6:16 下午
# @Author  : keith
# @File    : ApiPingPPOrder

from retry import retry
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from utils.format.format import now_timeStr
from business.common.UserProperty import UserProperty


class ApiPingppOrder(object):
    """
    处理ping++订单
    """

    def __init__(self, token, wechattoken=None):
        """
        :param token:
        """
        self.root = "/api/pingpp"
        self.headers = {"Authorization": token, "version": "1",
                        "User-Agent": "niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)"}
        self.wxapp_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                              "content-Type": "application/json"}
        self.wechat_headers = {'wechattoken': wechattoken, 'Authorization': token, "version": "1"}
        self.host = Domains.domain

    def api_get_order_detail(self, oid):
        """
        单个订单详情
        :param oid: 订单ID
        :return:
        """
        api_url = f"{self.root}/order/detail"
        body = {
            "oid": oid,
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_get_order(self, oid):
        """
        订单轮询
        :param oid:
        :return:
        """
        api_url = f"{self.root}/order"
        body = {
            "oid": oid,
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_get_order_list(self, page):
        """
        订单列表
        :param page:
        :return:
        """
        api_url = f"{self.root}/order/list"
        body = {
            "page": page,
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_get_order_logistics(self, oid):
        """
        订单物流
        :param oid:
        :return:
        """
        api_url = f"{self.root}/order/logistics"
        body = {
            "oid": oid,
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_get_order_coupon(self, itemid, bid):
        """
        优惠券列表
        :param itemid:
        :param bid:
        :return:
        """
        api_url = f"{self.root}/coupon"
        body = {
            "itemid": itemid,
            "bid": bid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_order_purchase(self, physical, bid, channel, itemid):
        """
        支付订单
        :param physical:
        :param bid:
        :param channel: 支付渠道
        :param itemid: 课程id
        :return:
        """
        api_url = f"{self.root}/purchase"
        body = {
            "physical": physical,
            "channel": channel,
            "bid": bid,
            "itemid": itemid
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    @retry(tries=10, delay=3)
    def api_put_physical_order(self, itemid, openuid=None, openapp=None, purchaseType=None, campaign=None, nonce=None,
                               account=None,
                               wechat_token=None, xshareInitiator=None, sharer=None):
        """
        生成订单
        :param itemid:
        :param openuid:
        :param openapp:
        :param purchaseType:
        :param clickId: 朋友圈广告投放渠道 字段
        :return:
        """
        api_url = f"{self.root}/physical/order"
        if openapp:
            body = {
                "itemid": itemid,
                "openuid": openuid,
                "openapp": openapp,
                "purchaseType": purchaseType,
                "campaign": campaign,
            }
            resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="put",
                                    headers=self.wxapp_headers)
        elif account:
            body = {
                'itemid': itemid,
                'nonce': nonce,
                'account': account,
                'typ': "unsilent",
                'wechat_token': wechat_token,
                'source': "AppHomeView",
                'xshareInitiator': xshareInitiator,
                'sharer': sharer,
                'welfare': False
            }
            resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="put",
                                    headers=self.wechat_headers)
        if resp.get('status') == 500:
            raise Exception("接口服务异常")
        return resp

    @retry(tries=10, delay=3)
    def api_physical_order_charge(self, oid, channel, openid):
        """
        支付订单
        :param oid: 订单号
        :param channel: 99渠道：wx_lite
        :param openid: 用户openid
        :return:
        """
        api_url = f"{self.root}/physical/order/charge"
        body = {
            "oid": oid,
            "channel": channel,
            "openid": openid
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        if resp.get('status') == 500:
            raise Exception("接口服务异常")
        return resp

    def api_order_refund(self, order_id, desc=None, amount=None):
        """
        未服务化
        订单退款 - role-ta权限鉴权
        :param order_id: 订单id
        :param desc: 备注描述
        :param amount: 部分退款金额
        :return:
        """
        api_url = f"/api/circulars/pingpp/refund"
        body = {}
        if desc is None and amount is None:
            body = {
                "id": order_id,
            }
        elif amount is None:
            body = {
                "id": order_id,
                "desc": desc,
            }
        elif desc is None:
            body = {
                "id": order_id,
                "amount": amount,
            }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wxapp_headers)
        return resp

    def api_charge_callback(self, click_id):
        """
        支付回调 - 未服务化
        :param click_id:
        :return:
        """
        api_url = f"{self.root}/charge/callback"
        body = {
            "click_id": click_id,
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wxapp_headers)
        return resp

    def api_get_realobject(self, oid):
        """
        查询打卡订单详情
        :param oid:订单号
        :return:
        """
        api_url = f"{self.root}/realobject"
        body = {
            "oid": oid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_check_address(self, region, addr, oid, tel, name):
        """
        填写打卡订单的收货地址
        :param region:省市区
        :param addr:详细地址
        :param oid:订单号
        :param tel:手机号
        :param tel:姓名
        """
        api_url = f"{self.root}/realobject/address"
        body = {
            "region": region,
            "addr": addr,
            "oid": oid,
            "tel": tel,
            "name": name,
            "zip": ""
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    def api_check_order(self, oid, comment, ttl):
        """
        提交打卡订单
        :param oid:订单号
        :param comment:备注
        :param ttl:商品名称
        """
        api_url = f"{self.root}/realobject/order"
        body = {
            "oid": oid,
            "comment": comment,
            "ttl": ttl
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://fat.jiliguala.com")
    token = UserProperty('19000000020').basic_auth
    # ord = ApiPingppOrder("Basic MTlkZWJkZDU3YmZhNGI0MThiNTg5YTEwNWI1NjA3ZmE6N2JjZGFhOWQ3MjI4NDI3MGFjZTlmYTAwNTk0YzNkYzU=")
    wechattoken = UserProperty('18720996803').encryptWechatToken_pingpp
    ord = ApiPingppOrder(token=token, wechattoken=wechattoken)
    # res = ord.api_put_physical_order(itemid='H5_Sample_DiamondActivity_Lv0', nonce=now_timeStr(),
    #                                  account='wxf78b28c6562d3c56',
    #                                  wechat_token=wechattoken, xshareInitiator='3c460a8ff2464d8fafdf0b235b83c335',
    #                                  sharer='3c460a8ff2464d8fafdf0b235b83c335')
    # print(res)
    # re = ord.api_physical_order_charge(oid=res['data']['_id'], channel='wx_pub',
    #                                    openid=UserProperty('18720996803').wc_openusers2_openId)
    # print(re)
    # db = xshareQuery()
    # token = db.get_open_user_token("13818207214")
    # order = ApiPingppOrder(token="Token {}".format(token))
    # # user.get_token(typ='mobile', u=18818207214, p=123456)
    # order.api_charge_callback("123")
    # order.api_physical_order()
    res1 = ord.api_get_realobject(oid="P_award_i2_R")
    # res1 = ord.api_check_address(region="天津市 天津市 和平区", addr="给v寻寻常常", oid="P_award_i2_R", tel="18868877521",
    #                              name='king')
    # res1 = ord.api_check_order(oid="P_award_i2_R", comment="自动化测试", ttl="呱呱书包")
    print(res1)
