# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiRedeem(object):
    """
    赠送vip
    """
    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def api_circulars_redeem(self, itemId):
        """
        生成兑换码
        """
        api_url = "/api/circulars/redeem"
        body = {
            "number": 1,
            "itemId": itemId,
            "channel": "test"
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    def api_redeem_exchange(self, code):
        """
        兑换
        """
        api_url = "/api/redeem/exchange"
        body = {"code": code}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    def api_redeem_refund(self, code):
        """
        退款
        """
        api_url = "/api/circulars/redeem/refund"
        body = {"codes": [code]}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp


if __name__ == '__main__':

    dm = Domains()
    dm.set_env_path('dev')
    dm.set_domain("https://devggr.jiliguala.com")

    # 生成兑换码
    mobile = '18621149482'
    user1 = UserProperty(mobile)
    token1 = user1.basic_auth
    redeem1 = ApiRedeem(token=token1)
    res = redeem1.api_circulars_redeem("LexileTestOnce_180")
    code = res['data']['code'][0]

    # 兑换
    user2 = UserProperty("13162592038")
    token2 = user2.basic_auth
    redeem2 = ApiRedeem(token=token2)
    res = redeem2.api_redeem_exchange(code)

    # 注销兑换码
    r = redeem1.api_redeem_refund(code)
    print(res)