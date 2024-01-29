#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> ApiLogOut
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/4/26 3:49 下午
@Desc   ：
=================================================="""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiLogOut:
    """LogOutController"""
    root = "/api/promoter"

    def __init__(self, wechat_token=None, basic_auth=None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    def api_log_out(self):
        """退出推广人账号"""
        api_url = f'{self.host}{self.root}/logout'
        resp = send_api_request(url=api_url, method='post',headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    dm.set_domain("https://fat.jiliguala.com")
    promo = UserProperty("15601706236")
    wechattoken = promo.encryptWechatToken_promoter
    basic = promo.basic_auth
    promoter = ApiLogOut(wechattoken, basic)
    res = promoter.api_log_out()
    print(res)