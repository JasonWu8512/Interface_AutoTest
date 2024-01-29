# coding=utf-8
# @Time    : 2021/02/24 6:33 下午
# @Author  : qilijun
# @File    : ApiActivity
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty
from business.xshare.ApiBannerDiamondEnum import BannerDiamondEnum

class ApiActivity:
    """"
    年度报告活动接口
    """
    def __init__(self,auth_token=None,wechat_token=None):
        self.host = Domains.domain
        self.root = "/api/xshare/activity"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def api_get_annualReport_by_user(self):
        """"
            查询用户年度报告接口
        """
        api_url = "{}/annualReportByUser".format(self.root)
        resp = send_api_request(url=self.host+api_url, method="get", headers=self.headers)
        return resp

    def api_get_annualReport_by_all(self):
        """"
            查询全体用户年度报告接口
        """
        api_url = "{}/annualReportByAll".format(self.root)
        resp = send_api_request(url=self.host+api_url, method="get", headers=self.headers)
        return resp

    def api_get_annualReport_anyone_by_user(self,userId):
        """"
            匿名查询用户年度报告限量数据接口
        """
        api_url = "{}/annualReportAnyoneByUser".format(self.root)
        body = {
            "uid": userId
        }
        resp = send_api_request(url=self.host+api_url, method="get", paramType="params", paramData=body, headers=self.headers)
        return resp

    def api_banner_diamond(self,activityId):
        """"
            进入钻石商城首页调用
            :param activityId: 枚举 CASHBACK|DIAMOND|GP|REPORT
        """
        api_url = "{}/banner/diamond".format(self.root)
        body = {
            "activityId": activityId
        }
        resp = send_api_request(url=self.host+api_url, method="get", paramType="params", paramData=body, headers=self.headers)
        return resp

    def api_offline_status(self):

        api_url = "{}/offline/status".format(self.root)
        resp = send_api_request(url=self.host+api_url, method="get", headers=self.headers)
        return resp

    def api_status(self):
        """"
            国庆购买页面时间判断接口
        """
        api_url = "{}/status".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

if __name__ == "__main__":
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    up = UserProperty("18900000314")
    auth_token = up.basic_auth
    user_id = up.user_id
    activity = ApiActivity(auth_token)
    # result = activity.api_get_annualreport_by_user()
    # result = activity.api_get_annualReport_by_all()
    # result = activity.api_get_annualReport_anyone_by_user(user_id)
    result = activity.api_banner_diamond(BannerDiamondEnum.DIAMOND.value)
    # result = activity.api_banner_diamond("DIAMOND")
    # result = activity.api_offline_status()
    # result = activity.api_status()
    print(result)