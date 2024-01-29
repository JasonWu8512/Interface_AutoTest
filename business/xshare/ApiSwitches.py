# coding=utf-8
# @Time    : 2020/9/10 1:50 下午
# @Author  : keith
# @File    : Switches


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSwitches(object):
    """
    转介绍-售卖开关
    """

    def __init__(self, auth_token=None):
        self.headers = {"Authorization": auth_token, "version": "1"}
        self.wx_headers = {"Authorization": auth_token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain
        self.root = "/api/xshare/switches"

    def api_get_switches_mode(self, platform):
        """
        获取售卖模式
        :param platform: 枚举 minimall|h5|fakegroup|outside
        :return:
        """
        api_url = "{}/mode".format(self.root)
        body = {
            "platform": platform
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

if __name__ == "__main__":
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    switch = ApiSwitches()
    result = switch.api_get_switches_mode("outside")
    print(result)