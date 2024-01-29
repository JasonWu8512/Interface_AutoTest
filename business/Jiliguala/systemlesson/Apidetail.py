''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/26
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiDetail(object):
    """课后报告详情页"""
    root = '/api/v3/lesson/detail'

    def __init__(self, token):
        # self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token
            # "Basic MTY3MmJhNWIzNmRkNGNhNDkzY2FlZmM5NjFjNmY0YjU6MDk0ZDdjOGNkYTNkNDU4N2E3NWQwNzFhNjU4Y2ExYTA="
        }
        # 设置域名host
        self.host = Domains.config.get('url')
        print(self.host)

    def api_detail(self, bid, lid):
        """
        接口信息
        """
        api_url = "/api/v3/lesson/detail"
        print(self.host + self.root)
        body = {'lid': lid,
                'bid': bid}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_lesson_report(self, bid, lessonid):
        """
        1.5课后报告
        :param bid：宝贝id,课程id
        :return:
        """
        api_url = "/api/lesson/singlelessonreport"
        body = {
            "bid": bid,
            "lessonid": lessonid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method='get',
                                headers=self.headers)
        return resp

if __name__ == '__main__':
    a = ApiDetail()
    a.api_detail()
