# coding=utf-8
# @Time    : 2021/02/26 6:33 下午
# @Author  : qilijun
# @File    : ApiWechat
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty
from business.xshare.ApiQrcodeEnum import QrcodeEnum

class ApiWechat:
    """"
    微信账户绑定解绑接口
    """

    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.domain
        self.root = "/api/xshare/wechat"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def api_get_bind_status(self):
        """"
        微信公众号查询绑定状态 from xshare v2.3
        """
        api_url = "{}/bindStatus".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    def api_bind(self, uid):
        """"
        微信公众号绑定叽里呱啦用户 from xshare v2.3
        """
        api_url = "{}/bind".format(self.root)
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body,
                                headers=self.headers)
        return resp

    def api_sbind(self, uid):
        """"
        微信公众号换绑叽里呱啦用户 from xshare v2.3
        """
        api_url = "{}/sbind".format(self.root)
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body,
                                headers=self.headers)
        return resp

    def api_unbind(self, uid):
        """"
        微信公众号解绑定叽里呱啦用户 from xshare v2.3
        """
        api_url = "{}/unbind".format(self.root)
        body = {
            "uid": uid
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body,
                                headers=self.headers)
        return resp

    def api_get_order(self):
        """"
        查询微信系订单状态
        """
        api_url = "{}/order".format(self.root)
        body = {
            "skuList": ["sku99"]
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body,
                                headers=self.headers)
        return resp

    def api_qrcode(self,sceneId,type,uid,appId):
        """"
        微信公众号生成二维码
        appId
        uid:"用户id"
        sceneId:"场景值"
        type:"二维码类型", allowableValues = "TEMP, PERM"
        appId:公众号appId
        """
        api_url = "{}/qrcode".format(self.root)
        body = {
            "sceneId": sceneId,
            "type": type,
            "uid": uid,
            "appId": appId
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body,
                                headers=self.headers)
        return resp

if __name__ == "__main__":
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    up = UserProperty("18900000723", "o0QSN1SyE6JzjNG735dhzIDNqqGw")
    auth_token = up.basic_auth
    userId = up.user_id
    wechat_token = up.encryptWechatToken_bindwechat
    wechat = ApiWechat(auth_token=auth_token)
    # result = wechat.api_get_bind_status()
    # result = wechat.api_bind(userId)
    # result = wechat.api_sbind("655b30ffcc2b425d81ae97ad4535a6d7")
    # result = wechat.api_get_order()
    # result = wechat.api_unbind(userId)
    # result = wechat.api_qrcode("2", 'TEMP', userId, "wx0657a7ec538357ac")
    result = wechat.api_qrcode("2", QrcodeEnum.TEMP.value, userId, "wx0657a7ec538357ac")
    print(result)


