# -*- coding: utf-8 -*-
# @Time    : 2021/4/19 11:26 上午
# @Author  : 万军
# @File    : ApiWithdraw.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTradeUser:
    """
    Trade-Account-用户相关接口
    """
    root = '/api/trade/account/user'

    def __init__(self, token):
        self.headers = {'Authorization': token}
        self.host = Domains.domain

    def api_bank_bind(self, user_name, bank_no, bank_name):
        """
        银行卡绑定
        :param user_name: 开户名字
        :param bank_no: 银行卡号
        :param bank_name: 银行名
        :return:
        """

        api_url = f'{self.host}{self.root}/bank/bind'
        body = {
            'userName': user_name,
            'bankNo': bank_no,
            'bankName': bank_name
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_bank(self):
        """
        获取当前有效银行卡信息
        :return:
        """

        api_url = f'{self.host}{self.root}/getBank'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_user_card_bind(self, type, use_name, card_no):
        """
        身份信息绑定
        :param type: 卡类型
        :param use_name: 姓名
        :param card_no: 证件卡号
        :return:
        """

        api_url = f'{self.host}{self.root}/userCard/bind'
        body = {
            'type': type,
            'userName': use_name,
            'cardNo': card_no
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_user_card(self):
        """
        获取当前有效身份信息
        :return:
        """

        api_url = f'{self.host}{self.root}/getUserCard'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_get_user_card_type_list(self):
        """
        获取用户身份类型列表
        :return:
        """

        api_url = f'{self.host}{self.root}/getUserCardTypeList'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_check_and_get_bank_name(self, bank_no):
        """
        检查并且获取银行名
        :param bank_no: 银行卡号
        :return:
        """

        api_url = f'{self.host}{self.root}/checkAndGetBankName'
        body = {
            'bankNo': bank_no
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    trade_user = ApiTradeUser('Basic YTU2YjA2YTg3NmYzNDEyOWE2MjgxZjczNTY0ZjNlZWQ6MmM4NDc1YjZkMjNmNGFlM2E5YjhlNTFhNTc0YjEzOWU=')
    print(trade_user.api_get_user_card_type_list())
    print(trade_user.api_check_and_get_bank_name(bank_no='6217920124814158'))




