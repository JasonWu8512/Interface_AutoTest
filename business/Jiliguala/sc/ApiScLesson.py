''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/23
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiScLesson(object):
    """
    sc课程详情页
    """
    root = '/api/sc/lesson'

    def __init__(self, token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token
            # "Basic MTY3MmJhNWIzNmRkNGNhNDkzY2FlZmM5NjFjNmY0YjU6MDk0ZDdjOGNkYTNkNDU4N2E3NWQwNzFhNjU4Y2ExYTA="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["url"]
        print(self.host)

    def api_lesson(self, bid, lessonId, albumId):
        api_url = "/api/sc/lesson"
        print(self.host + self.root)
        # body = {"bid":bid,
        #         "lessonId":"LCDS002",
        #         "albumId":"AlbumCDS001",
        #         "nonce":""}
        # 参数化
        body = {"bid": bid,
                "lessonId": lessonId,
                "albumId": albumId,
                "nonce": ""}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

# if __name__ == '__main__':
#     a = ApiScLesson()
#     a.api_lesson()
