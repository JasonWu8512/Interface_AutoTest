"""
=========
Author:WenLing.xu
time:2023/11/27
=========
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCompleteCourse(object):

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
        self.host = self.dm.set_env_path('fat')["hw_eduplatform_url"]

    def course_schedule_update(self, uid, starttime):
        api_url = "/inner/course/inner/tools/courseScheduleUpdate"
        body = {
            "uid": uid,
            "roadmapId": "2f4d023a52024a9683229273c908ca24",
            "nodeId": "5779acc907aa4f899f9ad77de45479bf",
            "source": None,
            "startTime": starttime
        }
        print(body)
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp
