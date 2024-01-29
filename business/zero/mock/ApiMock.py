# coding=utf-8
# @Time    : 2020/12/21 2:37 下午
# @Author  : jerry
# @File    : ApiMock.py

from utils.requests.apiRequests import send_api_request

class ApiMock:
    """mock支付"""

    root = "/v1"

    def __init__(self):
        self.host = "http://zero.jlgltech.com"
        self.headers = {"version": "1", "Content-Type": "application/json"}

    def api_update_mock_status(self, status, env, server_list, user_email):
        """
        开关mock：true为开；false为关
        """
        api_url = f'{self.host}{self.root}/mock/status/update'
        body = {
            'env': env,
            'domains': {
                "api.pingxx.com": status
            },
            "server_list": server_list,
            "user_email": user_email
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_refund_mock(self, chargeid):
        """退mock的订单时，不需要调真实的退款接口（也不需要开启mock），只需调mock的退款接口"""
        api_url = f'{self.host}{self.root}/charges/{chargeid}/refunds'
        body = {}
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

if __name__ == '__main__':
    mock = ApiMock()
    # re = mock.api_update_mock_status(status=True, env='dev')
    # re = mock.api_update_mock_status(status=False, env='dev')
    re = mock.api_refund_mock('mockch_nvdoUJQcBazS9v2WCZMQMc')
    print(re)