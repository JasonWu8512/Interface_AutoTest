'''
@Author : degg_wang
@Date : 2022/9/6
@File : ApiUserbuy
'''


from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains


class ApiUserbuy(object):
    """
        资产相关
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def getUserMostAdvancedLevel(self,uid):
        """
            查出已拥有的最高级别课程
           :param uid: 用户id
           :return:
                levelId: 路线图ID
        """
        api_url = "/inner/course/userbuy/getUserMostAdvancedLevel"
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="post",
                                headers=self.headers)
        return resp

    def whetherPossessRegularLesson(self,uid):
        """
            询是否拥有任意正式课（灵活课包资产）
            :param uid: 用户id
           :return:
                whetherPossess： 是否拥有正式课（false/true）
        """
        api_url = "/inner/course/userbuy/whetherPossessRegularLesson"
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="post",
                               headers=self.headers)
        return resp