"""
=========
Author:Anna
time:2023/12/25 7:51 下午
=========
"""
import os

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiInternal():
    '''
       内部接口
    '''

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json"
        }
        # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # 本地调试用，环境变量
        # env = 'fat'
        if env == 'fat':
            self.host = 'http://gateway-fat.jlgltech.com'

        elif env == 'rc':
            self.host = 'http://gateway-rc.jlgltech.com'
        else:
            self.host = 'http://gateway.jlgltech.com'

    def api_get_userInfo(self, mobile):
        """
        内部获取用户信息，含验证码
        :param mobile:目标手机号
        :return:
        """
        api_url = f"{self.host}/inner/userCenter/common/findUserDTOByUserExistDTO"
        body = {
            "userDTO": {
                "mobile": mobile
            }
        }
        resp = send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)
        return resp

    def api_get_smsByID(self, id):
        """
        内部获取用户信息，含验证码
        :param id:用户id
        :return:
        """
        api_url = f"{self.host}/inner/userCenter/common/findUserDTOByUserExistDTO"
        body = {
            "userDTO": {
                "id": id
            }
        }
        resp = send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)
        return resp

    def api_get_mobile(self):
        """开发内部接口查询可用手机号"""
        api_url = f"{self.host}/api/qa/fetchTestMobile"
        resp = send_api_request(url=api_url, method="get")
        return resp

    def api_post_refund(self, orderNo):
        """
        mock退款
        @param oid:订单id
        @return:
        """
        api_url = f"{self.host}/api/trade-order/refund"
        body = {
            "orderNo": orderNo
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_post_mock(self, id, time_paid, order_no, transaction_no):
        """
        mock支付
        @param id:付款单
        @param time_paid:支付时间
        @param order_no:订单编号
        @param transaction_no:支付id
        @return:
        """
        api_url = f"{self.host}/api/mock/pingpp/charge/callback"
        body = {
            "type": "charge.succeeded",
            "data": {
                "object": {
                    "id": id,
                    "time_paid": time_paid,
                    "order_no": order_no,
                    "transaction_no": transaction_no
                }
            }
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp


if __name__ == '__main__':
    internal = ApiInternal()
    # 获取验证码
    resp = internal.api_get_userInfo(mobile='15921263812')
    print(resp)

    resp01 = internal.api_get_mobile()
    print(resp01)
