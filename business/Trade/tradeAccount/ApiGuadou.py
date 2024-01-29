# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 11:26 上午
# @Author  : 万军
# @File    : ApiGuadou.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGuadou:
    """
    Trade-Account-呱豆账户
    """
    root = '/api/trade/account/admin'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_account_list(self, account_type, search=None, page=1, page_size=20):
        """
        呱豆账户列表
        :param account_type: 呱豆类型
        :param search: 搜索关键字
        :param page: 当前页数
        :param page_size:  每页数据量
        :return:
        """

        api_url = f'{self.host}{self.root}/account/list/{account_type}'
        body = {
            'accountType': account_type,
            'search': search,
            'pageSize': page_size,
            'page': page

        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_account_detail_list(self, account_type, user_no, balance_type=None, operate_type=None,
                                start_create_time=None, end_create_time=None, page=1, page_size=20):
        """
        呱豆账户明细
        :param account_type: 呱豆类型
        :param user_no: 搜索关键字
        :param balance_type: 账户类型：余额类型
        :param operate_type: 操作类型
        :param start_create_time: 开始:创建时间:yyyy-MM-dd
        :param end_create_time: 结束:创建时间:yyyy-MM-dd
        :param page: 当前页数
        :param page_size: 每页数据量
        :return:
        """

        api_url = f'{self.host}{self.root}/account/detail/{account_type}/{user_no}'
        body = {
            'accountType': account_type,
            'userNo': user_no,
            'balanceType': balance_type,
            'operateType': operate_type,
            'startCreateTime': start_create_time,
            'endCreateTime': end_create_time,
            'page_size': page_size,
            'page': page

        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_manual_adjust_type(self, account_type, operate_type=None):
        """
        获取调整类型
        :param account_type: 呱豆类型
        :param operate_type: 调整类型,枚举是ADD、SUB
        :return:
        """

        api_url = f'{self.host}{self.root}/manualAdjustType/{account_type}/{operate_type}'
        body = {
            'accountType': account_type,
            'operateType': operate_type
        }
        resp = send_api_request(method='get', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_manual_adjust_account(self, account_type, user_no, operate_type=None,
                                  adjust_type=None, adjust_amount=None, remark=None):
        """
        手动调整呱豆账户
        :param account_type: 呱豆类型
        :param user_no: 搜索关键字
        :param remark: 备注
        :param operate_type: 操作类型
        :param adjust_type: 调整类型，ADD、SUB
        :param adjust_amount: 调整金额,分为单位
        :return:
        """

        api_url = f'{self.host}{self.root}/manualAdjustAccount'
        body = {
            'accountType': account_type,
            'userNo': user_no,
            'remark': remark,
            'operateType': operate_type,
            'adjustType': adjust_type,
            'adjustAmount': adjust_amount

        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    guadou_admin = ApiGuadou('54fd3f61bb344457a12b71a02c3208bd')
    print(guadou_admin.api_account_list(account_type='GUADOU', search='15921992382'))
    # print(guadou_admin.api_manual_adjust_type(account_type='GUADOU', operate_type='ADD'))
    # print(guadou_admin.api_manual_adjust_account(account_type='GUADOU', user_no='1cb55671e35d44568ea0b15028eca4ee',
    #                                              operate_type='SUB', adjust_type='OTHER_SUB', adjust_amount='1200'))
    # print(guadou_admin.api_account_detail_list(account_type='GUADOU', user_no='01dd9a50cdbb4faea73d8fd710f6b7ec',
    #                                            balance_type='FREEZE',operate_type='SUB'))





