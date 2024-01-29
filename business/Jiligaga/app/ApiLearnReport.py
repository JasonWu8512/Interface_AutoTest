# -*- coding: utf-8 -*-
# @Time : 2023/11/6 上午10:34
# @Author : Saber
# @File : ApiLearnReport.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
class ApiLearnReport ():
    """
    app  C端：课后报告详情页
    """
    def __init__(self):
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        self.headers = {
            "Content-Type": "application/json"
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def api_learn_report_experience(self, bid, lessonId):
        """
        体验课课后报告页查询
        :param bid：宝贝id,lessonId课程id
        :return:
        """
        api_url = '/api/learn/report/experience'
        body = {
            "bid": bid,
            "lessonId":lessonId
        }
        resp = send_api_request (url=self.host + api_url, paramType='params', paramData=body, method='get',
                                  headers=self.headers )
        print(resp)
        return resp

    def api_learn_report(self, bid, lessonId):
        """
        正价课课后报告页查询
        :param bid：宝贝id,lessonId课程id
        :return:
        """
        api_url = '/api/learn/report'
        body = {
            "bid": bid,
            "lessonId":lessonId
        }
        resp = send_api_request (url=self.host + api_url, paramType='params', paramData=body, method='get',
                                  headers=self.headers )
        print(resp)
        return resp



if __name__ == '__main__':
    learnreport = ApiLearnReport()
    #查询正价课课后报告页
    resp = learnreport.api_learn_report(bid='2e009c7d83954ccbbb5a81281a733873', lessonId='12ade73d49813a0d8d3aedabf28c0fe6')


    learnreport = ApiLearnReport()
    #查询体验课课后报告页
    resp = learnreport.api_learn_report_experience(bid='8d60d367452c41f6a4fc18878ca01a8d', lessonId='0241059f8f414a09b140fdae4a8a64f7')

