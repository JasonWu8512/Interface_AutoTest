# -*- coding: utf-8 -*-
# @Time : 2021/5/31 3:00 下午
# @Author : Anna
# @File : ApiCirculars.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
import json


class ApiCirculars():
    """
    家长中心-生成兑换码
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/circulars'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_post_redeem(self, itemid, channel, num):
        """
        生成兑换码
        :param itemid:产品编号
        :param channel:渠道
        :param num:生成x条
        :return:
        """
        api_url = f"{self.host}{self.root}/redeem"
        body = {
            "itemid": itemid,
            "channel": channel,
            "num": num
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_post_refund(self, id):
        """
        兑换码注销
        ：param id:兑换码
        ：return:
        """
        api_url = f"{self.host}{self.root}/redeem/refund"
        body = {
            "id": id
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    # def api_post_pprefund(self, id):
    #     """
    #     购买课程后退款
    #     :param id:订单编号
    #     ：return:
    #     """
    #     api_url = f"{self.host}{self.root}/pingpp/refund"
    #     body = {
    #         "id": id
    #     }
    #     resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
    #     return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    # 有权限限制，只有指定用户有权限的
    user = UserProperty("15921263812")
    token = user.basic_auth
    version = config['version']['ver11.0']
    circulars = ApiCirculars(token, version)

    # 测试生成兑换
    resp = circulars.api_post_redeem("L0XX", "test", 1)
    print(resp)

    # 测试兑换码注销
    # 获取生成的兑换码
    code = resp['data']['code']
    print(code)
    code01 = json.dumps(code)
    print(type(code01))
    # resp_refund = circulars.api_post_refund(code01)
    # resp_refund = circulars.api_post_refund(" "+{code01})

    resp_refund = circulars.api_post_refund("EZLL8TYZPC9M")
    print(resp_refund)

    # 测试购买课程退款
    # resp02 = circulars.api_post_pprefund("O74744609989943296")
    # print(resp02)
