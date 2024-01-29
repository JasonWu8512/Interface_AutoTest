''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/18
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
import base64

class DeleteDevices(object):
    """
    删除设备信息
    """
    root = "/api/users/devices"

    def __init__(self):
        self.dm = Domains()
        self.host = self.dm.set_env_path('prod')["url"]

    def login(self):
          """
          游客登陆
          """
          api_url='/api/users/guest/v2'
          self.headers = {
              'Content-Type': 'application/json; charset=UTF-8',
              "Authorization": ''}
              # "Basic NzEzZDRkZDA1OTU0NDA2ZWIzYzExMjNhYWIxYjQzMTI6MDEwM2Y0MjlkZTgzNGYwNmE0OTJmMGI5Y2MyMGVlNjY="

          body = {'deviceId':'436f245525f425956bd0f6bbf6237c5f364ee513be0b32ed7643a1fba2a9be8c',
                  'deviceType':'vivo V2001A',
                  'version':111203,
                  'platform':1,
                  'model':0}
          resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="put",
                                          headers=self.headers)
          print(resp)
          return resp


    def get_token(self):

          res = self.login()
          token = res["data"]["tok"]
          uid = res["data"]["_id"]
          code = base64.b64encode(f'{uid}:{token}'.encode('utf-8'))
          token1='Basic ' + str(code, encoding="utf-8")
          print(token1)
          return token1


    def delete_devices(self):
        """
        删除指定设备
        """
        api_url = "/api/users/devices"
        print(self.host + self.root)
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": DeleteDevices().get_token(),
             # "Basic MDA0MTgyZDU4NTliNDZlM2IxNDZjZTgzMmY3OTg5ZTI6OTE4ODE2NjQyNzE4NGViODgxNjI3ZTkwNDYwOTcxMzY="
        }
        body = {'deviceId': '436f245525f425956bd0f6bbf6237c5f364ee513be0b32ed7643a1fba2a9be8c',

                }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="delete",
                                headers=self.headers)
        return resp

    def globe(self):
        """
        删除设备操作提示信息
        """

        api_url = "/api/globe"
        print(self.host + self.root)
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": DeleteDevices().get_token()
            # "Basic NzEzZDRkZDA1OTU0NDA2ZWIzYzExMjNhYWIxYjQzMTI6MDEwM2Y0MjlkZTgzNGYwNmE0OTJmMGI5Y2MyMGVlNjY="
        }
        body = {#'android_ch':'JLGLWBM',
                #'android_ver': 111202,
                'bid': 'a5ecaa63abe84fe0a7714468e680087b','level':'K1GE',
                'nonce':'9e7cbc73-583f-4226-b13d-3e34a8a8dcbe'}
        resp1 = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)

        print('这是',resp1)
        return resp1



if __name__ == '__main__':
      # a = DeleteDevices().login()
      # b= DeleteDevices().get_token()
      # # a.login()
      # c=DeleteDevices().delete_devices()
      # d=DeleteDevices().globe()
      a = DeleteDevices()
      a.delete_devices()


