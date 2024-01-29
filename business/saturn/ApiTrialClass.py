#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> ApiTrialClass.py
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/2/5 1:59 下午
@Desc   ：
=================================================="""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTrialClass:
    """TrialClassController"""

    root = "/api/saturn/channel/admin/trial"

    def __init__(self, admintoken):
        self.host = Domains.get_ggr_host()
        self.login_headers = {"version": "1", "Content-Type": "application/json"}
        self.headers = {"admintoken": admintoken, "version": "1", "Content-Type": "application/json"}

    def api_trial_open(self,mobile):
        """开体验课"""
        api_url = f"{self.host}{self.root}/open"
        body = {
            "mobile": mobile
        }
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_trial_inventory_info(self):
        """查询体验课库存"""
        api_url = f"{self.host}{self.root}/inventory/info"
        body = {

        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_trial_open_list(self, mobile, pageNo, pageSize):
        """体验课列表"""
        api_url = f"{self.host}{self.root}/open/list"
        body = {
            "mobile": mobile,
            "pageNo": pageNo,
            "pageSize": pageSize
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp


if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    trial = ApiTrialClass(admintoken="cc5b8f6a562440339bcc237578520b77")
    re = trial.api_trial_open(mobile='17361900610')
    print(re)
