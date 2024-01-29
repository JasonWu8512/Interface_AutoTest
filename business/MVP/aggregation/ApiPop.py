# coding=utf-8
# @Time    : 2022/9/20 4:02 下午
# @Author  : Karen
# @File    : ApiPop.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiPop(object):
    ''' MVP用户领取免费VIP弹窗 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_ggraggregation_pop(self,popUpsSource):
        """ 01）领取免费VIP弹窗 """
        api_url = "/api/ggraggregation/pop/get"
        body = {"popUpsSource": popUpsSource}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="json", method="post",
                                headers=self.headers)
        return resp