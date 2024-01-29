"""
=========
Author:WenLing.xu
time:2022/09/13
=========
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAccountV3(object):
    def __init__(self, token=None):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "platform": "ios",
            "dev_uni_id": "C264F398 - 4132 - 4162 - BC09 - 8DD21CA8CACC"
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path("fat")["gaga_url"]

    def create_account(self, countryCode):
        """
        创建游客账户
        """
        api_url = "/api/user/v3/create/account"
        body = {
            "userRegisterEvent": {
                "deviceType": "ANA-AN00",
                "osVersion": "10",
                "countryCode": countryCode,
                "deviceManufacturer": "HUAWEI",
                "deviceBrand": "HUAWEI"
            }
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def login_password(self, phone, pwd, countrycode):
        """
        密码登录/注册
        """
        api_url = "/api/user/v3/login/password"
        body = {
            "countryCode": countrycode,
            "account": phone,
            "password": pwd,
            "source": "log_out",
            "deviceType": "ANA-AN00"
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(body)
        print(resp)
        return resp

    def login_send_code(self, account, countrycode):
        """
        验证码登录/注册-发送验证码（邮箱或手机）
        """
        api_url = "/api/user/v3/login/send/code"
        body = {
            "countryCode": countrycode,
            "account": account,
            "source": "login"
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def login_validate_code(self, account, code, countrycode):
        """
        验证码登录-校验验证码
        """
        api_url = "/api/user/v3/login/validate/code"
        body = {
            "code": code,
            "countryCode": countrycode,
            "account": account,
            "deviceType": "ANA-AN00"
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def forget_send_code(self, account, countrycode):
        """
        忘记密码第1步-发送验证码
        """
        api_url = "/api/user/v3/h5/forget/send/code"
        body = {"countryCode": countrycode,
                "account": account,
                "source": "forgot_password"
                }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def forget_validate_code(self, account, code, countrycode):
        """
        忘记密码第2步-验证验证码
        """
        api_url = "/api/user/v3/h5/forget/validate"
        body = {"countryCode": countrycode,
                "account": account,
                "code": code
                }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def forget_reset_password(self, token, password=None, confirmpassword=None, password01=None,
                              confirmpassword01=None):
        """
        忘记密码第3步-重置密码
        """
        api_url = "/api/user/v3/h5/forget/reset/password"
        body = {"password": password, "confirmPassword": confirmpassword,
                "token": token}
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        if resp["code"] == 0:
            print(resp)
            return resp
        else:
            body = {
                "password": password01,
                "confirmPassword": confirmpassword01,
                "token": token
            }
            resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                    headers=self.headers)
            print(resp)
            return resp

    def close_user(self):
        """
        注销账号
        """
        api_url = "/api/user/close/account"
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=None, method="post",
                                headers=self.headers)
        print(self.headers)
        print(resp)
        return resp

# if __name__ == '__main__':
#     api = ApiAccountV3()
#     api.close_user()
# api.create_account()
# api.login_password(phone="13666666666", pwd="ZyiRJx24te/TDrEVNhRLeA==")
# api.login_send_code(phone="13552532363")
# api.forget_send_code(account="13552532363")

