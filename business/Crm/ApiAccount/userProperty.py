# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 2:38 下午
@Author  : Demon
@File    : userProperty.py
"""

from business.Crm.ApiAccount.ApiUser import ApiUser
from config.env.domains import Domains
from lazy_property import LazyProperty
from business.sso.ApiSso import ApiSso
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UserProperty(object):
    def __init__(self, email_address, pwd):
        self.host = Domains.domain
        self.sso = ApiSso(email_address=email_address, pwd=pwd)
        self.crm_auser = ApiUser()
        self.user_data = self.crm_auser.api_oa_account_login(sso_code=self.sso.sso_code)
        self.cookies = self.user_data.get('cookies')

    @LazyProperty
    def user_info(self):
        return self.user_data.get('user_info')

    @LazyProperty
    def id_token(self):
        return self.user_data.get('id_token')

    @LazyProperty
    def uid(self):
        return self.user_data.get('uid')

    # @LazyProperty
    # def get_cookie(self):
    #     return self.user_data.get('cookies')

    def logout(self):
        self.crm_auser.api_account_logout_sso(self.cookies)

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('fat')
    print(dm.config)
    crm_user = UserProperty(email_address=dm.config.get('xcrm').get('email_address'), pwd=dm.config.get('xcrm').get('pwd'))
    # print(crm_user.get_cookie, crm_user.uid)
    print(crm_user.sso.sso_code, crm_user.uid)