"""
=========
Author:WenLing.xu
time:2023/12/07
=========
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSkip(object):

    def __init__(self, token=None):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "platform": "ios",
            "dev_uni_id": "C264F398 - 4132 - 4162 - BC09 - 8DD21CA8CACC",
            "Accept-Language": "en-us"
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path("fat")["gaga_url"]

    def skip(self, lid, bid):
        """正式课跳课"""
        api_url = "/api/lesson/skip"
        body = {"lid": lid,
                "bid": bid
                }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp