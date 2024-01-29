# -*- coding: utf-8 -*-
# @Time : 2021/8/2 1:39 下午
# @Author : Cassie
# @File : ApiUserStrategy.py
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUserStrategy(object):
    """
    user-strategy  C端： 分流策略查询接口

    """

    def __init__(self):
        self.host = Domains.config.get('inner_url')
        self.headers = {
            "Content-Type": "application/json"
        }

    def api_get_user_strategy(self, bid, ip, subject, uid, agent):
        """
        查询用户分流结果
        :param bid:宝贝id
        :param ip:远端ip地址
        :param subject:学科科目
        :param uid:用户id
        :param agent:客户端设备信息
        :return:
        """
        api_url = "/inner/user-strategy/mark/test"
        data = {
            "babyId": bid,
            "remoteIp": ip,
            "subject": subject,
            "uid": uid,
            "userAgent": agent
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=data, method="post",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    resp = ApiUserStrategy().api_get_user_strategy(bid="e119811479fe495a9066200291c0d286",
                                                   ip="113.31.145.13",
                                                   subject="MA",
                                                   uid="08a7f26750474102a1d7af5b72d6c142",
                                                   agent="niuwa/11.8.0 (iPhone; iOS 13.6.1; Scale/3.00)")

    print(resp)
