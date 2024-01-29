# coding=utf-8 
# @File     :   ApiUser
# @Time     :   2021/3/7 8:41 下午
# @Author   :   austin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUser(object):

    def __init__(self, token):
        self.root = "/api"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_user_type(self):
        """
        进入钻石商城首页，判断用户身份

        """
        api_url = "{}/xshare/user/type".format(self.root)
        resp = send_api_request(url=self.host + api_url, paramType='json', method="get",
                                headers=self.wx_headers)
        return resp



if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://fat.jiliguala.com")
    token = ''
    print(ApiUser('').api_get_sms('18717877715'))