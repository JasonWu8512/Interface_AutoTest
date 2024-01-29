# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiSendVip(object):
    """
    赠送vip
    """
    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def api_send_vip(self, uid):
        """
        send vip
        """
        api_url = "/api/circulars/sendvip"
        body = {"typ": "_id", "duration": "7", "id": [uid]}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp


if __name__ == '__main__':

    dm = Domains()
    dm.set_env_path('fat')
    #admin后台登录
    # dm.set_domain("http://fat.jiliguala.com")
    # user = ApiUser()
    # token = user.get_token(typ="email", u='18621149482', p='qqqqqq')

    mobile = '18621149482'
    user = UserProperty(mobile)
    token = user.basic_auth

    print(token)
    dm.set_domain("https://fatggr.jiliguala.com")
    send_vip = ApiSendVip(token=token)
    res = send_vip.api_send_vip("1bb72162f2d949b78aad4e3164a219dd")
    print(res)
