# coding=utf-8
# @Time    : 2021/02/09 6:33 下午
# @Author  : qilijun
# @File    : ApiDiamond
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiDiamond:
    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.config.get("url")
        self.root = "/api/xshare/diamond"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def api_get_status(self):
        api_url = "{}/status".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    def api_get_config(self,type=None):
        api_url = "{}/config".format(self.root)
        print(api_url)
        body = {
            "type": type
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params", paramData=body,
                                headers=self.headers)
        return resp

    def api_get_sharePosterCheck(self):
        api_url = "{}/sharePosterCheck".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp


    def api_get_Diamond_user(self):
        api_url = "/api/diamond/user"
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp
    def api_diamond_user_invitees(self,pageSize=1000):
        api_url = "/api/diamond/user/invitees"
        body = {
            "page": 0,"pageSize":pageSize
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params", paramData=body,
                                headers=self.headers)
        return resp

    def api_diamond_user_orders(self,pageSize=1000):
        api_url = "/api/diamond/user/orders"
        body = {
            "page": 0,"pageSize":pageSize
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params", paramData=body,
                                headers=self.headers)
        return resp

if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path("fat")
    up = UserProperty("18900000725")
    auth_token = up.basic_auth
    # wechat_token = up.encryptWechatToken_pingpp
    diamond = ApiDiamond(auth_token)
    # result = diamond.api_get_config(type="small")
    result = diamond.api_get_sharePosterCheck()
    # result = diamond.api_diamond_user_invitees()
    # result = diamond.api_diamond_user_orders()
    print(result)
