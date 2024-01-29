# @Time    : 2021/2/3 6:05 下午
# @Author  : ygritte
# @File    : ApiLogin


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiInnerLogin:
    """
    InnerLoginController
    """
    root = "/api/inner/saturn"

    def __init__(self):
        self.host = Domains.get_ggr_host()
        self.headers = {"version": "1", "Content-Type": "application/json;charset=utf-8"}

    def api_getInfo(self, authCode):
        """
        登录接口，获取token
        """
        api_url = f'{self.root}/getInfo'
        body = {
            "authCode": authCode
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType='params',
                                paramData=body, headers=self.headers)
        return resp

    def api_logout(self):
        """
        管理平台登出接口
        """
        api_url = f'{self.root}/logout'
        resp = send_api_request(url=self.host + api_url, method="get", paramType='params',
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    login = ApiInnerLogin()
    res = login.api_getInfo(authCode="b3497696f7ed4a699aa0947c73e04703")
    print(res)


