# -*- coding: utf-8 -*-
# @Time: 2021/4/19 11:11 上午
# @Author: ian.zhou
# @File: RedeemController
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiRedeem:
    """
    eshop 商城管理后台
    """
    root = '/api/admin/eshop/redeem'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_redeem_batch_list(self, pageNo=1, pageSize=10):
        """
        获取兑换码批次列表
        :param page: 页码
        :param pageSize: 每页数量
        :return:
        """

        api_url = f'{self.host}{self.root}/batches'
        body = {
            'page': pageNo,
            'pageSize': pageSize
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_create_redeem(self, sguId, num=1, desc='trade_qa_automation'):
        """
        生成兑换码
        :param sguId: SGU商品id
        :param num: 生成数量
        :param desc: 描述
        :return:
        """

        api_url = f'{self.host}{self.root}/batches'
        body = {
            'sguId': sguId,
            'num': num,
            'desc': desc
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_destroy_redeem(self, redeemNoList, destroyDesc='自动化测试'):
        """
        销毁兑换码
        :param destroyDesc: 销毁原因
        :param redeek_list: 兑换码编号（支持批量，数组形式）
        :return:
        """

        api_url = f'{self.host}{self.root}/batches/destroy'
        body = {
            'destroyDesc': destroyDesc,
            'redeemNoList': redeemNoList
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_redeem_info(self, pageNo=1, pageSize=10, batchId=None, stateList=None, redeemNoList=None):
        """
        获取兑换码信息
        :param pageNo: 页码
        :param pageSize: 每页数量
        :param batchId: 兑换码批次
        :param stateList: 兑换码状态 未使用1 已使用2 销毁3
        :param redeemNoList: 兑换码编号
        :return:
        """

        api_url = f'{self.host}{self.root}/redeems'
        body = {
            'page': pageNo,
            'pageSize': pageSize,
            'batchId': batchId,
            'stateList': stateList,
            'redeemNoList': redeemNoList
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_crm_get_redeem_info(self, redeemNoList):
        """
        获取兑换码信息（供crm调用）
        :param redeemNoList: 兑换码编号（支持多个，列表形式）
        :return:
        """

        api_url = f'{self.host}{self.root}/crm/redeems'
        body = {
            'redeemNoList': redeemNoList
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_redeem_batches_detail(self, batchId):
        """
        获取兑换码批次详情
        """
        api_url = f'{self.host}{self.root}/batches/detail'
        body = {
            'batchId': batchId
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    redeem = ApiRedeem(token='817da0adbb264dffbc290c9f236722aa')
    # print(redeem.api_crm_get_redeem_info(redeemNoList=['qDwLQEEKZEZcAz', '7B6E6ipTRnGyce']))
    print(redeem.api_get_redeem_batches_detail(batchId=97))

