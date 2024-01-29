"""
=========
Author:Lisa
time:2022/10/18 6:38 下午
=========
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from datetime import datetime
from datetime import timedelta


class ApiRedeem():
    """
    通过兑换码兑换
    ApiRedeem
    """

    def __init__(self, token=None):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "platform": "ios"
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path("fat")["gaga_url"]
        self.a_host =self.dm.set_env_path("fat")["url"]

    def redeeming(self, startTime, expireTime):
        """生成兑换码"""
        api_url = '/api/admin/overseas/redeem/createRedeem'
        body = {"eventNo": "staff_test", "eventTypeTitle": "运营活动", "redeemType": 1, "skuNo": "CG94496756",
                "redeemDistributor": "内部_用研", "channelNo": "others_bonus",
                "redeemCondition": None, "num": 1,
                "startTime": startTime, "expireTime": expireTime, "redeemCreator": "wenling_xu@jiliguala.com"}
        print(body)

        resp = send_api_request(url=self.a_host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp
    def api_redeem_redeeming(self, redeemNo):
        """
        家长中心-兑换
        redeemNo
        """
        api_url = '/api/redeem/redeeming'
        body = {
            "redeemNo": redeemNo
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def api_redeem_getlist(self):
        """
        家长中心-兑换码列表查询
        getlist
        """
        api_url = '/api/redeem/getList'
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp


# if __name__ == '__main__':
#     api = ApiRedeem()
#     api.queryAddTeacherInfo(startTime="1667987509", expireTime="5668073909")
#     api.api_post_redeem_redeeming(redeemNo="YALFgFZDruzPcG")
#     api.api_post_redeem_getlist()
#     api.redeeming()

