# coding=utf-8 
# @File     :   ApiReservation
# @Time     :   2021/3/23 2:46 下午
# @Author   :   austin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiReservation(object):

    def __init__(self, token):
        self.root = "/api/xshare/reservation"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_reservation_event(self,additionalProp):
        """
        生成表单预约事件
        """
        api_url = "{}/event".format(self.root)
        body = {
            "queryParams":{
                "additionalProp": additionalProp
            }
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp


if __name__ == '__main__':
    dm = Domains()