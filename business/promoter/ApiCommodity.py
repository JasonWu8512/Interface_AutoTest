# coding=utf-8
# @Time    : 2020/12/3 10:29 上午
# @Author  : jerry
# @File    : ApiCommodity.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiCommodity:
    """
    promoter
    CommodityController
    """

    root = "/api/promoter"

    def __init__(self, wechat_token=None, basic_auth = None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    """-------------------------------------CommodityController--------------------------------"""

    def api_main_recommend_commodities(self):
        """
        首页商品推广(已废弃)
        """
        api_url = f'{self.host}{self.root}/main/recommendation/commodities'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_top_recommend_commodities(self):
        """
        主推商品
        """
        api_url = f'{self.host}{self.root}/top/recommendation/commodities'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_commodity_detail(self, id):
        """
        根据spu查询详情
        """
        api_url = f'{self.host}{self.root}/commodity/detail'
        body = {
            "id": id
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    promo = UserProperty('13951782841')
    wechattoken = promo.encryptWechatToken_promoter
    basic = promo.basic_auth
    promoter = ApiCommodity(wechattoken, basic)
    res = promoter.api_commodity_detail("CRM_H5_ST_K1_6_0")
    print(res)