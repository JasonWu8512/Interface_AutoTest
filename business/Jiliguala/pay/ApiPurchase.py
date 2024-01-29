# coding=utf-8
# @Time    : 2020/11/19 3:49 下午
# @Author  : jerry
# @File    : ApiPurchase.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty
from retry import retry

class ApiPurchase:
    """
    pay
    PurchaseController
    """

    def __init__(self, token):
        """
        :param token:
        """
        self.root = "/api/pingpp"
        self.headers = {"Authorization": token, "version": "1",
                        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; M15 Build/N2G47H); NiuWa : 223; AndroidVersion : 10.5.0",
                        "X-App-Params": "deviceId=867343030872952&deviceType=Meizu M15"}
        self.host = Domains.domain

    def api_pingpp_charge(self, channel, bid, itemid, guadou, nonce):
        """
        支付订单
        """
        api_url = f"{self.root}/charge"
        body = {
            "guadou": guadou,
            "channel": channel,
            "bid": bid,
            "itemid": itemid,
            "nonce": nonce
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp

    @retry(tries=10, delay=3)
    def api_pingpp_purchase(self, physical, bid, channel, itemid):
        """
        支付订单,app内购买呱美课
        :param physical:
        :param bid:
        :param channel: 支付渠道
        :param itemid: 课程id
        :return:
        """
        api_url = f"{self.root}/purchase"
        body = {
            "physical": physical,
            "channel": channel,
            "bid": bid,
            "itemid": itemid
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        if resp.get('status') == 500:
            raise Exception("接口服务异常")
        return resp

if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    user = UserProperty("13700000022")
    ord = ApiPurchase(token=user.basic_auth)
    res = ord.api_pingpp_purchase(physical=False, channel="alipay", bid=user.babies_id, itemid="CRM_H5_ST_K1_6_0")
    # res = ord.api_xx_paid(bid="224effb968cc4da3a02ac87f9c78af20")
    # res = ord.api_pingpp_charge(channel='wx', bid='224effb968cc4da3a02ac87f9c78af20', itemid='ReadingVIPLifetime', guadou='38800', nonce='5a319da8-5a1e-471f-ac77-194706d97460')
    print(res)
    # print(re)