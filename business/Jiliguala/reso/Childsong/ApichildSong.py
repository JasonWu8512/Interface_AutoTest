''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/15
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request



class ChildSong(object):
    """儿歌学堂"""

    root = 'api/sc/childsong'
    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" : token
                # "Basic MTY3MmJhNWIzNmRkNGNhNDkzY2FlZmM5NjFjNmY0YjU6MDk0ZDdjOGNkYTNkNDU4N2E3NWQwNzFhNjU4Y2ExYTA="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def songs(self,bid,nonce):

        api_url = "/api/sc/childsong"
        print(self.host + self.root)
        body = {"bid": bid,
                'level': 'F1GE',
                'nonce': nonce} #接口需要的参数
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",#发送接口
                                headers=self.headers)
        print(resp)
        return resp


