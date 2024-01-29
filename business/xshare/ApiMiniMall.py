# coding=utf-8
# @Time    : 2020/9/9 11:07 上午
# @Author  : keith
# @File    : ApiMiniMall

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.businessQuery import openuserQuery


# done
class ApiMiniMall(object):
    """
    转介绍 小程序商城
    """

    def __init__(self, token):
        self.root = "/api/xshare/mini/mall"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain
        self.gateway_host = Domains.get_gateway_host()

    def api_bind_mobile(self):
        """
        绑定手机号
        转发: /api/openapp/sp99/bind
        :return:
        """
        api_url = "{}/bind".format(self.root)
        body = {
        }
        resp = send_api_request(url=self.gateway_host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp

    def api_get_mobile_bind_status(self):
        """
        小程序查询绑定状态
        转发：/api/openapp/sp99/bind/status
        :return:
        """
        api_url = "{}/bind/status".format(self.root)
        resp = send_api_request(url=self.gateway_host + api_url, paramType='params', method="get",
                                headers=self.wx_headers)
        return resp

    def api_get_order_status(self, uid):
        """
        查询订单状态
        转发：/api/openapp/sp99/order/status
        :param uid:
        :return:
        """
        api_url = "{}/order/status".format(self.root)
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.gateway_host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_get_order_info(self):
        """
        查询订单状态
        转发：/api/openapp/sp99/order/info
        :return:
        """
        api_url = "{}/order/info".format(self.root)
        resp = send_api_request(url=self.gateway_host + api_url, paramType='params', method="get",
                                headers=self.wx_headers)
        return resp

    def api_save_address_sms(self, oid, receiver):
        """
        通过短信中的链接保存地址
        转发： /api/xshare/mini/mall/order/addr-sms
        :param oid:
        :param receiver:
        :return:
        """
        api_url = "{}/order/addr-sms".format(self.root)
        body = {
            "oid": oid,
            "receiver": receiver
        }
        resp = send_api_request(url=self.gateway_host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp

    def api_input_address(self, name, tel, region, addr):
        """
        H5商城填地址
        :param name:
        :param tel:
        :param region:
        :param addr:
        :return:
        """
        api_url = "{}/mini/mall/address".format(self.root)
        body = {
            "name": name,
            "tel": tel,
            "region": region,
            "addr": addr
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp

    def api_get_initiator_info(self, initiator):
        """
        查询当前用户的邀请人信息，目前包括微信头像和昵称
        :param initiator:
        :return:
        """
        api_url = "{}/mini/mall/initiator/info".format(self.root)
        body = {
            "initiator": initiator,
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    db = openuserQuery()
    token = db.get_openuser(mobile='13818207214')['sp99']['token']
    mall = ApiMiniMall(token="Token {}".format(token))
    # 4e34156167077d3c4ebf457f190dca9d
    # user.get_token(typ='mobile', u=18818207214, p=123456)
    mall.api_get_order_status("123")
