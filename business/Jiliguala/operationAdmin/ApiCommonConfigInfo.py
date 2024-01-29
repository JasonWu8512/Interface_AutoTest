# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 2:00 下午
# @Author  : zoey
# @File    : ApiCommonConfig.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCommonConfigInfo:
    """
    购买页配置后台
    """
    root = '/api/admin/common'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    """-------------------------------------commonConfigController--------------------------------"""
    def api_get_all_config(self, pageNo=1, pageSize=20):
        """
        获取投放计划列表
        :return:
        """
        api_url = f'{self.host}{self.root}/config/all'
        body = {
            "pageNo": pageNo,
            "pageSize": pageSize
        }
        resp = send_api_request(url=api_url, method='get',
                                paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_get_config_detail(self, id, channel, lv):
        """
        获取投放计划配置(外部，判断有效时间/有效性)
        :param id: 必填 投放计划id
        :param channel: 必填 投放计划渠道
        :param lv:
        :return:
        """
        api_url = f'{self.host}{self.root}/config'
        body = {
            "id": id,
            "channel": channel,
            "lv": lv
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_get_inner_config_detail(self, id, channel=None, lv=None):
        """
        获取投放计划配置(内部，不判断有效时间/有效性)
        :param id: 必填 投放计划id
        :param channel: 非必填 投放计划渠道
        :param lv:
        :return:
        """
        api_url = f'{self.host}{self.root}/inner/config'
        body = {
            "id": id,
            "channel": channel,
            "lv": lv
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_edit_config(self, id=None, title='', creator='', status=False, comment='', skudetail=[], configDetails=[], payload={}):
        """
        修改配置
        :param id:
        :param title:
        :param creator:
        :param status:
        :param comment:
        :return:
        """
        api_url = f"{self.host}{self.root}/config"
        if payload:
            body = payload
        else:
            body = {
                "id": id,
                "title": title,
                "creator": creator,
                "status": status,
                "comment": comment,
                "skuDetail": skudetail,
                "configDetails": configDetails
            }
        resp = send_api_request(url=api_url, method="post", paramData=body, paramType="json", headers=self.headers)
        return resp

    def api_edit_config_status(self, id, status, channel=None):
        """
        修改投放计划有效性。
        :param id: 必填 投放计划id
        :param channel: 非必填 投放计划渠道
        param status: 必填 投放计划有效性
        """
        api_url = f"{self.host}{self.root}/config/status"
        body = {
            "id": id,
            "status": status,
            "channel": channel
        }
        resp = send_api_request(url=api_url, method="post", paramData=body, paramType="json", headers=self.headers)
        return resp

    def api_get_config_channel_status(self, id):
        """
        获取单个投放计划各个渠道有效性
        param id: 必填 投放计划id
        """
        api_url = f"{self.host}{self.root}/config/channel/status"
        body = {
            "id": id
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp


    """-----------------------------------commonInfoController-----------------------------------"""
    def api_get_ghs_list(self):
        """
        获取规划师列表
        :return:
        """
        api_url = f"{self.host}{self.root}/ghs"
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp



if __name__ == '__main__':
    Domains.set_domain('https://dev.jiliguala.com')
    conf = ApiCommonConfigInfo('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c3IiOiIwZTg2YWNiY2EyODk0YTMxYTY1OGUyMjhmZmI0MDA1YSIsImV4cCI6MTYwMjI5NzU3OH0.IUwfRezMaTbNCwaoxtjL8mAkxUhy833F47wWOHC-3lePbLYANQAfoqGqqScIh0hKB_wXaH2MrgSTnFj7G2zIckhYye6RyG9zaa0gbZS1tAsFZ4X8B51DcRtmPnnzK1itSZQI70OQJeKzuFpG43Bf1mP9_gDs25e12Wvq1WT0pOY-ggg7tVzCO3X7Ox40MAL02NEuuubIo8n7vyL0qKDUTFj_Vwp3ZhrIDF6UHVKwBME1A2VHaNHdQXihAQNn2xoTVPORuKAirLgw_SL8OP44Xo74chb0aKB7mPdGhqlKG4e-vtUFZi16wDqkw9GNFhMRGS6ZO_x8anMAmjATVCYHFw')
    # conf.api_get_all_config()
    # conf.api_get_all_config()
    res = conf.api_get_inner_config_detail(id='28')
    print(res)
    # conf.api_get_config_detail(id='24', channel="wechat_mini_group", lv='')



