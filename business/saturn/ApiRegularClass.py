# @Time    : 2021/4/13 3:55 下午
# @Author  : ygritte
# @File    : ApiRegularClass

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiRegularClass:
    """
    RegularClassController
    """
    root = "/api/saturn/channel/admin/regular"

    def __init__(self, admintoken):
        self.host = Domains.get_ggr_host()
        self.headers = {
            "version": "1",
            "Content-Type": "application/json;charset=utf-8",
            "admintoken": admintoken
        }

    def api_level_list(self):
        """
        获取可开通小课包的列表
        """
        api_url = f'{self.root}/level/list'
        res = send_api_request(url=self.host + api_url, method="get",
                               paramData=None, paramType="params", headers=self.headers)
        return res

    def api_inventory_info(self):
        """
        获取当前代理的库存信息
        """
        api_url = f'{self.root}/inventory/info'
        res = send_api_request(url=self.host + api_url, method="get",
                               paramData=None, paramType="params", headers=self.headers)
        return res

    def api_open_list(self, pageNo=1, pageSize=20):
        """
        获取已开通小课包的用户列表
        """
        api_url = f'{self.root}/open/list'
        body = {
            "pageNo": pageNo,
            "pageSize": pageSize
        }
        res = send_api_request(url=self.host + api_url, method="get",
                               paramData=body, paramType="params", headers=self.headers)
        return res

    def api_open(self, mobile, levelUuid):
        """
        开通小课包接口
        """
        api_url = f'{self.root}/open'
        body ={
            "mobile": mobile,
            "levelUuid": levelUuid
        }
        res = send_api_request(url=self.host + api_url, method="post", paramType="json",
                               paramData=body, headers=self.headers)
        return res


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    rc = ApiRegularClass(admintoken="5116998a89914d158f23cd5b92b064a4")
    resp = rc.api_open(mobile="17777788888", levelUuid="1095DC61-0509-48FB-A9F4-4806A50C69E4")
    print(resp)
