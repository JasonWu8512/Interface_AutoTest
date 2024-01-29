# -*- coding: utf-8 -*-
# @Time: 2021/4/19 10:26 上午
# @Author: ian.zhou
# @File: RedeemController
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiRedeem:
    """
    兑换码
    """
    root = '/api/eshop/redeem'

    def __init__(self, token):
        self.headers = {'Authorization': token, "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_use_redeem(self, redeemNo, needAddress=False, recipient='测试订单', mobile='12345678901',
                       addressProvince='黑龙江省', addressCity='双鸭山市', addressDistrict='宝山区',
                       addressStreet='测试地址'):
        """
        使用兑换码兑换
        :param redeemNo: 兑换码
        :param needAddress: 是否需要地址
        :param recipient: 收货地址: 收件人
        :param mobile: 收货地址: 收件人手机号
        :param addressProvince: 收货地址: 省份/自治区/直辖市
        :param addressCity: 收货地址: 市
        :param addressDistrict: 收货地址: 区/县
        :param addressStreet: 收货地址: 详细地址
        :return:
        """

        api_url = f'{self.host}{self.root}'
        body = {
            'redeemNo': redeemNo
        }
        if needAddress:
            body = {
                'redeemNo': redeemNo,
                'recipient': recipient,
                'mobile': mobile,
                'addressProvince': addressProvince,
                'addressCity': addressCity,
                'addressDistrict': addressDistrict,
                'addressStreet': addressStreet
            }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    user = UserProperty(mobile='17621026961')
    redeem = ApiRedeem(token=user.basic_auth)
    print(redeem.api_use_redeem(redeemNo='7B6E6ipTRnGyce', needAddress=True))

