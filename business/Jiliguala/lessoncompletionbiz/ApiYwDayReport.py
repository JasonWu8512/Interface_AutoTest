# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 6:46 下午
# @Author  : jacky_yuan
# @File    : ApiYwDayReport.py


from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiDayReport():
    """
    lesson-completion  C端: 语文日报接口
    Dayreport
    """

    def __init__(self, token):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token
        }

    def api_day_report(self, bid, lessonId):
        """
        语文日报展示
        :param bid:宝贝id
        :param lessonId:课程id
        :return:
        """
        api_url = "/api/learn/report"
        body = {
            "bid": bid,
            "lessonId": lessonId
        }
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("17621160716")
    token = user.basic_auth
    report = ApiDayReport(token)
    resp = report.api_day_report(bid="c1ee7624af344e4eb1344b1df6a2cd1b", lessonId="Z1YWF001")
    print(resp)


