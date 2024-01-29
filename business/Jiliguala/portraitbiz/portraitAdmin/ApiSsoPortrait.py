# -*- coding: utf-8 -*-
# @Time : 2021/3/2 6:02 下午
# @Author : Cassie
# @File : ApiSsoPortrait.py
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.sso.ApiSso import ApiSso


class ApiSsoPortrait():
    """
    资源位管理后台：登录相关接口
    """
    root = '/api/portraitbiz/sso'

    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.host = Domains.config.get('url')

    def api_get_token(self, code):
        """
        获取登录态
        :param code: sso服务返回的token
        :return: 将sso_token进行JWT加密后返回idToken
        """
        api_url = f'{self.host}{self.root}/token'
        body = {
                "code":code
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers).get("data").get("idToken")
        return resp

    def api_logout(self, token):
        """
        退出登录
        :return:
        """
        api_url = f'{self.host}{self.root}/logout'
        headers = {
            "authorization": f"Basic {token}", "Content-Type": "application/json"
        }
        body = {
        }
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("dev")
    # dm.set_domain("http://dev.jiliguala.com")
    sso = ApiSso(email_address=config['sso']['email_address'], pwd=config['sso']['pwd']).sso_code
    print(f'sso 服务返回的token:{sso}')
    token = ApiSsoPortrait().api_get_token(sso)
    print(f'资源位服务生成的toen:{token}')
    resp=ApiSsoPortrait().api_logout(token)
    print(resp)
