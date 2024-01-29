# coding=utf-8
"""
@Time    : 2022/6/23 10:40 下午
@Author  : Anna
@File    : ApiXx
"""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiXx():
    """
    正价课首购后跳转规划师页面
    """

    def __init__(self, token, version=None):
        """
        :param token:
        """

        self.host = Domains.config.get('url')
        self.root = '/api/xx'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version}

    def api_get_xx_paid(self, bid, itemid, level):
        """
        正价课首购后跳转规划师页面
        :param bid: 宝贝ID
        :param itemid: 课程ID
        :param level: 课程级别
        :return:
        """
        api_url = f"{self.root}/paid"
        body = {
            "bid": bid,
            "itemid": itemid,
            "level": level
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
    xx = ApiXx(token, version)
    # 正价课首购后跳转规划师页面
    res1 = xx.api_get_xx_paid("467f0668aeec404382e504cd5731e994", "F1_S1-6_WITHOUTDISCOUNT", 'K1GE')
    print(res1)
