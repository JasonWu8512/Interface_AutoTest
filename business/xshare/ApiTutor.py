# coding=utf-8
# @Time    : 2021/03/16
# @Author  : qilijun
# @File    : ApiTutor.py
# @Software: PyCharm
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTutor:
    """"
    转介绍班主任（扩科）相关-api
    """
    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.domain
        self.root = "/api/xshare/tutor/info"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def get_tutor_info(self):
        """"
        班主任查询接口
        """
        api_url = self.root
        resp = send_api_request(url=self.host+api_url,method="get",headers=self.headers)
        return resp

if __name__ == "__main__":
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    up = UserProperty("18900000773")
    auth_token = up.basic_auth
    tutor = ApiTutor(auth_token=auth_token)
    result = tutor.get_tutor_info()
    print(result)