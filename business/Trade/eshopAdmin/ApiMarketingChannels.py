#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/3 10:20 上午
# @Author : liang_li
# @Site : 
# @File : ApiMarketingChannels.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiMarketingChannels:
    """
    渠道管理
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_marketing_channel(self, pageSize=50, pageNo=1, parentId=0):
        """
        根据parentId查询渠道
        :param pageNo: 页面编号
        :param pageSize: 一页展示的商品数量
        :param parentId: 父级渠道id
        """
        api_url = f'{self.host}{self.root}/marketing-channels'
        body = {
            "pageSize": pageSize,
            "pageNo": pageNo,
            "parentId": parentId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_create_marketing_channel(self, channelNo, name, parentId, remark=None):
        """
        根据parentId查询渠道
        :param channelNo: 渠道参数
        :param name: 渠道名
        :param parentId: 父级渠道id
        :param parentId: 备注
        """
        api_url = f'{self.host}{self.root}/marketing-channels'
        body = {
            "channelNo": channelNo,
            "name": name,
            "parentId": parentId,
            "remark": remark
        }
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    channel = ApiMarketingChannels(token='23a80fbb23e04a3e89a731c3af35431e')
    print(channel.api_create_marketing_channel(channelNo='zhuzhou1', name='株洲天元区', parentId=12))
    print(channel.api_get_marketing_channel(parentId=7))