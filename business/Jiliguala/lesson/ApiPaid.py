"""
=========
Author:Lisa
time:2021/6/16 7:51 下午
=========
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPaid():
    '''
       LessonController
       已购课程
    '''

    def __init__(self, token, version, agent=None):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token,
            "Content-Type": "application/json",
            "X-APP-Version": version,
            "User-Agent": agent
        }

    def api_get_lesson_paid_v2(self, bid):
        '''
        :param bid:宝贝id
        :return:
        '''
        api_url = f"{self.host}/api/lesson/paid/v2"
        print(api_url)
        body = {
            "bid": bid
        }
        print(body)
        print(self.headers)
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        print(resp)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("18521030429")
    token = user.basic_auth
    version = config['version']['ver11.0']
    roadmap = ApiPaid(token, version)
    resp = roadmap.api_get_lesson_paid_v2("9f1be7047976453a904edd45a37a8c46")
    print(resp)
