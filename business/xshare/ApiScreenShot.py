# -*- coding: utf-8 -*-
# @Time    : 2021/02/09 6:55 下午
# @Author  : qilijun
# @File    : ApiScreenShot.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiScreenShot:

    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.domain
        self.root = "/api/xshare"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def api_config(self):
        """
        查询上传截图活动配置接口
        """
        api_url = "{}/screenshot/config".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    def api_check(self):
        """
        查询用户是否具有参加活动的资格
        """
        api_url = "{}/screenshot/check".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    def api_weekly(self):
        """
        查询本周上传截图记录接口
        """
        api_url = "{}/screenshot/weekly".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    def api_history(self):
        """
        查询历史上传截图记录接口
        """
        api_url = "{}/screenshot/history".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    def api_screenshot(self):
        """
        上传截图接口
        """
        api_url = "{}/screenshot".format(self.root)
        body = {
            "url": "https://qiniucdn.jiliguala.com/dev/upload/aedb0f7eac7c492e91fc65bac32c2fc4_20210209033335.jpeg",
            "source": "VIP_Menu"
        }

        resp = send_api_request(url=self.host + api_url, method="post", paramData=body, paramType="json", headers=self.headers)
        return resp



if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    up = UserProperty("18900000314")
    auth_token = up.basic_auth
    wechat_token = up.encryptWechatToken_pingpp
    screen_shot = ApiScreenShot(auth_token, wechat_token)
    result = screen_shot.api_history()
    print(result)
