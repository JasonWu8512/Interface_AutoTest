"""
=========
Author:Lisa
time:2022/6/21 5:24 下午
=========
"""

from ensurepip import version
# import resp as resp
from paramiko import agent
from business.common.UserProperty import UserProperty
from business.xshare.ApiUser import ApiUser
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiHomeParentCenter(object):
    """
    app  C端：获取家长中心查询
    ParentCenterController
    """

    def __init__(self,token):
        self.host = Domains.config.post('url')
        self.root = '/api/home/parent/center'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version,
            "User-Agent": agent

        }

    def api_home_parent_center(self,token=None):
        """
        菜单查询
        :param bid：宝贝id
        :return:
        """
        api_url = "/api/home/parent/center"
        body = {
            "bid": "a1ef3b0f455a4a3f94f1189dd2dc10e1"

        }
        resp = send_api_request ( url=self.host + api_url, paramType='params', paramData=body, method="post",
                                  headers=self.headers )
        print(resp)
        return resp


# if __name__ == '__main__':
#     dm = Domains ()
#     dm.set_domain ( "https://fat.jiligaga.com" )
#     a = ApiHomeParentCenter ()
#     a.api_home_parent_center ()

