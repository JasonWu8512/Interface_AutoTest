# -*- coding: utf-8 -*-
# @Time : 2021/6/3 13:30 下午
# @Author : nana
# @File : ApiUserAccount.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiUserAccount():
    """
    家长中心-账号管理
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/user/account'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_user_account(self):
        """
        无入参
        :return:
        """
        api_url = f"{self.host}{self.root}"
        body = {
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("13242040693")
    token = user.basic_auth
    version = config['version']['ver11.6']
    useraccount = ApiUserAccount(token, version)

    # /api/user/account
    resp = useraccount.api_get_user_account()
    print(resp)
