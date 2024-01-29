# coding=utf-8
"""
@Time    : 2022/6/23 6:16 下午
@Author  : Anna
@File    : ApiTrialClass
"""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiTrialClass():
    """
    9.9购买后跳转页面地址
    """

    def __init__(self, token, version=None):
        """
        :param token:
        """

        self.host = Domains.config.get('url')
        self.root = '/api/tc'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version}

    def api_get_tc_paid(self, bid, itemid):
        """
        9.9购买后跳转页面地址
        :param bid: 宝贝ID
        :param itemid: 课程ID
        :return:
        """
        api_url = f"{self.root}/paid"
        body = {
            "bid": bid,
            "itemid": itemid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("12345678001")
    token = user.basic_auth
    version = config["version"]['ver11.0']
    tc = ApiTrialClass(token, version)
    # 购买9.9后跳转的页面地址信息
    res1 = tc.api_get_tc_paid("467f0668aeec404382e504cd5731e994", "L1TC")
    print(res1)
