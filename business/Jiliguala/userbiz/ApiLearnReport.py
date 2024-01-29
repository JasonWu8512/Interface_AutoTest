# -*- coding: utf-8 -*-
# @Time : 2021/5/28 3:00 下午
# @Author : Anna
# @File : ApiAddress.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAddress():
    """
    查询用户默认地址信息
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/user/address'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_address(self):
        """
        查询用户默认地址信息（get）
        :return:
        """
        api_url = f"{self.host}{self.root}"
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp

    def api_put_address(self, name, mobile, region, address):
        """
        查询用户默认地址信息（put）
        :param name:收件人姓名
        :param mobile:收件人手机号
        :param region:地区【省、市、县】
        :param address:详细地址
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
            "name": name,
            "mobile": mobile,
            "region": region,
            "address": address
        }
        resp = send_api_request(url=api_url, method="put", headers=self.headers, paramType="json", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19393123455")
    token = user.basic_auth
    version = config['version']['ver11.6']
    address = ApiAddress(token, version)
    # 测试查询默认地址接口
    resp = address.api_get_address()
    print(resp)

    # 测试填写地址接口
    resp01 = address.api_put_address('tester', '19696969696', '北京市 东城区', '测试订单地址')
    print(resp01)
