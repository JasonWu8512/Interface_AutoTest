# coding=utf-8 
# @File     :   ApiTiktok
# @Time     :   2021/3/22 3:18 下午
# @Author   :   austin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiWechatUserInfo(object):

    def __init__(self, token):
        self.root = "/api/xshare/wechatUserInfo"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_getUserInfoByUid(self,uid):
        """
        微信用户信息
        """
        api_url = "{}/getUserInfoByUid".format(self.root)
        body = {
            "uid":uid
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp


if __name__ == '__main__':
    dm = Domains()