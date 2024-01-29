# coding=utf-8
# @Time    : 2022/7/15 6:33 下午
# @Author  : Karen
# @File    : ApiGoldenTouch.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiGoldenTouch(object):

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_goldentouch_roadmap_v2(self,roadmapId,bid):
        """ 01）请求路线图 """
        api_url = "/api/goldentouch/roadmap/v2"
        body = {
            'roadmapId': roadmapId,
            'bid': bid
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="params", method="get",
                                headers=self.headers)
        return resp


    def api_goldentouch_lesson(self,roadmapId ,bid ,lid):
        """ 02）课程详情页 """
        api_url = "/api/goldentouch/lession"
        body = {
            'roadmapId': roadmapId,
            'bid': bid,
            'lid': lid
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="params", method="get",
                                headers=self.headers)
        return resp


    def api_goldentouch_video(self,gameId):
        """ 03）请求子课程视频 """
        api_url = "/api/goldentouch/video"
        body = {'gameId': gameId}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="params", method="get",
                                headers=self.headers)
        return resp


    def api_goldentouch_progress(self,gameId, nodeId, bid):
        """ 04）完课上报 """
        api_url = "/api/goldentouch/progress"
        body = {
            'gameId': gameId,
            'nodeId': nodeId,
            'bid': bid
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json',method="post", headers=self.headers)
        return resp