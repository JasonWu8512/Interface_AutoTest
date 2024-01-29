# -*- coding: utf-8 -*-
# @Time : 2021/6/1 3:41 下午
# @Author : Cassie
# @File : ApiCheck.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCheck():
    """
    activity  C端：老呱美1.5打卡活动页相关接口
    CheckApiController
    """

    def __init__(self, token, version, agent):
        self.host = Domains.config.get('url')
        self.root = '/api/check'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version,
            "User-Agent": agent
        }

    def api_get_meta(self, bid):
        """
        打卡进度查询
        :param bid:宝贝id
        :return:
        """
        api_url = f"{self.host}{self.root}/meta"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_config(self):
        """
        打卡活动奖品配置信息查询
        :return:
        """
        api_url = f"{self.host}{self.root}/common/config"
        body = {}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19000000020")
    token = user.basic_auth
    version = config['version']['ver11.6']
    agent = config['agent']['ios_11.6']
    check = ApiCheck(token, version, agent)
    resp = check.api_get_meta("107a2627821d4cfd8992bd1e45a9355e")
    # resp = check.api_get_config()
    print(resp)
