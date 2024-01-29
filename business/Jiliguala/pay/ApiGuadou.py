# coding=utf-8
# @Time    : 2020/8/11 6:16 下午
# @Author  : keith
# @File    : ApiGuadou

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGuadou(object):
    """
    音频相关
    """

    def __init__(self, token):
        self.headers = {"Authorization": token, "version": "1"}
        self.host = Domains.domain

    def api_get_audios_channel(self, itemid, fields, ):
        api_url = "/api/guadou/state"
        body = {
            "itemid": itemid,
            "fields": fields,
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp
