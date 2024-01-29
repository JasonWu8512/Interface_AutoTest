# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 2:38 下午
@Author  : Demon
@File    : userProperty.py
"""

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse


class ApiUserInfo(object):
    def __init__(self, cookies):
        # 请求头文件
        self.headers = header
        self.host = Domains.config.get('crm_number_url')
        self.root = '/api/account'
        self.cookies = cookies

    def api_get_account_detail(self):
        api_url = parse.urljoin(self.host, f"{self.root}/get_account_detail")
        body = {
            "account_identity": '3c2d5cf15e1d467b93b2fb565c6d9566'
        }
        resp = send_api_request(url=api_url, paramData=body, paramType='json', method="post",
                                headers=self.headers, cookies=self.cookies)
        return resp

    def api_get_account_allowed_subject_types(self, ):
        """
         获取当前登录用户科目权限列表
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_account_allowed_subject_types")
        body = {}
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    # def api_account_logout_sso(self):
    #     """退出登录"""
    #     api_url = parse.urljoin(self.host, f"{self.root}/logout_sso")
    #     return send_api_request(url=api_url, paramType='json', paramData={}, cookies=self.cookies, method='post')


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('dev')
    from business.Crm.ApiAccount.userProperty import UserProperty
    crm_user = UserProperty(email_address=dm.config.get('xcrm').get('email_address'), pwd=dm.config.get('xcrm').get('pwd'))
    aui = ApiUserInfo(cookies=crm_user.cookies)
    print(aui.api_get_account_allowed_subject_types())
