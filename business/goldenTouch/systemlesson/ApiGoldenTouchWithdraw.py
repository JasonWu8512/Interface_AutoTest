# coding=utf-8
# @Time    : 2022/7/15 6:34 下午
# @Author  : Karen
# @File    : ApiGoldenTouchWithdraw.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiGoldenTouchWithdraw(object):

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_goldentouch_withdraw(self):
        """ 01）发起提现 """
        api_url = "/api/goldentouch/withdraw"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json',method="post", headers=self.headers)
        return resp


    def api_goldentouch_queryWithdrawDetail(self,uid):
        """ 02）查询提现明细 """
        api_url = "/api/goldentouch/queryWithdrawDetail"
        body = {
            "uid":uid
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="params", method="get",
                                headers=self.headers)
        return resp