''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/18
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request



class UserDevices(object):
    """
    获取用户设备信息
    """
    root = "/api/users/devices"

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" : token
                # "Basic MTY3MmJhNWIzNmRkNGNhNDkzY2FlZmM5NjFjNmY0YjU6MDk0ZDdjOGNkYTNkNDU4N2E3NWQwNzFhNjU4Y2ExYTA="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def devices(self):
        """
        接口信息
        """
        api_url = "/api/users/devices"
        print(self.host + self.root)
        body = {"nonce" : "b252bf75-80bc-4113-bd4a-0b3beffa2559"}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


# if __name__ == '__main__':
#     a = UserDevices()
#     a.devices()