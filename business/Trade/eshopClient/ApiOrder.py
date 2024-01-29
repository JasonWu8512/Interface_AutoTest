# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 2:48 下午
# @Author  : zoey
# @File    : ApiOrder.py
# @Software: PyCharm


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from utils.format.format import now_timeStr
from business.Trade.eshopClient.ApiOrders import ApiOrders
from business.common.UserProperty import UserProperty


class ApiOrder:
    """
    eshop 商城微信C端 - 订单相关,need wechat login
    OrderController
    """

    def __init__(self, wechat_token=None, token=None):
        self.host = Domains.domain
        self.root = '/api/eshop'
        self.headers = {'Authorization': token, "wechattoken": wechat_token, "Content-Type": "application/json"}

    def api_create_order(self, account, wechatToken, itemId, promoterId=None, nonce=now_timeStr(), promotionId=None, groupId='', quantity=1,
                         name='zoey', tel='13951782841', addr="1号楼", region='上海市 上海市 黄浦区'):
        """
        下单接口
        :param account:
        :param wechatToken:
        :param itemId: 商品id
        :param promoterId:
        :param promotionId:活动id
        :param groupId:团单id
        :param quantity:购买数量
        :param name:收货人姓名
        :param tel:收货人手机号
        :param addr: 收货地址
        :param region: 收货城市
        :return:
        """
        api_url = f'{self.host}{self.root}/order'
        body = {
            "itemid": itemId,
            "receiver": {
                "name": name,
                "tel": tel,
                "addr": addr,
                "region": region
            },
            "nonce": nonce,
            "promoterId": promoterId,
            "promotionId": promotionId,
            "groupId": groupId,
            "account": account,
            "typ": "unsilent",
            "wechat_token": wechatToken,
            "quantity": quantity
        }
        print(self.headers)
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json', headers=self.headers)
        return resp

    def api_get_order_status(self, oid):
        """
        查询订单状态
        :param oid: 订单id
        :return:
        """
        api_url = f'{self.host}{self.root}/order/status'
        body = {"oid": oid}
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    # wechattoken = "z7VOzHVUQIiijnGZstM1otrA6LTyw7PF3ixYSpELpIJo/PDy1RqIMIqAOLczJIdrPPEDq+plzMqayHtiVYQ8V9Jh0W8QR3LE+xxNltDHtZ91gEIJ/8mNKnbVN7TKVsfbvtzqzI7C7dogAJ9h58wMHeLHBDV7sGWmdHlDrGDWwgZ0wIkD53LJda9D527+DEKnAPL1197ifCoJehkV0cwOlLCKL4dSOpxhx59LkLs89GhsPAmtYfAzAeu/MkuNj7cswsjcxqO4z7XVAGZ01mi7sgbySjd0fwV2qXHOSQ+610jOxqGRpEwHTCwKy5h7Exqo82r+JPzKiEtrMt/Evgi5wpnLCBZ4W64GnhYxfUy3MRis"
    user = UserProperty('15996244603')
    wechattoken = user.encryptWechatToken
    # eshop_basic_auth = "Basic MTlkZWJkZDU3YmZhNGI0MThiNTg5YTEwNWI1NjA3ZmE6N2JjZGFhOWQ3MjI4NDI3MGFjZTlmYTAwNTk0YzNkYzU="
    eshop_basic_auth = user.basic_auth
    order = ApiOrder(wechattoken, eshop_basic_auth)
    orders = ApiOrders(wechattoken, eshop_basic_auth)
    res = order.api_create_order(account="wxd388f6f520772446", wechatToken=wechattoken, itemId="CRM_H5_L0XX", promoterId="JLGL_DP_12063")
    print(res)
    charge_res = orders.api_charge(oid=res["data"]["id"], guadouDiscount=res["data"]["amount"], payWechatToken=wechattoken)
    print(charge_res)