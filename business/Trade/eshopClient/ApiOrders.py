# coding=utf-8
# @Time    : 2020/12/3 9:55 上午
# @Author  : jerry
# @File    : ApiOrders.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiOrders:
    """
    eshop
    OrdersController
    """

    def __init__(self, wechat_token, basic_token=None):
        self.host = Domains.domain
        self.root = '/api/eshop/orders'
        self.headers = {'Authorization': basic_token, "wechattoken": wechat_token, "Content-Type": "application/json"}

    """-------------------------------------------orders相关OrdersController--------------------------------"""

    def api_verify_orders(self, itemId, promotionId, quantity, verify, useGuadou):
        """
        确认订单
        :param itemId: 商品id
        :param verifyBy: 结算方式, 0以商品编号直接结算, 1以选中购物车直接结算
        :param promotionId:活动id
        :param quantity:购买数量
        :param useGuadou:是否使用呱豆
        :return:
        """
        api_url = f'{self.host}{self.root}/verify'
        body = {
            'quantity': quantity,
            'itemId': itemId,
            'verify': verify,
            'promotionId': promotionId,
            'useGuadou': useGuadou
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_charge(self, oid, payWechatToken, guadouDiscount=0, channel="wx_pub", payTotal=0):
        """
        创建交易对象
        :param oid: 订单id
        :param channel: 支付渠道
        :param payTotal:前端显示给用户的价格（分）
        :param guadouDiscount：前端显示使用呱豆的数量，0为不使用，不传默认0
        :param payWechatToken:wx_pub, wx_lite渠道必传 服务端加密等效token
        :param payWechatTokenType:wx_pub, wx_lite渠道必传 微信授权类型
        :return:
        """
        api_url = f'{self.host}{self.root}/charge'
        body = {
            "payTotal": payTotal,
            "guadouDiscount": guadouDiscount,
            "channel": channel,
            'oid': oid,
            "pay_wechat_token_typ": "unsilent",
            "pay_wechat_token": payWechatToken
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json', headers=self.headers)
        return resp