# coding=utf-8
# @Time    : 2022/9/20 3:52 下午
# @Author  : Karen
# @File    : ApiGGRVip.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiGGRVip(object):
    ''' MVP用户领取免费VIP '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_ggraggregation_vip_exist(self,sourceType):
        """ 01）查询是否领取过某类型 VIP """
        api_url = "/api/ggraggregation/vip/exist"
        body = {"sourceType": sourceType}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="json", method="post",
                                headers=self.headers)
        return resp


    def api_ggraggregation_vip_set(self,sourceType,vipType):
        """ 02）领取免费VIP """
        api_url = "/api/ggraggregation/vip/set"
        body = {
            "sourceType": sourceType,
            "vipType": vipType
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="json", method="post",
                                headers=self.headers)
        return resp