"""
=========
Author:Lisa
time:2022/7/19 2:17 下午
=========
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTradeRedeemGetlist():
    """
    获取兑换码列表

    """
    def __init__(self,authorization,):
        self.host = Domains.get_gaga_host ()
        self.root = '/api/trade/redeem'
        self.header={
            "authorization": "Basic NTU1ZmE2NmExYjAxNDczYTk3MzEzOWUwYTY1NzM4NDg6YTk1MjdmZjZmNzExNDRiZjg1YTlkYmRhYjU3NjUxZGY6ZWU1NGMxMThlMjA0MGNhNw==",
            "Content-Type": "application/json",
        }
    def api_trade_redeem_getlist(self):
        """
        获取兑换码列表
        """
        api_url='/getList'
        body={

        }
        print(self.host+self.root+api_url)
        resp = send_api_request ( url=self.host + self.root + api_url, paramType='json', paramData=body, method="post",
                                  headers=self.header )
        print(resp)

# if __name__ == '__main__':
#      dm = Domains()
#      config = dm.set_env_path("fat")
#      token = UserProperty('0800001111').basic_auth
#      redeemgetlist =ApiTradeRedeemGetlist(token)
#      # 获取兑换码列表
#      resp= redeemgetlist.api_trade_redeem_getlist()
#      print(resp)


