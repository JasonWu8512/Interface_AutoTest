''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/26
===============
'''


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request



class ApiProgress(object):
    """完课上报"""
    root = '/api/v3/sublesson/progress'

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" : token
                # "Basic MTY3MmJhNWIzNmRkNGNhNDkzY2FlZmM5NjFjNmY0YjU6MDk0ZDdjOGNkYTNkNDU4N2E3NWQwNzFhNjU4Y2ExYTA=",


        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_progress(self,bid):
        """

        """
        api_url = "/api/v3/sublesson/progress"
        print(self.host + self.root)
        body = {"gameId":"SPW02D02L1",
                "avgScore":-1,
                "subLessonId":"F1GEF00701",
                "lessonId":"F1GEF007",
                "bid":bid}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp


# if __name__ == '__main__':
#     a = ApiProgress()
#     a.api_progress()