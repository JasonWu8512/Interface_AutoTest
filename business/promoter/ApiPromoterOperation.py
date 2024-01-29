#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：tiga -> ApiGroup
@IDE    ：PyCharm
@Author ：qinjunda
@Date   ：2021/4/26 4:19 下午
@Desc   ：
=================================================="""
from utils.requests.apiRequests import send_api_request

class ApiPromoterOperation:
    """PromoterOperationController"""
    root = "/api/promoter/tags"

    def __init__(self, url=None):
        self.url=url

    def api_update_tags(self,promoter_id,tags):
        """添加标签"""
        api_url = f'{self.url}{self.root}/update'
        tags_json=[]
        tags_json.append(tags)
        body = {
            "promoterId": promoter_id,
            "tags":
                tags_json
        }
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=None)
        return resp


    def api_find_tags(self,promoter_id):
        """查询标签"""
        api_url = f'{self.url}{self.root}/find'
        body = {
            "promoterId": promoter_id
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=None)
        return resp


if __name__ == '__main__':

    promoter = ApiPromoterOperation("http://10.100.128.43:50025")
    list=["地推","old"]
    #res = promoter.api_update_tags("JLGL_TEST_WYW1",tags=list)
    res = promoter.api_find_tags("JLGL_TEST_WYW1")
    print(res)