# coding=utf-8 
# @File     :   ApiOrder
# @Time     :   2021/3/7 8:52 下午
# @Author   :   austin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiOrder(object):

    def __init__(self, token):
        self.root = "/api/xshare/order"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_order_status(self):
        """

        """
        header = self.wx_headers.copy()
        header["Content-Type"] = "text/plain"
        api_url = "{}/status".format(self.root)
        body = {

        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="get",
                                headers=header)
        return resp


if __name__ == '__main__':
    dm = Domains()