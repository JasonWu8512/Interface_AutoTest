# -*- coding: utf-8 -*-
# @Time : 2021/5/31 11:40 上午
# @Author : Anna
# @File : ApiPermission.py
from business.common.UserProperty import UserProperty
# from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPermission():
    """
    购买资格查询[非游客账号有权限]
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token,
            "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_permission(self, buyType):
        """
        购买资格查询
        :param buyType:购买类型
        :return:
        """
        api_url = f"{self.host}/api/buy/permisson"
        body = {
            "buyType": buyType
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19393123455")
    token = user.basic_auth
    version = config['version']['ver11.0']

    permission = ApiPermission(token, version)
    resp = permission.api_get_permission("c_type_h5")
    print(resp)
