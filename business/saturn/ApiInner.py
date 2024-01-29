#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> ApiInner
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/3/23 2:19 下午
@Desc   ：
=================================================="""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiInner:
    """InnerController"""

    root = "/inner/saturn/relation"

    def __init__(self, token=None, authorization=None):
        self.host = Domains.config.get('saturn_gateway')
        self.login_headers = {"version": "1", "Content-Type": "application/json"}
        self.headers = {"admintoken": token, "version": "1", "Content-Type": "application/json","Authorization": authorization}

    def api_fan_query(self, uid):
        """判断是否已被下沉锁粉"""
        api_url = f"{self.host}{self.root}/channel/fan/query"
        body = {
            "uid": uid,
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.login_headers)
        return resp


if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path("dev")
    channel = ApiInner(token="a5d596e595ce4473b1836ebaa08f0289")
    re = channel.api_fan_query(uid='8f01cfa5f5134b9abc77367814e882e1')
    print(re)
