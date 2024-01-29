''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/23
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiScBuy(object):
    """
    sc课程专辑购买
    """
    root = '/api/sc/buy'

    def __init__(self, token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token

        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["url"]
        print(self.host)

    def api_buy(self, lessonId, albumId):
        """
        课程购买
        """
        api_url = "/api/sc/buy"
        print(self.host + self.root)
        # body = {'lessonId':'LCIX001',
        #           'albumId':'AlbumCIX001'}
        # 参数化
        body = {'lessonId': lessonId,
                'albumId': albumId}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

# if __name__ == '__main__':
#     a = ApiScBuy()
#     a.api_buy()
