# -*- coding: utf-8 -*-
# @Time : 2021/6/18 3:00 下午
# @Author : jane
# @File : ApiNewReport.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiNewReport():
    """
    lessonbiz:获取MC PH课后报告
    LessonController
    """
    def __init__(self,token,version):
        self.host = Domains.config.get('url')
        self.root = '/api/lesson'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }
    def api_get_newreport(self,bid,lid,subtaskid):
        """
        MC/PH学习报告
        :param bid:宝贝id
        :param lid:当前课程id
        :return:
        """
        api_url = f"{self.host}{self.root}/newreport"
        body = {
            "bid":bid,
            "lid":lid,
            "subtaskid": subtaskid
        }
        resp = send_api_request(url=api_url,method="get",headers=self.headers, paramType="params", paramData=body)
        return resp
    '''
    post请求直接返回空
        def api_post_newreport(self,bid,lid,subtaskid):
        """
        MC/PH 学习报告
        :param bid:宝贝id
        :param lid:当前课程id
        :param subtaskid:子任务id
        """
        api_url = f"{self.host}{self.root}/newreport"
        body = {
            "bid":bid,
            "lid":lid,
            "subtaskid":subtaskid
        }
        resp = send_api_request(method="post",url=api_url,headers=self.headers,paramType="params",paramData=body)
        return resp
    '''


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19991011051")
    token = user.basic_auth
    version = config['version']['ver11.6']
    resport = ApiNewReport(token,version)
    resp = resport.api_get_newreport("1b877919e16d4a8682bce4014bf70c6b","L1PH20","L1PH202")
    print(resp)
