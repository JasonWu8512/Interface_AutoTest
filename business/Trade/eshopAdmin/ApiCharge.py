# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:19 上午
# @Author  : zoey
# @File    : ApiCharge.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCommodity:
    """
    eshop 商城管理后台
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain


    def api_get_qiniu_img_token(self, mediaType='png'):
        """
        获取七牛图片上传图片凭证
        :param mediaType: 上传图片类型
        :return:
        """

        api_url = f'{self.host}{self.root}/media/token/qiniu'
        body = {
            'type': mediaType
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp


    def api_get_hb_fq_strategy(self, pageNo=1, pageSize=20):
        """
        获取花呗分期策略列表
        :param pageNo: 当前页数
        :param pageNo: 每页数据量
        :return:
        """

        api_url = f'{self.host}{self.root}/hb-fq-strategies'
        body = {
            'pageNo': pageNo,
            'pageSize': pageSize
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_get_app_payments(self):
        """
        获取APP商品分期方式
        :param pageNo: 当前页数
        :param pageNo: 每页数据量
        :return:
        """

        api_url = f'{self.host}{self.root}/payments'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp
