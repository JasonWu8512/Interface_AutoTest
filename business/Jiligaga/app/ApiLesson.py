# -*- coding: utf-8 -*-
# @Time : 2022/6/24 下午1:54
# @Author : Saber
# @File : ApiLessonDetail.py

# import email
# import pytest
# import lazy_property

from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiLesson():
    """
    app  C端：课程详情页
    Lesson Controller
    """

    def __init__(self, token= None):
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        self.root01 = '/api/subLesson'
        self.root02 = '/api/section'
        self.root03 = '/api/web/section'
        self.headers = {
            "authorization": token,
            # "Content-Type": "application/json"
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def api_lesson_detail_v2(self, bid, lid):
        """
        课程详情页查询
        :param bid：宝贝id,lessonIds:课程id
        :return:
        """
        api_url = '/api/lesson/detail/v2'
        body = {
            "bid": bid,
            "lid": lid

        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method='get',
                                headers=self.headers)
        return resp

    def api_lesson_resource(self,bid,cocosEnv,lessonIds,lessonVersion):
        """
        获取课程资源
        :params
        :return:
        """
        api_url = '/api/lesson/resource'
        body = {
            "bid": bid,
            "cocosEnv": cocosEnv,
            "lessonIds": lessonIds,
            "lessonVersion": lessonVersion
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method='get',
                                headers=self.headers)
        return resp

    def api_lesson_skip(self, bid, lid):
        """
        跳课
        bid：宝贝id,lid：课程id
        :return:
        """
        api_url = '/api/lesson/skip'
        body = {
            "bid": bid,
            "lid": lid
        }

        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method='post',
                                headers=self.headers)
        return resp

    def api_sublesson_progress(self, avgScore, bid,lessonId,subLessonId,gameId):
        """
        sublesson子课分数上报
        :return:
        """
        api_url = '/api/web/section/progress'
        body = {
            "avgScore":avgScore,
            "bid":bid,
            "lessonId":lessonId,
            "subLessonId":subLessonId,
            "gameId":gameId
        }

        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method='post',
                                headers=self.headers)
        return resp

    def api_section_progress(self,bid,gameId,sectionId,subLessonId,lessonId,sectionType,score):
        """
        cocos脚本课知识点分数上报
        :return:
        """
        api_url = '/api/section/progress'
        body = {
              "bid":bid,
              "gameId":gameId,
              "sectionId":sectionId,
              "subLessonId":subLessonId,
              "lessonId":lessonId,
              "sectionType":sectionType,
              "score":score,
              "roundDetail": [

              ],
              "sentenceDetail": [

              ],
              "details":[
                        ]

              }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method='post',
                                headers=self.headers)
        return resp


    def api_web_section_progress(self,bid,gameId,sectionId,sublessonId,lessonId,score,ruleType,
                                 displayScore,realScore,audioDecibel,audioTag,audioUrl,questionId,
                                 knowledgeId,skillId,predScore,gamePredId,fixedType,scoreComponentID,
                                 scoreComponentType,klgFinishTime,finishTime):
        """
        web编辑器上报接口
        :return:
        """
        api_url = '/api/subLesson/progress'
        body = {
              "bid":bid,
              "gameId":gameId,
              "sectionId":sectionId,
              "sublessonId":sublessonId,
              "lessonId":lessonId,
              "score":score,
              "details":[{
                        "ruleType":ruleType,
                        "displayScore":displayScore,
                        "realScore":realScore,
                        "audioDecibel":audioDecibel,
                        "audioTag":audioTag,
                        "audioUrl":audioUrl,
                        "questionId":questionId,
                        "knowledgeId":knowledgeId,
                        "skillId":skillId,
                        "predScore":predScore,
                        "gamePredId":gamePredId,
                        "fixedType":fixedType,
                        "scoreComponentID":scoreComponentID,
                        "scoreComponentType":scoreComponentType,
                        "klgFinishTime":klgFinishTime}],
              "finishTime": finishTime
              }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method='post',
                                headers=self.headers)
        return resp



if __name__ == '__main__':
    # dm = Domains()
    # config=dm.get_jlgg_host('fat')
    # config = dm.set_env_path("fat")
    token = 'Basic NWI4ZWVhZmRkZmRlNGYwOWFjODk4MDgyZjBhNTMyYTI6M2Y2MmUzNWM5NGNjNGJiMGE2ODJmYjcxNTA4NWJkNTY6NUQxMURCNkItNzg4OC00OTk1LTg4OTEtQzNBOUM1NUVBNUI4'
    lesson = ApiLesson(token)
    # 查询课程详情页
    resp = lesson.api_lesson_detail_v2(bid='2e009c7d83954ccbbb5a81281a733873',lid='12ade73d49813a0d8d3aedabf28c0fe6')
    print(resp)
#
#
#     # 获取课程资源
#     # resp = lesson.api_lesson_resource(bid='5f38d13dc4164d20b6480402af07c1aa',cocosEnv='abroad',lessonIds='d488bb8556d634c4ba728595e1b0a1a8',lessonVersion='2')
#
#
#     # 跳过课程
#     # resp = lesson.api_lesson_skip(bid='5f38d13dc4164d20b6480402af07c1aa',lid='93a32af2f3f33f4793d0d6e44cc13e04')
#
#
#     # 子课分数上报
#     # resp = lesson.api_sublesson_progress(avgScore=-1,bid='5f38d13dc4164d20b6480402af07c1aa',lessonId='a33c5f5ef1ad3d12a9cea60cb027b4db',subLessonId='8d43670804de3182b04f250c41a2ca8b',gameId='B1GEW03D2L1')
#
#
#    # web编辑器分数上报
#    #  resp = lesson.api_web_section_progress(bid="1413d35c30f64145babbd2bbb4f06cc3", gameId="B1GEW01D3L1",sectionId="1ad7289ca449bf3e",sublessonId="57f9b0b134c330e4935e699997c0fa34",
#    #                                         lessonId="aed750e4762030af829301261ff21cae",score=100,ruleType="drag",displayScore=100,realScore=100,audioDecibel=None,audioTag=None,
#    #                                         audioUrl=None,questionId=None,knowledgeId="GEKLT2850818",skillId="GESLS2784867",predScore=None,gamePredId=None,fixedType=1,
#    #                                         scoreComponentID="itemId-1ec7d3cbffec9b30",scoreComponentType="dragScoreCalculator",klgFinishTime=1658563864095,finishTime=1658563873602)
#
#     #cocos脚本课程知识点分数上报
#     # resp = lesson.api_section_progress(bid="1413d35c30f64145babbd2bbb4f06cc3",gameId="B1GEW01D1L1",sectionId="B1GEW01D1L1sec_V01",
#     #                                   subLessonId="5aab1c4b334d3640a1de3a87f915d5b1",lessonId="12ade73d49813a0d8d3aedabf28c0fe6",
#     #                                   sectionType="video-new",score=-1)
#     # print(resp)
#
