# coding=utf-8 
# @File     :   ApiHMall
# @Time     :   2021/2/28 6:46 下午
# @Author   :   austin


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiHMall(object):

    def __init__(self, token):
        self.root = "/api/xshare/hmall"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"wechattoken": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_hmall_inviter(self,):
        """
        查询当前用户的邀请人信息，目前包括微信头像和昵称

        """
        api_url = "{}/inviter/info".format(self.root)

        resp = send_api_request(url=self.host + api_url, paramType='params',  method="get",
                                headers=self.wx_headers)
        return resp

    def api_hmall_fpromoter(self,initiator,xid):
        """
        h5商城获取firstPromoterId
        "initiator":邀请人uid
        "xid":为itemid
        """
        api_url = "{}/fpromoter".format(self.root)
        body={
            "initiator":initiator,
            "xid":xid
        }

        resp = send_api_request(url=self.host + api_url, paramType='params',paramData=body,  method="get",
                                headers=self.wx_headers)
        return resp

    def api_hmall_stock(self,itemid,initiator):
        """
        商城页进入时查询9.9库存
        没调通
        """
        api_url = "{}/stock".format(self.root)
        body={
            "itemid":itemid,
            "initiator":initiator,
        }

        resp = send_api_request(url=self.host + api_url, paramType='params',paramData=body, method="get",
                                headers=self.wx_headers)
        print(self.host + api_url)
        return resp

    def api_hmall_ggshare_subcheck(self,unionId):
        """
        9.9二维码页面退出时查询是否关注过呱呱爱分享公众号

        """
        api_url = "{}/ggshare/subcheck".format(self.root)
        body={
            "unionId":unionId,
        }

        resp = send_api_request(url=self.host + api_url, paramType='json',paramData=body,  method="post",
                                headers=self.wx_headers)
        return resp

    def api_hmall_order_logistics(self):
        """
        查询当前用户物流订单信息

        """
        api_url = "{}/order/logistics".format(self.root)

        resp = send_api_request(url=self.host + api_url, paramType='params',method="get",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
