# coding=utf-8
# @Time    : 2021/04/04 6:33 下午
# @Author  : qilijun
# @File    : ApiManagementSystem
# @Software: PyCharm
import base64

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiManagementSystem:
    """"
    钻上商城后端接口封装
    """
    def __init__(self, auth_token=None):
        self.host = Domains.config.get("admin_url")

        self.root = "/api/zeus"
        self.headers = {"version": "1", "Content-Type": "application/json", "X-APP-ID": "5fb4d4064d03357897115df3",
                        "Authorization": auth_token}

    def api_login(self, username, password):
        """"
        登录接口，获取用户token，用于生成Auth
        """
        api_url = "/api/login"
        body = {
            "username": username,
            "password": password
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body, headers=self.headers)
        return resp

    def api_get_auth(self, username, password):
        """"
        生成用户Auth并返回
        """
        login_res = self.api_login(username, password)
        user_tok = login_res["data"]["token"]
        return 'JWT ' + str(user_tok)

    def api_diamond_batch(self,pointNum,Title,uidList):
        api_url = "{}/xshare/diamond/batch".format(self.root)
        body = {
            "point": pointNum,
            "title": Title,
            "typprinte": "uid",
            "idList": uidList
        }

        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body, headers=self.headers)
        return resp
    def api_get_user_diamond(self,uid):
        api_url = "{}/user/{}/diamond/total".format(self.root, uid)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp




if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path("dev")
    user = ApiManagementSystem()
    auth_token = user.api_get_auth(config['xshare']['manage']['user'], config['xshare']['manage']['password'])
    manage = ApiManagementSystem(auth_token=auth_token)
    result = manage.api_diamond_batch(100, "自动化测试",  ["44aef649a6594f9e9845907a1b981bd8","64532f8fdb084b47b4b99ddcab050553","9cdb239d1459463598641aa417686e30"])
    # result = manage.api_get_user_diamond("44aef649a6594f9e9845907a1b981bd8")

    print(result)



