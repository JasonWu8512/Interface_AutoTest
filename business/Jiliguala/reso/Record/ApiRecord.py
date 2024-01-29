# coding=utf-8
# @Time    : 2020/8/10 5:19 下午
# @Author  : keith
# @File    : ApiRecord

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiRecord(object):
    """
    自动停止录音配置
    """
    dm = Domains

    def __init__(self, token):
        self.headers = {"Authorization": token, "version": "1"}
        self.host = Domains.domain

    def api_get_record_config(self):
        api_url = "/api/stop/record/config"
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp
