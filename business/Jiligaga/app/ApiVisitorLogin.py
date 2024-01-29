"""
=========
Author:WenLing.xu
time:2022/7/14
=========
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiVisitorLogin(object):

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "platform": "ios",
            "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC"
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def visitor_login(self):
        """游客登录"""
        api_url = "/api/user/visitor/login"
        body = {
            "birthDesc": "2014-12",
            "nick": "",
            "autoTakeTrialMember": True,
            "userRegisterEvent": {
                "deviceType": "ANA-AN00",
                "osVersion": "10",
                "countryCode": "CN",
                "languageCode": "zh",
                "deviceManufacturer": "HUAWEI",
                "deviceBrand": "HUAWEI"
            }
        }
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def visitor_login_salesman(self, countryCode, languageCode):
        """游客登录-人转游客"""
        api_url = "/api/user/visitor/login"
        body = {
            "birthDesc": "2014-12",
            "nick": "",
            "autoTakeTrialMember": True,
            "userRegisterEvent": {
                "deviceType": "ANA-AN00",
                "osVersion": "10",
                "countryCode": countryCode,
                "languageCode": languageCode,
                "deviceManufacturer": "HUAWEI",
                "deviceBrand": "HUAWEI"
            }
        }
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        api_url = "/api/user/debug/change/businesstype?type=1&uid={}".format(resp["data"]["user"]["userNo"])
        print(api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp
# if __name__ == '__main__':
#     a =ApiVisitorLogin()
#     a.visitor_login_salesman()
