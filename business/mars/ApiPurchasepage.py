# coding=utf-8
# @Time    : 2021/3/30 3:49 下午
# @Author  : jerry
# @File    : ApiPurchasepage.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPurchasepage:
    """商品详情"""

    root = "/api/mars/purchasepage"

    def __init__(self, wechat_token=None, basic_auth=None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain

    def get_config_v2(self, spu_id=None, spu_tag=None, channel_environment="WxChat", visit_id=None):
        """获取首页配置"""
        api_url = f'{self.host}{self.root}/config/v2'
        body = {
            "spuId": spu_id,
            "spuTag": spu_tag,
            "channel_environment": channel_environment,
            "visitId": visit_id
        }
        resp = send_api_request(url=api_url, method='get', paramType="params", paramData=body, headers=self.headers)
        return resp

    def get_stock_v2(self, spuId=None):
        """获取spu详情"""
        api_url = f'{self.host}{self.root}/stock/v2'
        body = {
            "spuId": spuId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType="params", headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_env_path("fat")
    dm.set_domain("https://fat.jiliguala.com")
    token = UserProperty('18362933382').basic_auth
    wechattoken = UserProperty('18362933382').encryptWechatToken_pingpp
    pur = ApiPurchasepage(wechat_token=wechattoken, basic_auth=token)
    res = pur.get_config_v2()
    re = pur.get_stock_v2(spuId=res['data']['spuId'])
    print(re)
