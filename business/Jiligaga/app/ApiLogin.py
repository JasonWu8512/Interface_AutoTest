"""
=========
Author:WenLing.xu
time:2022/7/6
=========
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class Login(object):

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'dev_uni_id': 'iphone12,1'
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def mail_pwd_login_salesman(self, mail, pwd):
        """邮箱登录接口-人转用户"""
        url = "/api/user/login"
        body = {
            "account": mail,
            "password": pwd,
            "deviceType": "VOG-AL00"
        }
        resp = send_api_request(url=self.host + url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        api_url = "/api/user/debug/change/businesstype?type=1&uid={}".format(resp["data"]["user"]["userNo"])
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    # def phone_pwd_login_salesman(self, areaCode, phone, pwd):
    #     """手机登录接口-人转用户  已下线"""
    #     url = "/api/user/login/phone"
    #     body = {
    #         "areaCode": areaCode,
    #         "phone": phone,
    #         "password": pwd,
    #         "deviceType": "ANA-AN00"
    #     }
    #     resp = send_api_request(url=self.host + url, paramType="json", paramData=body, method="post",
    #                             headers=self.headers)
    #     api_url = "/api/user/debug/change/businesstype?type=1&uid={}".format(resp["data"]["user"]["userNo"])
    #     resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="get",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp

    def mail_pwd_login(self, mail, pwd):
        """邮箱登录接口"""
        url = "/api/user/login"
        body = {
            "account": mail,
            "password": pwd,
            "deviceType": "VOG-AL00"
        }
        resp = send_api_request(url=self.host + url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    # def code_login(self, code, phone):
    #     """验证码登录
    #       代码已下线
    #     """
    #     api_url = "/api/user/login/code"
    #     body = {
    #         "code": code,
    #         "areaCode": "86",
    #         "phone": phone,
    #         "deviceType": "iPhone13,2"
    #     }
    #     resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp

    # def phone_pwd_login(self, phone, pwd):
    #     """手机登录接口  已下线"""
    #     url = "/api/user/login/phone"
    #     body = {
    #         "areaCode": "886",
    #         "phone": phone,
    #         "password": pwd,
    #         "deviceType": "ANA-AN00"
    #     }
    #     resp = send_api_request(url=self.host + url, paramType="json", paramData=body, method="post",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp

    # def login_getcode(self, region=None, phone=None, mail=None):
    #     """
    #         接口已下线
    #         登录-发送验证码
    #       """

    #     api_url = "/api/user/login/send/code"
    #     body = {
    #         "source": "login",
    #         "mail": mail,
    #         "areaCode": region,
    #         "phone": phone
    #     }
    #     resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp

    def getMyInfo(self, authorization):
        """获取当前登陆用户信息"""
        api_url = "/api/user/getMyInfo"
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "authorization": authorization
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=None, method="post",
                                headers=headers)
        print(resp)
        return resp

# if __name__ == '__main__':
#     login = Login()
# login.mail_pwd_login(mail="wenling_xu@jiliguala.com", pwd="ZyiRJx24te/TDrEVNhRLeA==")
# login.mail_pwd_login_salesman(mail="wenling_xu@jiliguala.com", pwd="ZyiRJx24te/TDrEVNhRLeA==")
# login.code_login(code="3239", phone="13666666666")
# login.phone_pwd_login(phone="13666666666", pwd="ZyiRJx24te/TDrEVNhRLeA==")
# login.phone_pwd_login_salesman(phone="13666666666", pwd="ZyiRJx24te/TDrEVNhRLeA==")
# login.login_getcode(mail="wenling_xu@jiliguala.com")
# login.getMyInfo(
# authorization="Basic ZDliY2IzM2ZlYzEyNDhlYzg5NjBiZWI0NGEwYTY3YTc6ZmU1Y2FmZGUwNzNjNDhlOGJlZGY2ZDRiMDU4MDY3MTE6OGQ4MGJiYTZmYzkxY2RhYw==")
