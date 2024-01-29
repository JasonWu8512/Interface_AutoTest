# -*- coding: utf-8 -*-
# @Time    : 2021/6/4 15:26 下午
# @Author  : 万军
# @File    : ApiDbInner.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiDbInner:
    """
    ios_ver修改内部接口
    """
    root = '/api/db/inner'

    def __init__(self, token):
        self.headers = {'Authorization': token}
        self.host = Domains.domain

    def api_ios_cer_get(self):
        """
        查询ios_ver
        :return:
        """

        api_url = f'{self.host}{self.root}/ios_ver'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_ios_cer_put(self, value):
        """
        修改ios_ver
        :param value: 值
        :return:
        """

        api_url = f'{self.host}{self.root}/ios_ver'
        body = {
            'value': value

        }
        resp = send_api_request(method='put', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    Db_inner = ApiDbInner('Basic YTU2YjA2YTg3NmYzNDEyOWE2MjgxZjczNTY0ZjNlZWQ6MmM4NDc1YjZkMjNmNGFlM2E5YjhlNTFhNTc0YjEzOWU=')
    # print(Db_inner.api_ios_cer_get())
    print(Db_inner.api_ios_cer_put(value='ios_ver'))





