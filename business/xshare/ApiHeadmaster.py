# coding=utf-8
# @Time    : 2020/9/8 6:38 下午
# @Author  : keith
# @File    : ApiHeadmaster

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiHeadmaster(object):

    def __init__(self, token):
        self.root = "/api/headmaster"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_headmaster_info(self, uid):
        """
        班主任查询接口(/api/xshare/headmaster/info)
        生产能调通，其他环境跑不通
        """
        api_url = "{}/info".format(self.root)
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_headmaster_classinfo(self, uid):
        """
       班主任接口
        """
        header = self.wx_headers.copy()
        header["Content-Type"] = "text/plain"
        api_url = "{}/classinfo".format(self.root)
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, paramType='json',paramData=body ,method="post",
                                headers=header)
        return resp


if __name__ == '__main__':
    dm = Domains()
