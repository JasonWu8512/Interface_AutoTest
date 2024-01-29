# -*- coding: utf-8 -*-
# @Time: 2021/2/26 6:39 下午
# @Author: qilijun
# @File: ApiIncome
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiIncome(object):
    """
    转介绍收入页相关接口
    """

    def __init__(self, wechat_token=None, authtoken=None):
        self.host = Domains.domain
        self.root = "/api/xshare/income"
        self.headers = {"version": "1",
                        "Content-Type": "application/json", "Authorization": authtoken, "wechattoken": wechat_token}

    def api_get_xshare_income_home(self):
        """
        收入页首页接口
        """
        api_url = "{}/home".format(self.root)
        body = {
            "xid": "H5_Cashback",
            "page": "XshareIncome"
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramData=body, paramType="params",
                                headers=self.headers)
        return resp

    def api_get_xshare_income_detail(self, userId):
        """
        收入明细接口
        """
        api_url = "{}/detail".format(self.root)
        body = {
            "xid": "H5_Cashback",
            "initiator": userId

        }
        resp = send_api_request(url=self.host + api_url, method="get", paramData=body, paramType="params",
                                headers=self.headers)
        return resp

    def api_xshare_income_checkout(self,userId,amout):
        """
        收入页提现接口
        @params:
            initiator :用户ID
            amount：提现金额
        """
        api_url = "{}/checkout".format(self.root)
        body = {
            "xid": "H5_Cashback",
            "initiator": userId,
            "amount": amout
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramData=body, paramType="json",
                                headers=self.headers)
        return resp

if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://fat.jiliguala.com")
    user = UserProperty(mobile="18900000805")
    user_id = user.user_id
    auth = user.basic_auth
    test = ApiIncome(authtoken=auth)
    res = test.api_get_xshare_income_home()
    # res = test.api_get_xshare_income_detail(user_id)
    # res = test.api_xshare_income_checkout(userId=user_id, amout=500)

    print(res)
