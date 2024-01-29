''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/31
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser

class Apitable(object):
    """
    拓展tab详情页
    """
    root = '/api/sc/table'

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" : token
                # "Basic YmFlZGY0ZWJjYjYwNDk3YTg5ZjlkZGI3OTA4N2U2ZDY6OGVhNmYxM2Q3Y2VjNGM1M2E3MWFiMTExZGUxMmFiMzc="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_table(self,bid):
        api_url = "/api/sc/table"
        print(self.host + self.root)
        body = {
                'bid':bid,
                "nonce":"ff2a77be-550e-4721-add0-b51c11fd9b6c"}

        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


# if __name__ == '__main__':
#
#     dm = Domains()
#     config = dm.set_env_path('fat')
#     dm.set_domain(config['url'])
#     user = ApiUser()
#     token = user.get_token(typ="mobile", u="18664309513", p="123456")
#     apitable = Apitable(token=token)
#     apitable.api_table()


