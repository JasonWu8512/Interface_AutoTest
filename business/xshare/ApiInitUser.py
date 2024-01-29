from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiInitUser:
    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.config.get("url")
        self.headers = {
            "version": "1",
            "Content-Type": "application/json",
            "Authorization": auth_token,
            "wechattoken": wechat_token,
        }

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
