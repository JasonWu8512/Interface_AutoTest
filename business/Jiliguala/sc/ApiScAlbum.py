''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/23
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser


class Apialbum(object):
    """
    sc课程详情页
    """
    root = '/api/sc/album'

    def __init__(self, token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token
            # "Basic OWI4OGJkOTkwY2Q2NGNhYTgyYmNlZGI5NTM5YmY5NjQ6ZWQwMWQyOThiN2NiNGY5NWFkNGYzYjQ2NmIwZWM5ZGI="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["url"]
        print(self.host)

    def api_album(self, bid, albumId):
        api_url = "/api/sc/album"
        print(self.host + self.root)
        # 参数化前代码
        # body = {'albumId':'AlbumCIX001',
        #         'bid':bid,
        #         "nonce":"9E5133B2-2D0E-45F3-A3F4-05D9C0588A55"}

        body = {'bid': bid,
                'albumId': albumId}

        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = ApiUser()
    CS_user = config["CS_user"]
    SC_album = config["SC_album"]
    token = user.get_token(typ="mobile", u=CS_user["user"], p=CS_user['pwd'])
    apialbum = Apialbum(token=token)
    apialbum.api_album(SC_album['bid'])
