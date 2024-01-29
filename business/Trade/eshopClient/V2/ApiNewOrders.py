# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 12:07 下午
# @Author  : zoey
# @File    : ApiNewOrders.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiNewOrders:
    """
    eshop H5商城
    """
    root = '/api/eshop/v2/orders'

    def __init__(self, token):
        self.headers = {'Authorization': token, "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_order_verify(self, sp2xuId, payPrice=0, number=1, shipping=True, useGuadou=True, guaDouNum=None,
                         recipientInfo=None, promotionId=None, marketingChannel=None, groupId=None, promoterId=None,
                         userRemarks=None):
        """
        订单确认（购买页）
        :param sp2xuId: spu->s[kg]u 映射id
        :param payPrice: 支付金额
        :param number: 购买数量
        :param shipping: 是否包邮
        :param recipientInfo: 收货人信息
        :param promotionId: 活动id
        :param useGuadou: 是否使用呱豆
        :param guaDouNum: 使用呱豆数量
        :param marketingChannel: 订单渠道字符串:1班主任 2上海规划师 3武汉规划师
        :param groupId: 团id，参团购买时传入
        :param promoterId: 推广人id
        :param userRemarks: 用户备注
        :return:
        """

        api_url = f'{self.host}{self.root}/verify'
        body = {
            'sp2xuId': sp2xuId,
            'payPrice': payPrice,
            'number': number,
            'shipping': shipping,
            'recipientInfo': recipientInfo,
            'promotionId': promotionId,
            'useGuadou': useGuadou,
            'guaDouNum': guaDouNum,
            'marketingChannel': marketingChannel,
            'groupId': groupId,
            'promoterId': promoterId,
            'userRemarks': userRemarks
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_order_create(self, sp2xuId, payPrice, number=1, shipping=True, useGuadou=True, guaDouNum=0,
                         promotionId=None, marketingChannel=None, groupId=None, promoterId=None, userRemarks=None,
                         recipient='测试订单', mobile='12345678901', addressProvince='黑龙江省', addressCity='双鸭山市',
                         addressDistrict='宝山区', addressStreet='测试地址'):
        """
        创建订单
        :param sp2xuId: spu->s[kg]u 映射id
        :param payPrice: 支付金额
        :param number: 购买数量
        :param shipping: 是否包邮
        :param promotionId: 活动id
        :param useGuadou: 是否使用呱豆
        :param guaDouNum: 使用呱豆数量
        :param marketingChannel: 订单渠道字符串:1班主任 2上海规划师 3武汉规划师
        :param groupId: 团id，参团购买时传入
        :param promoterId: 推广人id
        :param userRemarks: 用户备注
        :return:
        """

        api_url = f'{self.host}{self.root}'
        body = {
            'sp2xuId': sp2xuId,
            'payPrice': payPrice,
            'number': number,
            'shipping': shipping,
            'recipientInfo': {
                'recipient': recipient,
                'mobile': mobile,
                'addressProvince': addressProvince,
                'addressCity': addressCity,
                'addressDistrict': addressDistrict,
                'addressStreet': addressStreet
            },
            'promotionId': promotionId,
            'useGuadou': useGuadou,
            'guaDouNum': guaDouNum,
            'marketingChannel': marketingChannel,
            'groupId': groupId,
            'promoterId': promoterId,
            'userRemarks': userRemarks
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_order_match_verify(self, sp2xuId, orderNo, promotionId=None, groupId=None):
        """
        订单匹配确认
        :param sp2xuId: spu->s[kg]u 映射id
        :param orderNo: 订单号
        :param promotionId: 活动id
        :param groupId: 团id
        :return:
        """

        api_url = f'{self.host}{self.root}/match/verify'
        body = {
            'sp2xuId': sp2xuId,
            'orderNo': orderNo,
            'promotionId': promotionId,
            'groupId': groupId,
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_charge_create(self, oid, channel, payTotal, guadouDiscount=0, payWechatToken=None,
                          payWechatTokenTyp='silent', resultUrl=None, successUrl=None, hbFqNum=None):
        """
        创建交易
        :param oid: 订单号
        :param channel: 支付渠道
        :param payTotal: 支付金额
        :param guadouDiscount: 呱豆抵扣
        :param payWechatToken: 服务端加密等效token wx_pub, wx_lite渠道必传
        :param payWechatTokenType: 授权类型
        :param resultUrl: wx_wap渠道支付完成的回调地址
        :param successUrl: alipay_wap渠道支付成功的回调地址
        :param hbFqNum: 支付宝花呗分期期数
        :return:
        """

        api_url = f'{self.host}{self.root}/charge'
        body = {
            'oid': oid,
            'channel': channel,
            'payTotal': payTotal,
            'guadouDiscount': guadouDiscount,
            'pay_wechat_token': payWechatToken,
            'pay_wechat_token_typ': payWechatTokenTyp,
            'extra': {
                'result_url': resultUrl,
                'success_url': successUrl,
                'hb_fq_num': hbFqNum
            }
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_edit_order_address(self, orderNo, recipient='测试订单', mobile='12345678901', addressProvince='黑龙江省',
                               addressCity='双鸭山市', addressDistrict='宝山区', addressStreet='测试地址'):
        """
        修改订单地址
        :param orderNo: 订单号
        :param recipient: 收货地址: 收件人
        :param mobile: 收货地址: 收件人手机号
        :param addressProvince: 收货地址: 省份/自治区/直辖市
        :param addressCity: 收货地址: 市
        :param addressDistrict: 收货地址: 区/县
        :param addressStreet: 收货地址: 详细地址
        :return:
        """

        api_url = f'{self.host}{self.root}/address'
        body = {
            'orderNo': orderNo,
            'receiver': {
                'recipient': recipient,
                'mobile': mobile,
                'addressProvince': addressProvince,
                'addressCity': addressCity,
                'addressDistrict': addressDistrict,
                'addressStreet': addressStreet
            }
        }
        resp = send_api_request(method='patch', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_env_path('dev')
    Domains.set_domain('https://dev.jiliguala.com')
    user = UserProperty(mobile='17777766666')
    eshop = ApiNewOrders(token=user.basic_auth)
    # print(eshop.api_order_verify(sp2xuId=969, payPrice=200, promotionId='DACT_420'))
    order = eshop.api_order_create(sp2xuId=2143, payPrice=48800, useGuadou=False)
    print(order)
    order_no = order['data']['orderNo']
    # print(eshop.api_order_match_verify(sp2xuId=969, orderNo=order_no, promotionId='DACT_420'))
    # print(eshop.api_edit_order_address(orderNo=order_no, recipient='修改地址'))
    res = eshop.api_charge_create(oid=order_no, channel='wx_pub', payTotal=48800)
    print(res)
