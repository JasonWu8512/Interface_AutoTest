''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/23
===============
'''



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiProgress(object):
    """
    sc课程上报
    """
    root = '/api/sc/lesson/progress'

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

    def api_progress(self,bid):
        """
        课程上报
        """
        api_url = "/api/sc/lesson/progress"
        print(self.host + self.root)
        body = {"bid":bid,
                "lessonid":"LCDS045",
                "sublessonid":"LCDS0452",
                "units":[{"content":"N/A",
                          "realscore":0,
                          "score":0,
                          "sectionid":"DS0452sec01",
                          "skill":"N/A"},
                         {"content":"N/A",
                          "realscore":100,
                          "score":100,
                          "sectionid":"DS0452sec02",
                          "skill":"N/A"},
                         {"content":"N/A",
                          "realscore":100,
                          "score":100,
                          "sectionid":"DS0452sec03",
                          "skill":"N/A"},
                         {"content":"N/A",
                          "realscore":0,
                          "score":0,
                          "sectionid":"DS0452sec04",
                          "skill":"N/A"}]}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp


# if __name__ == '__main__':
#     a = ApiProgress()
#     a.api_progress()