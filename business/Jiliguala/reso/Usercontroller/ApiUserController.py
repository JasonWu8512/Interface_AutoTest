''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/14
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUserController(object):
    """查看魔石明细"""
    root = 'api/magika/user/trans'

    def __init__(self,token):
        # print(token)
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token

        }
        print(self.headers)
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]

    def magika(self):
        """"""
        api_url = "/api/magika/user/trans"
        print(self.host + self.root)
        body = {"page":0,
                "tab":"in"}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData = body , method="get",
                                headers=self.headers)
        print(resp)
        return resp


# if __name__ == '__main__':
#     a = ApiUserController()
#     a.magika()
