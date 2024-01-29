'''
@Author : degg_wang
@Date : 2022/9/6
@File : ApiStudy
'''


from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains

class ApiStudy(object):
    """
        学习服务
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def start_class(self, uid, source, buyTime, courseBundleList):
        """
            购课-开课（灵活路线图，点石成金小程序，实体英语）
            :param source:   来源
            :param buyTime:   购买时间
            :param courseBundleList: 课包list
            :param uid: 用户id
            :return:
        """
        api_url = "/api/v1/study/startClass"
        body = {
            "source": source,
            "buyTime": buyTime,
            "courseBundleList": courseBundleList,
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="post",
                                headers=self.headers)
        return resp


    def get_possess_course_bundles(self, curriculumCode, uid):
        """
            购课-查询购课信息（灵活路线图，点石成金小程序，实体英语）
            :param curriculumCode: 课程code
            :param uid: 用户id
            :return:
        """
        api_url = "/api/v1/study/getPossessCourseBundles"
        body = {
            "curriculumCode": curriculumCode,
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="post",
                                headers=self.headers)
        return resp