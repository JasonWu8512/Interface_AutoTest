# coding=utf-8 
# @File     :   ApiPopup
# @Time     :   2021/2/24 3:20 下午
# @Author   :   austin
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPoster(object):

    def __init__(self, token):
        self.root = "/api/xshare/poster"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_poster_multi(self,type,source,pid):
        """
        获取多海报配置(/api/xshare/poster/multi)
        type:渠道
        source：入口
        pid：uid
        """
        api_url = "{}/multi".format(self.root)
        body = {
            "type": type,
            "source": source,
            "pid": pid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_poster_invite(self):
        """
        邀请邀请海报底图(/api/xshare/poster/invite)
        """
        api_url = "{}/invite".format(self.root)
        body = {

        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_poster_progress(self,xid):
        """
        获取课程进度/api/xshare/poster/progress
        xid:为itemid
        """
        api_url = "{}/progress".format(self.root)
        body = {
            "xid":xid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp



if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    token = 'Basic NTA1ZWE3OTU3ZmQ2NDM5NjhmNzYzNDk5MjM2MjFhNmY6N2MyYmJjNTQ0NzIxNDM5Y2FjZmM4MGMzNzAyYzI4NTQ='
    print(ApiPoster(token).api_poster_progress("H5_XX_Sample"))
