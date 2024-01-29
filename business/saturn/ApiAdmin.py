# @Time    : 2021/4/7 4:37 下午
# @Author  : ygritte
# @File    : ApiAdmin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAdmin:
    """
    AdminController
    """
    root = "/channel/admin"

    def __init__(self):
        self.host = Domains.domain
        self.headers = {
            "version": "1",
            "Content-Type": "application/json;charset=utf-8"
        }

    def api_order_sync(self, orderId):
        """
        同步已锁粉用户购买正价课订单
        """
        api_url = f'{self.root}/order/sync'
        body = {"orderId": orderId}
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("http://10.10.78.122:60266")
    admin = ApiAdmin()
    res = admin.api_order_sync("O39175377343746048")
    print(res)