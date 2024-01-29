# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2022/6/23 11:05 上午
@Author   : Anna
@File     : ApiHome.py
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiExperiment():
    def __init__(self, token, version=None):
        self.host = Domains.config.get('url')
        self.root = '/api/experiment'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_experiment(self, bid, expKeys, uid):
        """
        查询首页模式
        :param bid:宝宝id
        :param expKeys:实验id
        :param uid:用户id
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
            "bid": bid,
            "expKeys": expKeys,
            "uid": uid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19494123420")
    token = user.basic_auth
    version = config["version"]['ver12.1']
    expKeys = 'HOME_V11_8_AB_EXP' + '%2' + 'CSPU_DETAIL_V11_8_AB_EXP'
    print(expKeys)

    # 查询用户模式（v4/v5）
    experiment = ApiExperiment(token, version)
    resp = experiment.api_get_experiment("ff74079aa22c4afc858b8541722487a4",
                                         expKeys,
                                         "36cf640b79e2416f919dc8c1157c2f60")
    print(resp)
