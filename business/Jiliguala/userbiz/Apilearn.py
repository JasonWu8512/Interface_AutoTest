''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/8
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class Api_Learn_Report(object):
    """课后报告详情页"""
    root = '/api/learn/report'

    def __init__(self, token):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token
            # "Basic MTY3MmJhNWIzNmRkNGNhNDkzY2FlZmM5NjFjNmY0YjU6MDk0ZDdjOGNkYTNkNDU4N2E3NWQwNzFhNjU4Y2ExYTA="
        }
        # 设置域名host
        self.host = Domains.config.get('url')
        print(self.host)

    def api_report(self, bid, lessonId):
        """
        接口信息
        """
        api_url = "/api/learn/report"
        print(self.host + self.root)
        body = {'bid': bid,
                'lessonId': lessonId}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

# if __name__ == '__main__':
#     a=Api_Learn_Report()
#     a.api_report()
