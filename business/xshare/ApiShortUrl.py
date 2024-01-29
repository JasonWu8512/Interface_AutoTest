# coding=utf-8 
# @File     :   ApiShortUrl
# @Time     :   2021/2/24 3:29 下午
# @Author   :   austin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiShortUrl(object):

    def __init__(self, token):
        self.root = "/api/xshare/shorturl"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_geturl(self, pid,itemid):
        """
        pid为uid

        """
        header = self.wx_headers.copy()
        header["Content-Type"] = "text/plain"
        api_url = "{}/geturl".format(self.root)
        body = {
            "url":self.host + "/store/share/index.html#/item?itemid="+itemid+"&pid=" + pid + "&initiator=" + pid
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=header)
        return resp

if __name__ == '__main__':
    dm = Domains()
