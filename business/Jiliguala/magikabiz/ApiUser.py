# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/8/4 3:09 下午
@Author   : Anna
@File     : ApiUser.py
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiStoreUser():
    """
    魔石商城
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/magika'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_trans(self, page, tab):
        """
        魔石明细页面
        :param page:页码
        :param tab:类型
        :return：
        """
        api_url = f"{self.host}{self.root}/user/trans"
        body = {
            "page": page,
            "tab": tab
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19393123455")
    token = user.basic_auth
    version = config['version']['ver11.6']
    user = ApiStoreUser(token, version)

    # 调用魔石商城明细页
    resp01 = user.api_get_trans("0", "in")
    print(resp01)
