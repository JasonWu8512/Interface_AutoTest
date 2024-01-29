#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> ApiSsoPortrait.py
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/2/4 1:30 下午
@Desc   ：
=================================================="""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSso:
    root = "/api/sso"

    def __init__(self, email_address, pwd):
        self.host = Domains.config.get('sso_url')
        print(self.host)
        self.headers = {"version": "1", "Content-Type": "application/json"}
        self.email_address = email_address
        self.pwd = pwd

    def api_login_by_email(self, email_address, pwd):
        """邮箱登陆"""
        api_url = f"{self.host}{self.root}/login_by_email"
        body = {
            "email_address": email_address,
            "pwd": pwd
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post", headers=self.headers)
        return resp

    def api_authorize(self, cookies):
        """鉴权"""
        api_url = f"{self.host}{self.root}/authorize"
        body = {

        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post", headers=self.headers,
                                cookies=cookies)
        return resp

    @property
    def sso_code(self):
        cookies = self.api_login_by_email(email_address=self.email_address, pwd=self.pwd).get('cookies')
        return self.api_authorize(cookies).get('data').get('sso_auth_code')

if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path("dev")
    sso = ApiSso(email_address=config['sso']['email_address'], pwd=config['sso']['pwd'])
    print(config["sso"])

    print(sso.sso_code)
