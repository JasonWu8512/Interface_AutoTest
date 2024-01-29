# coding=utf-8
# @Time    : 2020/8/3 4:11 下午
# @Author  : keith
# @File    : ApiAudio

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAudio(object):
    """
    音频相关
    """

    def __init__(self, token):
        self.headers = {"Authorization": token, "version": "1"}
        self.host = Domains.domain

    def api_get_audios_channel(self):
        api_url = "/api/audios/channel"
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    def api_get_audios_list(self, channel, bid):
        api_url = "/api/audios/list"
        body = {
            "channel": channel,
            "bid": bid
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp
