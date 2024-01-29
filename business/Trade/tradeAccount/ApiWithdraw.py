# -*- coding: utf-8 -*-
# @Time    : 2021/4/19 11:26 上午
# @Author  : 万军
# @File    : ApiWithdraw.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiWithdraw:
    """
    提现api接口汇总
    """
    root = '/api/trade/account/withdraw'

    def __init__(self, token):
        self.headers = {'Authorization': token}
        self.host = Domains.domain

    def api_render(self, account_business_group):
        """
        提现页面渲染接口
        :param account_business_group: 账户业务组,一个用户在一个业务组只能拥有一个账号
        :return:
        """

        api_url = f'{self.host}{self.root}/render/{account_business_group}'
        body = {
            'accountBusinessGroup': account_business_group
        }
        resp = send_api_request(method='get', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_user_withdraw_list_by_account_business_group(self, account_business_group, page):
        """
        根据业务类型查询对应的提现信息列表
        :param account_business_group: 账户业务组,一个用户在一个业务组只能拥有一个账号
        :param page 页数
        :return:
        """

        api_url = f'{self.host}{self.root}/getUserWithdrawListByAccountBusinessGroup/{account_business_group}/{page}'
        body = {
            'accountBusinessGroup': account_business_group,
            'page': page
        }
        resp = send_api_request(method='get', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_get_user_withdraw_by_withdraw_no(self, withdraw_no):
        """
        根据提现单号获取提现信息
        :return:
        """

        api_url = f'{self.host}{self.root}/getUserWithdrawByWithdrawNo/{withdraw_no}'
        body = {
            'withdrawNo': withdraw_no
        }
        resp = send_api_request(method='get', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_apply(self, account_business_group_enum, apply_amount, apply_type, msg_code):
        """
        申请提现
        :param account_business_group_enum: 账户业务组,一个用户在一个业务组只能拥有一个账号
        :param apply_amount: 申请金额
        :param apply_type: 类型:WECHAT:微信提现,BANK:银行卡提现
        :param msg_code: 验证码
        :return:
        """

        api_url = f'{self.host}{self.root}/apply'
        body = {
            'AccountBusinessGroupEnum': account_business_group_enum,
            'applyAmount': apply_amount,
            'applyType': apply_type,
            'msgCode': msg_code
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    withdraw = ApiWithdraw('Basic YTU2YjA2YTg3NmYzNDEyOWE2MjgxZjczNTY0ZjNlZWQ6MmM4NDc1YjZkMjNmNGFlM2E5YjhlNTFhNTc0YjEzOWU=')
    print(withdraw.api_get_user_withdraw_by_withdraw_no(withdraw_no='W0000000000071'))
    print(withdraw.api_get_user_withdraw_list_by_account_business_group(account_business_group='PROMOTER', page=1))
    print(withdraw.api_apply(account_business_group_enum='PROMOTER', apply_amount=100, apply_type='BANK', msg_code=1000))



