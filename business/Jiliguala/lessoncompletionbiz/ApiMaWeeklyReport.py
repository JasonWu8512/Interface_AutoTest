# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 6:46 下午
# @Author  : jacky_yuan
# @File    : ApiMaWeeklyReport.py


from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiWeeklyReport():
    """
    lesson-completion  C端: 思维周报接口
    Weeklyreport
    """

    def __init__(self, token):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token
        }

    def api_weekly_report(self, bid, weekId):
        """
        思维周报展示
        :param bid:宝贝id
        :param weekId:周id
        :return:
        """
        api_url = "/api/learn/ma/weekly/report"
        body = {
            "bid": bid,
            "weekId": weekId
        }
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("17621160716")
    token = user.basic_auth
    report = ApiWeeklyReport(token)
    resp = report.api_weekly_report(bid="e9f18597eae14a3a9aa3e58ec1967793", weekId="K1MAE04")
    print(resp)


