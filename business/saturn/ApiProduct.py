#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> ApiProduct.py
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/2/5 1:59 下午
@Desc   ：
=================================================="""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiProduct:
    """ProductController"""

    root = "/api/saturn/channel"

    def __init__(self, token=None, authorization=None):
        self.host = Domains.get_ggr_host()
        self.login_headers = {"version": "1", "Content-Type": "application/json"}
        self.headers = {"admintoken": token, "version": "1", "Content-Type": "application/json","Authorization": authorization}

    def api_product_list(self, pageNo=1, pageSize=20):
        """商品列表"""
        api_url = f"{self.host}{self.root}/product/list"
        body = {
            "pageNo": pageNo,
            "pageSize": pageSize

        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp


if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    product = ApiProduct(authorization="Basic MDZkYjJlYTM2YTEyNDlkMTg3YTZmZjMzYjk2YTliMjQ6NDA3NTU5YTI0Y2FlNDZiZGEwNzBlNGNkM2E5N2M5ZmM=")
    re = product.api_product_list(pageNo=1, pageSize=20)
    print(re)
