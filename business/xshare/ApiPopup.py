# coding=utf-8 
# @File     :   ApiPopup
# @Time     :   2021/3/22 2:27 下午
# @Author   :   austin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPopup(object):

    def __init__(self, token):
        self.root = "/api/xshare"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_popupreport(self,initiator,xid,popup):
        """
        转介绍弹窗上报接口
        initiator:邀请人id
        xid：itemid
        popup：
        """
        api_url = "{}/popupreport".format(self.root)
        body = {
            "initiator": initiator,
            "xid": xid,
            "popup": popup
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp

    def api_popup_showed(self,initiator,popup):
        """
        判断这个用户是否看过特定弹窗
        """
        api_url = "{}/popup/showed".format(self.root)
        body = {
            "initiator":initiator,
            "popup":popup

        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_inviter_fisrtpop(self):
        """
        用户是否需要显示首邀弹窗

        """
        api_url = "{}/inviter/fisrtpop".format(self.root)
        body = {
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    token = 'Basic NTA1ZWE3OTU3ZmQ2NDM5NjhmNzYzNDk5MjM2MjFhNmY6N2MyYmJjNTQ0NzIxNDM5Y2FjZmM4MGMzNzAyYzI4NTQ='
    print(ApiPopup(token).api_inviter_fisrtpop())
