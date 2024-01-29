''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/23
===============
'''



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiList(object):
    """
    sc拓展资源列表页
    """
    root = '/api/sc/album/list'

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" : token
                # "Basic ODk2NmY3YjIxZWIzNGU5ZmJlNjJlODIxYzk5NTNiMDM6ZWExYzgzNDc1N2RkNDViNjhmNjcxNzU1NjIwNjY0Njc="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["url"]
        print(self.host)

    def api_list(self):
        """
        课程上报
        """
        api_url = "/api/sc/album/list"
        print(self.host + self.root)
        body = {"page":0,
                'nonce':'4f14580d-320f-40b7-aaae-81d3f4fa3e66'}

        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

#
# if __name__ == '__main__':
#     a = ApiPList()
#     a.api_list()