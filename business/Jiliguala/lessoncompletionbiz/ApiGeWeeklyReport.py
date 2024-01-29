# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 6:46 下午
# @Author  : jacky_yuan
# @File    : ApiGeWeeklyReport.py


from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiWeeklyReport():
    """
    lesson-completion  C端: 英语3.0课程周报接口
    Weeklyreport
    """

    def __init__(self, token):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token
        }

    def api_weekly_report(self, uid, startTime):
        """
        英语3.0课程周报展示
        :param uid: 用户id
        :param  startTime: 开课时间
        :return:
        """
        api_url = "/api/learn/ge/weekly/report"
        body = {
            "uid": uid,
            "startTime": startTime
        }
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("20000002947")
    token = user.basic_auth
    report = ApiWeeklyReport(token)
    resp = report.api_weekly_report(uid="8751910de5a24dea9abd45d676485cf0", startTime="2021-06-21")
    print(resp)


