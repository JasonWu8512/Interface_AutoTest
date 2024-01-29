# coding=utf-8
# @Time    :
# @Author  : anna
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.businessQuery import usersQuery


class ApiPing(object):
    def __init__(self, token=None):
        self.host = Domains.config.get('url')
        self.headers = {"authorization": token, "Content-Type": "application/json"}

    def api_post_ping(self):
        """心跳监测"""
        api_url = f"{self.host}/api/user/ping"
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json")
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("fat")
    ping = ApiPing()
    resp = ping.api_post_ping()
    print(resp)
