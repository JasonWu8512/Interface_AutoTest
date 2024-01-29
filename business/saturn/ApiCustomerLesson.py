# @Time    : 2021/3/4 8:03 下
# @Author  : ygritte
# @File    : ApiCustomerLesson

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCustomerLesson:
    """
    CustomerLessonController
    """
    root = '/api/saturn/admin/customer'

    def __init__(self, admintoken=None):
        self.host = Domains.get_ggr_host()
        self.headers = {
            "version": "1",
            "Content-Type": "application/json;charset=utf-8",
            "admintoken": admintoken
        }

    def api_baby_list(self, uid):
        """
        获取baby信息
        """
        api_url = f'{self.root}/baby/list'
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType='params',
                                paramData=body, headers=self.headers)
        return resp

    def api_course_list(self, uid):
        """
        获取用户已购课程信息
        """
        api_url = f'{self.root}/course/list'
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params",
                                paramData=body, headers=self.headers)
        return resp

    def api_baby_learning_record(self, uid, bid):
        """
        获取用户baby学习记录
        """
        api_url = f'{self.root}/baby/learning/record'
        body = {
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params",
                                paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    cl = ApiCustomerLesson("cc486f08482c460bb5b2ee3ac0dcb28f")
    res = cl.api_baby_learning_record("eec88cf73e4541cd8b8130ea9840245e",
                                      "f28498b7329643f9a7c610b01b1df634")
    print(res)