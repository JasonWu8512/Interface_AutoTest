# -*- coding: utf-8 -*-
# @Time : 2023/10/13 下午5:01
# @Author : Saber
# @File : ApiUsertest.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiMarktestaccount():
    """
        app  线上标记测试账户接口

        """

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
        }
        # 设置域名host
        self.dm = Domains()
        self.host = self.dm.set_env_path("fat")["gaga_url"]

    def api_mark_testaccount(self, uids=None, areacode=None, phone=None):
        """
        app  线上标记测试账户接口
        :return:
        """
        root = '/api/inner/app/admin/user/mark/test/account'
        body = {
            "uids": [uids],
            "guaids": [],
            "phones": [{
                "areaCode": areacode,
                "phone": phone
            }]
        }
        resp = send_api_request(url=self.host + root, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    uids = '973a29b5cb1e4f9a8d39b2a2715468df'
    areacode = '886'
    phone = '900000108'
    # 打标签
    resp = ApiMarktestaccount().api_mark_testaccount(uids=uids, areacode=areacode, phone=phone)
    print(resp)
