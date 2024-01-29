# coding=utf-8
# @File     :   ApiLottery
# @Time     :   2021/3/4 7:43 下午
# @Author   :   austin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiLottery(object):

    def __init__(self, token):
        self.root = "/api/xshare/lottery"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_order_logistics(self, oid):
        """
        福袋活动查看奖品订单物流信息

        """
        api_url = "{}/order/logistics".format(self.root)
        body = {

            "oid":oid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_lottery_rewardList(self,currentPage,pageSize,activityId):
        """
        福袋活动获取我的奖品列表
        currentPage:页数
        pageSize：一页显示的数量
        activityId：活动id

        """
        header=self.wx_headers.copy()
        header["Content-Type"]="text/plain"
        api_url = "{}/rewardList".format(self.root)
        body = {
            "currentPage":currentPage,
            "pageSize":pageSize,
            "activityId":activityId
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=header)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    token = 'Basic NTA1ZWE3OTU3ZmQ2NDM5NjhmNzYzNDk5MjM2MjFhNmY6N2MyYmJjNTQ0NzIxNDM5Y2FjZmM4MGMzNzAyYzI4NTQ='
    print(ApiLottery(token).api_lottery_rewardList(1,10,10001))
