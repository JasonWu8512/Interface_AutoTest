# coding=utf-8
# @Time    : 2020/12/3 11:17 上午
# @Author  : jerry
# @File    : ApiPromoterRecordReporter.py

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApipromoterRecordReporter:
    """
    promoter
    PromoterRecordReporterController
    """
    root = "/api/promoter"

    def __init__(self, wechat_token=None, basic_auth=None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth, "User-Agent": ""}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    """-------------------------------------PromoterRecordReporterController--------------------------------"""

    def api_promoter_reporter(self, itemid, promoterid):
        """
        新增主推商品的推广记录
        """
        api_url = f'{self.host}{self.root}/record/reporter'
        body = {
            "itemid": itemid,
            "promoterId": promoterid
        }
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=self.headers)
        return resp