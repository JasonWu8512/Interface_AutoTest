# -*- coding: utf-8 -*-
# @Time    : 2021/6/2 11:27 上午
# @Author  : jacky_yuan
# @File    : ApiVoiceFeedback.py


from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiVoiceFeedback():
    """
    lesson-completion  C端：呱美2.5语音反馈上报接口
    VoiceFeedback
    """

    def __init__(self, token):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "Version": "1"
        }

    def api_voice_feedback(self, uid, bid, lessonId, totalCount, feedbackCount, sameTagFlag):
        """
        语音反馈上报
        :param uid: 用户id
        :param bid: 宝贝id
        :param lessonId: 课程id
        :param totalCount: 上报数量
        :param feedbackCount: 上报中点踩的数量
        :param sameTagFlag: 上报是否带有引擎熟悉
        :return:
        """
        api_url = "/api/lesson/voice/v2/feedback"
        body = {
            "uid": uid,
            "bid": bid,
            "lessonId": lessonId,
            "totalCount": totalCount,
            "feedbackCount": feedbackCount,
            "sameTagFlag": sameTagFlag,
        }
        resp = send_api_request(url=self.host + api_url, method="post", headers=self.headers, paramType="json",
                                paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("20000002410")
    token = user.basic_auth
    voice = ApiVoiceFeedback(token)
    resp = voice.api_voice_feedback(uid="650cc553fb914e4aab9c2eda455afda9",
                                    bid="b5273eb6fe5c40b6b42a593ac23ca9e1",
                                    lessonId="K1GEF001",
                                    totalCount="1",
                                    feedbackCount="0",
                                    sameTagFlag="true"
                                    )
    print(resp)