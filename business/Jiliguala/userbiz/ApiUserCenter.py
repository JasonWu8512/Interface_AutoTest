# -*- coding: utf-8 -*-
# @Time : 2021/6/3 13:00 下午
# @Author : nana
# @File : ApiUserCenter.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiUserCenter():
    """
    /api/user/center    10.5以下版本 家长中心
    /api/user/center/v2 10.5及以上版本 家长中心
    /api/user/center/v3 11.5及以上版本 我的tab(家长中心)
    """
    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root1 = '/api/user/center'
        self.root2 = '/api/user/center/v2'
        self.root3 = '/api/user/center/v3'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_usercenter(self, bid, id , level):
        """
        获取10.5以下版本 家长中心数据
        :param bid:宝贝
        :param id:用户UID
        :param level:当前所在级别
        :return:
        """
        api_url = f"{self.host}{self.root1}"
        body = {
            "bid": bid,
            "id": id,
            "level": level
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


    def api_get_usercenter_v2(self, bid, id , level):
        """
        10.5及以上版本 家长中心数据
        :param bid:宝贝
        :param id:用户UID
        :param level:当前所在级别
        :return:
        """
        api_url = f"{self.host}{self.root2}"
        body = {
            "bid": bid,
            "id": id,
            "level": level
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_usercenter_v3(self, bid, id):
        """
        获取11.4及以上家长中心数据
        :param bid:宝贝
        :param id:用户UID
        :return:
        """
        api_url = f"{self.host}{self.root3}"
        body = {
            "bid": bid,
            "id": id
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp



if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("13242040693")
    token = user.basic_auth
    version = config['version']['ver11.6']
    usercenter = ApiUserCenter(token, version)

    # /api/user/center
    resp = usercenter.api_get_usercenter('b1d4ffd0b19b4dd9b8e5aeb29c13ac0d', '5286509c471e48bbb2705985d695dea2', 'L1XX')
    print(resp)

    # /api/user/center/v2
    resp = usercenter.api_get_usercenter_v2('b1d4ffd0b19b4dd9b8e5aeb29c13ac0d', '5286509c471e48bbb2705985d695dea2', 'T1GE')
    print(resp)

    #/api/user/center/v3
    resp = usercenter.api_get_usercenter_v3('ee46b9f8738b4b3a9472d95de1d74003','5286509c471e48bbb2705985d695dea2')
    print(resp)
