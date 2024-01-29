# coding=utf-8
# @Time    : 2021/05/17 2:33 下午
# @Author  : tina_hu
# @File    : ApiDiamondMall
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiDiamondMall:
    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.config.get("url")
        self.root = "/api/diamond"
        self.headers = {
            "version": "1",
            "Content-Type": "application/json",
            "Authorization": auth_token,
            "wechattoken": wechat_token,
        }

    """获取用户积分情况"""

    def api_get_diamondUser(self):
        api_url = "{}/user".format(self.root)
        resp = send_api_request(url=self.host + api_url, method="get", headers=self.headers)
        return resp

    """查询是否完成对应任务"""

    def api_get_missionCheck(self, mission, lesson=None):
        api_url = "{}/user/check".format(self.root)
        body = {"mission": mission, "lesson": lesson}
        resp = send_api_request(
            url=self.host + api_url, paramType="params", paramData=body, method="get", headers=self.headers
        )
        return resp

    """提交兑换订单"""

    def api_put_UserOrder(self, iid, num, comment=None):
        api_url = "{}/user/order".format(self.root)
        body = {"iid": iid, "num": num, "comment": comment}
        url = self.host + api_url
        print("请求地址：%s" % url, "请求头：%s" % self.headers, "请求body:%s" % body)
        resp = send_api_request(url=url, paramType="json", paramData=body, method="put", headers=self.headers)
        return resp

    """查询用户邀请人名单"""

    def api_get_invitees(self, page=None, pageSize=None):
        api_url = "{}/user/invitees".format(self.root)
        body = {"page": page, "pageSize": pageSize}
        resp = send_api_request(
            url=self.host + api_url, paramType="params", paramData=body, method="get", headers=self.headers
        )
        return resp

    """查询用户积分变动列表"""

    def api_get_transactions(self, page=None, pageSize=None):
        api_url = "{}/user/transactions".format(self.root)
        body = {"page": page, "pageSize": pageSize}
        resp = send_api_request(
            url=self.host + api_url, paramType="params", paramData=body, method="get", headers=self.headers
        )
        return resp

    """查询用户订单列表"""

    def api_get_orders(self, page=None, pageSize=None):
        api_url = "{}/user/orders".format(self.root)
        body = {"page": page, "pageSize": pageSize}
        resp = send_api_request(
            url=self.host + api_url, paramType="params", paramData=body, method="get", headers=self.headers
        )
        return resp

    """查询商品列表"""

    def api_get_items(self, page=None, pageSize=None, promoterZoneFlag=None):
        api_url = "{}/market".format(self.root)
        url = self.host + api_url
        print("请求地址：%s" % url, "请求头：%s" % self.headers)
        body = {"page": page, "pageSize": pageSize, "promoterZoneFlag": promoterZoneFlag}
        resp = send_api_request(url=url, paramType="params", paramData=body, method="get", headers=self.headers)
        return resp

    def query_items(self):
        """查询所有的itemid,用于检测自动化购买的item是否存在"""
        result = self.api_get_items(pageSize=100, promoterZoneFlag=0)
        a = []
        for i in result["data"]["list"]:
            a.append(i["iid"])
        print(a)
        return a

    def query_itemBuyNum(self, iid):
        """根据iid查询指定item当前购买次数,钻石价格,库存"""
        result = self.api_get_items(pageSize=100, promoterZoneFlag=0)
        print(result)
        for i in result["data"]["list"]:
            if i["iid"] == iid:
                return i["num"], i["point"], i["store"]
        print("找不到这个item相关信息")

    def query_pointNum(self):
        """查询当前钻石数"""
        result = self.api_get_diamondUser()
        num = result["data"]["point"]
        return num

    def query_itemByType(self, type):
        """根据type查询一个iid"""
        result = self.api_get_items(pageSize=100, promoterZoneFlag=0)
        for i in result["data"]["list"]:
            if i["type"] == type:
                return i["iid"]
        print("找不到type下的iid")


if __name__ == "__main__":
    dm = Domains().set_env_path("fat")
    user11 = UserProperty("19900000001")
    token = user11.basic_auth
    wxtoken = user11.encryptWechatToken
    diamondUser = ApiDiamondMall(token, wxtoken)
    print(diamondUser.headers)
