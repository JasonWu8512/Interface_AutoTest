# -*- coding: utf-8 -*-
# @Time : 2021/5/27 5:18 下午
# @Author : Cassie
# @File : ApiUserBiz.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUserBiz():
    """
    userbiz  C端：家长中心相关接口
    UserbizController
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/user'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_auth(self):
        """
        ai用内网用户鉴权接口
        :return:
        """
        api_url = f"{self.host}{self.root}/auth"
        body = {

        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("15958112857")
    token = user.basic_auth
    version = config['version']['ver15.0']
    userBiz = ApiUserBiz(token,version)
    resp = userBiz.api_get_auth()
    print(resp)
