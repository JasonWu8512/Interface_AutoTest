''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/22
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request



class GetGuadou(object):
    """获取瓜豆状态"""

    root = '/api/guadou/state'
    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" : token
                # "Basic MTY1ZTdlODg4OTYxNGNlZmI3MmE1ZTM5NjZkYjU3MjA6MGEwOWI0MTc1YzBlNDljNTg3MTJhYjE4MDU2N2U1ZjA="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def guadou_state(self):
        """
        接口信息
        """
        api_url = "/api/guadou/state"
        print(self.host + self.root)
        body = {'fields' : 'balance',
                'nonce' : '0ec67f14-bf27-4c66-9444-a23bd92825e6'}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

