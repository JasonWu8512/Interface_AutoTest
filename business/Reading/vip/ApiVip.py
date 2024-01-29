# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty
from business.Reading.user.ApiUser import ApiUser
import copy


class ApiVip(object):
    """
    用户的vip信息
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def api_get_vip(self):
        """
        获取vip信息
        """
        api_url = "/api/vip"
        body = {}
        # GGV2="apJKXtHSKN6VdDh0Bq56Shaq6C/vlIWdf2GOUq7CbV5UzS3mY48yi9WlP6WPFmL90bCA9pQtildDEydi0iMB3YmYthOsR4/xZX+y90zTuX6YVvm4qTHy0ZB45AKnu60yfrUIw8EptP1CBUI+x+6ZPK2JhTQM2HJk9Q7eaZv+ASU0Gg=="
        # header = copy.deepcopy(self.headers)
        # header['GGHeader-V2'] = GGV2
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_get_v2_vip_purchase(self):
        """
        新购买页，允许多个 SKU
        """
        api_url = "/api/v2/vip/purchase"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_vip_trial(self, mobile, code, channel, skuId):
        """
        站外领取VIP
        :param mobile:手机号
        :param code:验证码
        :param channel:
        :param skuId:
        """
        api_url = "/api/vip/trial"
        body = {
            "mobile": mobile,
            "code": code,
            "channel": channel,
            "skuId": skuId
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp

    def api_get_user_sms_logout(self, mobile, type='text'):
        """
        发送手机验证码
        """
        api_url = "/api/user/sms_logout"
        body = {"mobile": mobile,
                type: type
                }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_delete_user(self, typ, u, p):
        """
        注销
        """
        api_url = "/api/user"
        body = {"typ": typ,
                "u": u,
                "p": p
                }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="delete",
                                headers=self.headers)
        return resp

    def api_vip_entrance(self):
        """ 词句库页面vip购买页入口 """
        api_url = "/api/vip/entrance"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp



if __name__ == '__main__':

    dm = Domains()
    dm.set_env_path('dev')
    dm.set_domain("https://devggr.jiliguala.com")
    # 发送验证码
    u = ApiUser()
    mobile = '13162592038'
    u.api_get_user_sms(mobile)
    # code
    db_user = u.get_jlgl_user(mobile)
    code = db_user['sms']['code']

    user = UserProperty(mobile)
    token = user.basic_auth
    vip = ApiVip(token=token)
    res = vip.api_vip_trial(mobile, code, "DetailShareBook", "ReadingVIPFree_7_Share")

    # 注销
    vip.api_get_user_sms_logout(mobile)
    db_user = u.get_jlgl_user(mobile)
    code = db_user['sms']['code']
    print(code)

    r = vip.api_delete_user('mobilecode', mobile, code)
    print(res)