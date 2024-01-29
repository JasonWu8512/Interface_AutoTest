# coding=utf-8
# @Time    : 2021/3/29 5:52 下午
# @Author  : jerry
# @File    : ApiOrder.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.format.format import now_timeStr
from utils.requests.apiRequests import send_api_request


class ApiOrder:
    """订单相关接口"""

    root = "/api/mars/order"

    def __init__(self, wechat_token=None, basic_auth=None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    def api_create_v2(self, item_id, xshare_initiator, sharer, sp2xuIds, nonce, source, gpid=None, gpoid=None):
        """创建订单"""
        api_url = f'{self.host}{self.root}/create/v2'
        body = {
            "itemid": item_id,
            "nonce": nonce,
            "source": source,
            "xshareInitiator": xshare_initiator,
            "sharer": sharer,
            "sp2xuIds": sp2xuIds,
            'gpid':gpid,
            'gpoid':gpoid
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="put", headers=self.headers)
        return resp

    def api_charge_v2(self, channel, oid, pay_wechat_token_typ=None, pay_wechat_token=None, result_url=None):
        """支付订单"""
        api_url = f'{self.host}{self.root}/charge/v2'
        body = {
            "channel": channel,
            "oid": oid,
            "pay_wechat_token_typ": pay_wechat_token_typ,
            "pay_wechat_token": pay_wechat_token,
            "extra": {
                "result_url": result_url
            }
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post", headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_env_path('fat')
    dm.set_domain("https://fat.jiliguala.com")
    token = UserProperty('18362933382').basic_auth
    wechattoken = UserProperty('18362933382').encryptWechatToken_pingpp
    ord = ApiOrder(wechat_token=wechattoken, basic_auth=token)
    res = ord.api_create_v2(item_id='H5_Sample_DiamondActivity', nonce=now_timeStr(), source="AppHomeView",
                            xshare_initiator="793fa8a2cfbe4285a7a60384a040e5df",
                            sharer="793fa8a2cfbe4285a7a60384a040e5df", sp2xuIds=[2143])
    print(res)
    re = ord.api_charge_v2(oid=res['data']['orderNo'], channel='wx_pub', pay_wechat_token_typ="silent",
                           pay_wechat_token=wechattoken)
    print(re)