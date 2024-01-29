# coding=utf-8
# @Time    : 2022/10/28 5:44 下午
# @Author  : Karen
# @File    : ApiResource.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiResource(object):
    ''' 课程资源 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_resource_package_base(self):
        """ 01）获取课程资源包 """
        api_url = "/api/resource/package/base"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp

    def api_resource_book_page(self,id):
        """ 02）获取课程内容图片 """
        api_url = "/api/resource/book/page"
        body = {'id':id}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp