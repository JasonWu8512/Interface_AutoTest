"""
=========
Author:Lisa
time:2023/4/24 6:25 下午
=========
"""
from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains


class ApiRoadmapExperienceLessonTake():
    """
    人转-路线图领取体验课
    """

    def __init__(self, token=None, appversion=None) -> object:
        self.dm = Domains()
        self.host = self.dm.set_env_path("fat")["gaga_url"]
        self.root = '/api/roadmap/experience/lesson/take'
        self.headers = {
            "authorization": token,
            "Content-Type": "application/json",
            "appversion": appversion,
            "platform": "ios"

        }

    def api_roadmap_experience_lessontake(self, source):
        """人转-路线图领取体验课"""
        api_url = "/api/roadmap/experience/lesson/take"
        body = {
            "source": source
        }
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)

        return resp
