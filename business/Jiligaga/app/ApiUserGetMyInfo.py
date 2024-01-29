"""
=========
Author:Lisa
time:2022/6/20 10:25 下午
=========
"""
from ensurepip import version
# import resp as resp
from paramiko import agent

from business.Jiligaga.app.ApiLogin import Login
from business.common.UserProperty import UserProperty
from business.xshare.ApiUser import ApiUser
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUserGetMyInfo():
    """
    app  C端：获取家长区域

    """

    def __init__(self, token=None):
        self.login = Login ()
        self.dm = Domains ()
        self.gaga_app = self.dm.set_env_path ( 'fat' )["gaga_app"]
        # self.token = self.login.phone_pwd_login(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"])["data"]["auth"]
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "platform": "ios",
            # "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC",
            "Authorization": token
        }
        self.dm = Domains ()
        # 设置域名host
        self.host = self.dm.set_env_path ( 'fat' )["gaga_url"]

    def api_user_getMyInfo(self):
        """
        家长区域查询
        """
        api_url = "/api/user/getMyInfo"
        body = {

        }
        resp = send_api_request ( url=self.host + api_url, paramType='params', paramData=body, method="post",
                                  headers=self.headers )
        return resp


# if __name__ == '__main__':
#     dm = Domains ()
#     dm.set_domain ( "https://fat.jiligaga.com" )

