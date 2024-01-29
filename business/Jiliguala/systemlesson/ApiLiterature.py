''' 
===============
@Project  :  JLGL_autotest
@Author   :  Anna
@Data     :  2023/4/13
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiLiterature(object):
    """国学百科详情页"""
    root = '/api/literature'

    def __init__(self, token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token
        }
        # 设置域名host
        self.host = Domains.config.get('url')
        print(self.host)

    def api_Literature(self, bid, lid):
        """
        百科详情页
        :param bid:宝宝id
        :param lid:课程id
        :return:
        """
        api_url = f"{self.root}/lesson"
        print(self.host + self.root)
        body = {'lid': lid,
                'bid': bid}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

if __name__ == '__main__':
    a = ApiLiterature()
    a.api_Literature()
