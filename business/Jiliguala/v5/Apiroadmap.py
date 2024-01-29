''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/23
===============
'''


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiRoadmap(object):
    """
    v5路线图
    """
    root = '/api/v5/roadmap'

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" :token
                # "Basic ODk2NmY3YjIxZWIzNGU5ZmJlNjJlODIxYzk5NTNiMDM6ZWExYzgzNDc1N2RkNDViNjhmNjcxNzU1NjIwNjY0Njc="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_roadmapKC(self,bid):
        """
        英语课程路线图
        """
        api_url = "/api/v5/roadmap"
        print(self.host + self.root)
        body = {'level':'',
                'subject':'GE',
                'weekId':'',
                'lessonId':"",
                'source':'',
                'bid':bid,
                'nonce':'ecc46fe2-a809-404b-9b62-376691f9f365'}
        resp1 = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp1)
        return resp1

    def api_roadmapSW(self,bid):
            """
            思维课程路线图
            """
            api_url = "/api/v5/roadmap"
            print(self.host + self.root)
            body = {'level':'',
                    'subject':'MA',
                    'weekId':'',
                    'lessonId':'',
                    'source':'',
                    'bid':bid,
                    'nonce':'24abd1fe-2529-4cee-9353-1948cc0e5c17'}
            resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                    headers=self.headers)
            print(resp)
            return resp

# if __name__ == '__main__':
#     a = ApiRoadmap()
#     # a.api_roadmapSW()
#     a.api_roadmapKC()