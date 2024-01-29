"""
=========
Author:Lisa
time:2022/7/11 11:36 上午
=========
"""
import self as self

from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTradeRedeemRedeeming():
    """
    通过兑换码兑换会员时间
    ApiTradeRedeemRedeeming
    """

    def __init__(self, authorization):
        self.host = Domains.get_gaga_host()
        self.root='/api/trade/redeem'
        self.header={
            "authorization": "Basic ZmM4ODgyYjVmYTY3NGU4MGIyM2ZlNzYzNjBlZmEyZTk6MGVmNDg3ZjU0ZmM3NDcwNWIxZmMxYTE3MjRjZjE3ODE6ZWU1NGMxMThlMjA0MGNhNw==",
            "Content-Type": "application/json",
        }

    def api_post_redeem_redeeming(self,redeemNo):
        """
        家长中心-兑换
        redeemNo
        """
        api_url='/redeeming'
        body={
            'redeemNo':redeemNo
        }
        print(self.host+self.root+api_url)
        resp=send_api_request(url=self.host+self.root+api_url,paramType='list',paramData=body,method="post",headers=self.header)

        print(resp)
    def api_post_redeem_getlist(self,uid='fc8882b5fa674e80b23fe76360efa2e9'):
        """
        家长中心-兑换码查询
        """
        api_url='/getList'
        print(self.host+self.root+api_url)
        resp=send_api_request(url=self.host+self.root+api_url,method="post",headers=self.header)
        print(resp)



# if __name__=='__main__':
#     dm=Domains()
#     config=dm.set_env_path('fat')
#     token = UserProperty ( 'lisa02@qq.com' ).basic_auth
#     redeeming=ApiTradeRedeemRedeeming(token)
#     resp=redeeming.api_post_redeem_redeeming(redeemNo="pf8q3eDH8cNKPy")
#     print(resp)

