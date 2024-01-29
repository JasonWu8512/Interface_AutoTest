"""
=========
Author:WenLing.xu
time:2022/7/6
=========
"""
from requests import request
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAccount(object):

    def __init__(self, token=None):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "platform": "ios",
            "dev_uni_id": "C264F398 - 4132 - 4162 - BC09 - 8DD21CA8CACC",
            "Accept-Language": "en-us"
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path("fat")["gaga_url"]

    def query_mail(self, mail):
        """查询邮箱使用状态"""
        api_url = "/api/user/query/email/status"
        body = {
            "source": "login",
            "mail": mail
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def query_phone(self, region, phone):
        """查询手机号使用状态"""
        api_url = "/api/user/query/phone/status"
        body = {
            "source": "login",
            "areaCode": region,
            "phone": phone
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def query_level(self, birthdesc, nick):
        """查询推荐等级"""
        api_url = "/api/user/recommend/level"
        body = {
            "birthDesc": birthdesc,
            "babyLevel": 0,
            "nick": nick
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def register_getcode(self, country, countryCode, languageCode, phone01=None, mail=None):
        """注册-发送码验证"""
        api_url = "/api/user/register/send/mail/code"
        body = {
            "birthDesc": "2015-06",
            "areaCode": country,
            "phone": phone01,
            "mail": mail,
            "nick": "宝贝",
            "autoTakeTrialMember": True,
            "source": "register",
            "userRegisterEvent": {
                "deviceType": "ANA-AN00",
                "osVersion": "10",
                "countryCode": countryCode,
                "languageCode": languageCode,
                "deviceManufacturer": "HUAWEI",
                "deviceBrand": "HUAWEI"
            }
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def query_phone_mail(self, country, phone):
        """验证邮箱/手机是否已使用，返回0表示已使用"""
        api_url = "/api/user/validate/mail"
        body = {
            "areaCode": country,
            "phone": phone
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def return_phone_code(self, phone=None, country=None, mail=None):
        """return获取的手机验证码"""
        api_url = "/inner/app/admin/user/query/code"
        body = {
            "email": mail,
            "areaCode": country,
            "phone": phone
        }
        code_url =self.dm.set_env_path("fat")["code_url"]
        resp = send_api_request(url=code_url + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp["data"]["code"])
        return resp["data"]["code"]

        # api_url = "/api/user/debug/redis/get?key=user%3Aregister%3Aphone%3A{0}%3A{1}".format(country, phone)
        # resp = request(url=self.host + api_url, method="get", headers=self.headers)
        # print(resp.json())
        # print("验证码：" + resp.json[-1]["code"])
        # return resp.json()[-1]["code"]

        # def return_mail_code(self, mail):
        """return获取的邮箱验证码"""
        # api_url = "/api/user/debug/redis/get?key=user:register:{0}".format(mail)
        # print(self.host + api_url)
        # resp = request(url=self.host + api_url, method="get", headers=self.headers)
        # print("验证码：" + resp.text)
        # return resp.text

    def send_code(self, country, phone):
        """忘记密码第1步-发送验证码"""
        api_url = "/api/user/forget/send/mail/code"
        body = {
            "areaCode": country,
            "phone": phone,
            "source": "forgot_password"
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def validate(self, country, phone02, code):
        """忘记密码第2步-验证验证码"""
        api_url = "/api/user/forget/validate"
        body = {
            "areaCode": country,
            "phone": phone02,
            "code": code
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def reset_password(self, password, confirmpassword, token, password01, confirmpassword01, **gk):
        """忘记密码第3步-重置密码"""
        api_url = "/api/user/forget/reset/password"
        body = {
            "password": password,
            "confirmPassword": confirmpassword,
            "token": token
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        if resp["code"] == 0:
            print(body)
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

    def close_account(self, token):
        """销户"""
        api_url = "/api/user/close/account"
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "platform": "ios",
            "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC"
        }
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=headers)
        print(resp)
        return resp

    def register_validate(self, country, countryCode, languageCode, code, phone):
        """注册-验证验证码"""
        api_url = "/api/user/register/validate"
        body = {
            "code": code,
            "areaCode": country,
            "phone": phone,
            "userRegisterEvent": {
                "deviceType": "iPhone13,2",
                "osVersion": "15.5",
                "countryCode": countryCode,
                "languageCode": languageCode,
                "deviceManufacturer": "Apple",
                "deviceBrand": "iOS"
            },
            "autoTakeTrialMember": True
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def bind_send_code(self, mail=None, areaCode=None, phone=None):
        """绑定-发送手机/邮箱验证码"""
        api_url = "/api/user/bind/send/code"
        body = {
            "phone": phone,
            "areaCode": areaCode,
            "mail": mail,
            "source": ""
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def set_password(self, password, confirmPassword, auth):
        """设置密码"""
        api_url = "/api/user/register/set/password"
        body = {"password": password,
                "confirmPassword": confirmPassword
                }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": auth,
            "Host": "fat.jiligaga.com",
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=headers)
        print(resp)
        return resp

    def bind_phonemail_validate_code(self, code, auth, phone=None, mail=None, areaCode=None):
        """
        验证code-绑定手机/邮箱
        """
        api_url = "/api/user/validate/code/to/bind"
        body = {"areaCode": areaCode,
                "phone": phone,
                "mail": mail,
                "code": code
                }
        print(body)
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": auth,
            "appversion": "1.10.0",
            "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC"
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=headers)
        print(resp)
        return resp

# if __name__ == '__main__':
#     apiaccount = ApiAccount()
#     apiaccount.return_phone_code(phone="123456789", country="886")
#     apiaccount.return_mail_code(mail="ling@jiliguala.com")
#     apiaccount.query_mail(mail="wenling_xu@jiliguala.com")
#     apiaccount.query_phone(region="86", phone="13666666666")
#     apiaccount.query_level(birthdesc="2015-06", nick="宝贝")
#     apiaccount.register_getcode(phone01="17777777777")
#     apiaccount.query_phone_mail(phone="13666666666")
#     apiaccount.send_code(phone="13666666666")
#     apiaccount.validate(phone02="13666666666", code="4554")
#     apiaccount.reset_password(password="xu123456", confirmpassword="xu123456", password01="xu1234567",
#                          confirmpassword01="xu1234567",
#                          token="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJwaG9uZSIsInN1YiI6IntcImFyZWFDb2RlXCI6XCI4NlwiLFwicGhvbmVcIjpcIjE4ODg4ODg4ODg4XCJ9IiwiaXNzIjoidXNlciIsImlhdCI6MTY1ODIwNzkwNiwiZXhwIjoxNjU4MjA4NTA2fQ.3oMdJbp2fmVoe0A3sOVeA4TtngxUGKmMFdUKxqJR69s")
#     apiaccount.close_account( token ="Basic Y2Y3MTRmOGY1NWE3NDMwMGJlOTJlY2ExMGE3OWIyMTg6MGQ5ODY2ODI2NzkyNGQ3NWFjYjRiMWI2MGYzY2Y5MWI6QzI2NEYzOTgtNDEzMi00MTYyLUJDMDktOEREMjFDQThDQUND")
#     apiaccount.register_validate(code="1949", phone="1322222222")
#     apiaccount.bind_send_code(mail="13111111111@163.com")
#     apiaccount.bind_send_code(phone="13111111111", areaCode="86")
#     apiaccount.set_password(auth="Basic MmI4YTVmZTdlMTY3NDFhNTljOWNlYzVkNTNhMjk2MWY6NjIyNTc0MTg4ODNiNDY3ZTljN2FjY2Q2MGRlMjNkNzI6QzI2NEYzOTgtNDEzMi00MTYyLUJDMDktOEREMjFDQThDQUND",
#                         password="c4lZZJrYf9ZR0jf9n7PETg==", confirmPassword="c4lZZJrYf9ZR0jf9n7PETg==")
