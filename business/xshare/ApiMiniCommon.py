# coding=utf-8
# @Time    : 2021/03/09 6:33 下午
# @Author  : qilijun
# @File    : ApiWechat
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiMiniCommon:
    """"
    转介绍-小程序公用-api
    """
    def __init__(self, auth_token=None, wechat_token=None):
        """
        前端调用接口为：/api/openapp/login，转发到/api/xshare/mini/common/login接口
        """
        self.host = Domains.domain
        self.root ="/api/xshare/mini/common/login"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def api_openapp_login(self):
        """
        小程序登录
        jlglOpenapp：前端根据环境写死
        dev:wx18f8075163853984||fat:wx18f8075163853984||rc:wx8f94c312514f740e||prod:wx8f94c312514f740e
        opencode：需要调用wx.login获取（封装在前端SDK）
        """
        api_url = "/api/openapp/login"
        body = {
            "jlglOpenapp": "wx18f8075163853984",
            "opencode": "043Vzd100d3tiL1qFn200psfZt1Vzd11"
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params", paramData=body,
                                headers=self.headers)
        return resp

if __name__ =="__main__":
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    miniCommon = ApiMiniCommon()
