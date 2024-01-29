# coding=utf-8
# @Time    : 2020/8/12 4:07 下午
# @Author  : keith
# @File    : ApiUserInfo

from business.businessQuery import usersQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiUserInfo(object):
    """
    用户信息
    """

    def __init__(self, token=None):
        self.headers = {"Authorization": token, "version": "1"}
        self.host = Domains.domain
        # self.host = "http://gateway-fat.jlgltech.com"

    # 发送短信验证码
    def api_get_sms(self, target):
        """
        :param target: 手机号
        :return:
        """
        api_url = "/api/sms/password"
        body = {
            "target": target,
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get")
        return resp

    def api_get_websms(self, mobile):
        """
        获取验证码/注册
        """
        api_url = "/api/web/sms"
        body = {"mobile": mobile, "source": "Test", "crm_source": "sampleH5"}
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body)
        return resp

    # 获取用户信息
    def api_get_users(self, _id):
        """
        :param _id:
        :return:
        """
        api_url = "/api/users"
        body = {"_id": _id}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get")
        return resp

    # 编辑瓜豆
    def api_manage_guadou(self, guaid, guadouBalance):
        """
        :param guaid: gua
        :param guadouBalance:
        :return:
        """
        api_url = "/api/backend/users/guadoumanager"
        body = {
            "data": [
                {
                    "guaid": guaid,
                    "guadouBalance": guadouBalance,
                }
            ]
        }
        resp = send_api_request(
            url=self.host + api_url, paramType="json", paramData=body, method="post", headers=self.headers
        )
        return resp

    # 用户中心
    def api_get_user_center(self, bid, id, level):
        # https://dev.jiliguala.com/api/user/center?bid=e712fc6a6a614d868788721febadef26&id=dd093b38dd56458a853a3f772974f783&level=L1XX&nonce=5B2292A8-1D6B-42D1-9204-8044124AC2B8
        api_url = "/api/user/center"
        data = {"bid": bid, "id": id, "level": level}
        resp = send_api_request(
            url=self.host + api_url, paramType="params", paramData=data, method="get", headers=self.headers
        )
        return resp

    def api_sms_logout(self):
        """
        注销账号第一步，发送验证码
        """
        api_url = "/api/user/sms_logout"
        body = {"type": "text HTTP/1.1"}
        resp = send_api_request(
            url=self.host + api_url, paramType="params", paramData=body, method="get", headers=self.headers
        )
        return resp

    def api_users_security_info(self, mobile, smsCode):
        """
        注销账号第二步，真正注销
        """
        api_url = "/api/users/security/info"
        body = {"mobile": mobile, "smsCode": smsCode}
        resp = send_api_request(
            url=self.host + api_url, paramType="params", paramData=body, method="delete", headers=self.headers
        )
        return resp


if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path(env="fat")
    dm.set_domain(config["url"])
    # token = ''
    # print(ApiUserInfo('').api_get_websms('18717877715'))
    # user = UserProperty("19919999999")
    # auth_token = user.basic_auth
    # ApiUserInfo(auth_token).api_sms_logout()
    # smsCode = usersQuery().get_users(mobile="19919999999")["sms"]["code"]
    # ApiUserInfo(auth_token).api_users_security_info(mobile="19919999999",smsCode=smsCode)
    ApiUserInfo().api_get_websms("19919999999")
    user = UserProperty("19919999999")
    auth_token = user.basic_auth
    ApiUserInfo(auth_token).api_sms_logout()
    smsCode = usersQuery().get_users(mobile="19919999999")["sms"]["code"]
    print(smsCode)
    ApiUserInfo(auth_token).api_users_security_info(mobile="19919999999", smsCode=smsCode)
