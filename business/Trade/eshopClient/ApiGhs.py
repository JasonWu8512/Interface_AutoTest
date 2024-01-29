# coding=utf-8
# @Time    : 2020/12/3 10:03 上午
# @Author  : jerry
# @File    : ApiGhs.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiGhs:
    """
    eshop规划师、班主任
    """

    def __init__(self, token):
        self.host = Domains.domain
        self.root = '/api/eshop'
        self.headers = {'Authorization': token, "Content-Type": "application/json"}


    def api_get_ghs(self, orderId):
        """
        获取当前订单是否展示规划师
        :param orderId: 订单号
        :return:
        """
        api_url = f"{self.host}{self.root}/ghs/info"
        body = {
            "orderId": orderId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params',
                                headers=self.headers)
        return resp

    def api_post_ghs(self):
        """
        长按规划师二维码更新规划师信息、已弃用，替换为规划师服务接口
        :return:
        """
        api_url = f"{self.host}{self.root}/ghs/info"
        resp = send_api_request(url=api_url, method='post', headers=self.headers)
        return resp

    def api_get_bzr(self, orderId):
        """
        获取当前订单是否展示班主任
        :param orderId: 订单号
        :return:
        """
        api_url = f"{self.host}{self.root}/bzr/info"
        body = {
            "orderId": orderId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params',
                                headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    user = UserProperty(mobile='17621026961')
    redeem = ApiGhs(token=user.basic_auth)
    print(redeem.api_get_ghs(orderId='O50320947340906496'))
