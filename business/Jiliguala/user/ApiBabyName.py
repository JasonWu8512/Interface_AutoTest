# -*- coding: utf-8 -*-
# @Time : 2021/5/26 8:05 下午
# @Author : Cassie
# @File : ApiBabyName.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiBabyName():
    """
    userbiz  C端：宝贝姓名相关接口
    BabyNameController
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/babyname'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_name(self, bid):
        """
        查询宝贝姓名
        :param bid:宝贝id
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_update_name(self, id, gender):
        """
        修改宝贝姓名
        :param id: 宝贝id
        :gender: 性别
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
            "_id": id,
            "gender": gender,
            "tags": ["test"],
            "validTags": "true"
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("dev")
    user = UserProperty("15958112857")
    version = config['version']['ver11.0']
    token = user.basic_auth
    babaName = ApiBabyName(token, version)
    # resp = babaName.api_get_name("296ae20c4d8a43c4a705cd229c340764")
    resp = babaName.api_update_name("3aec6bbdc84048f8b9e68580390a300c", "girl")
    print(resp)
