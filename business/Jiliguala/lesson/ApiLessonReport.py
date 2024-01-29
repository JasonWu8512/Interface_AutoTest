# -*- coding: utf-8 -*-
# @Time : 2021/6/21 4:22 下午
# @Author : jane
# @File : ApiLessonreport.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiLessonReport:
    """
    课后报告
    lessonbiz
    LessonController
    """
    def __init__(self,token,version):
        self.host = Domains.config.get('url')
        self.root = '/api/lesson'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-App-Version":version
        }
    def api_lesson_report(self,bid,lid):
        api_url = f"{self.host}{self.root}/report"
        body = {
            "bid": bid,
            "lid":lid
        }
        resp = send_api_request(method="get",url=api_url,headers=self.headers, paramType="params", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty('19991011051')
    token = user.basic_auth
    version = config['version']['ver11.0']
    report = ApiLessonReport(token,version)
    resp = report.api_lesson_report("1b877919e16d4a8682bce4014bf70c6b",'B2MC29')
    print(resp)

