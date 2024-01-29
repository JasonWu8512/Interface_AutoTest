#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> ApiGroupPurchase
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/4/26 2:43 下午
@Desc   ：
=================================================="""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGroupPurchase:
    """GroupPurchaseController"""
    root = "/api/promoter/group"

    def __init__(self, wechat_token=None, basic_auth=None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    def api_group_purchase_list(self,status):
        """获取拼团信息"""
        api_url = f'{self.host}{self.root}/purchase/list'
        body = {
            "status": status
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    dm.set_domain("https://fat.jiliguala.com")
    promo = UserProperty("15601706236")
    wechattoken = promo.encryptWechatToken_promoter
    basic = promo.basic_auth
    promoter = ApiGroupPurchase(wechattoken, basic)
    res = promoter.api_group_purchase_list(0)
    print(res)