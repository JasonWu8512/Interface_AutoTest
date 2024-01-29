"""
=========
Author:Lisa
time:2021/6/16 11:17 下午
=========
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSmartreview():
    '''
        home
        ApiSmartreview 进入智能复习
    '''

    def __init__(self,token,version):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_smartreview_home(self, bid):
        '''
        :param bid:宝贝id
        :return:
        '''

        api_url = f"{self.host}/api/smartreview/home"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("18521030429" )
    token = user.basic_auth
    version = config['version']['ver11.0']
    roadmap = ApiSmartreview(token, version)
    resp = roadmap.api_get_smartreview_home("9f1be7047976453a904edd45a37a8c46")
    print(resp)
