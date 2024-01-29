# @Time    : 2021/2/4 5:19 下午
# @Author  : ygritte
# @File    : ApiInnerAdmin

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiInnerAdmin:
    """
    InnerAdminController
    """
    root = "/api/inner/saturn"

    def __init__(self, admin_token=None):
        self.host = Domains.get_ggr_host()
        self.headers = {
            "version": "1",
            "Content-Type": "application/json;charset=utf-8",
            "admintoken": admin_token
        }

    def api_admin_account_list(self, page_no, page_size):
        """
        代理商账号列表
        """
        api_url = f'{self.root}/admin/account/list'
        body = {
            "pageNo": page_no,
            "pageSize": page_size
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params",
                                paramData=body, headers=self.headers)
        return resp

    def api_admin_account_phone_registered(self, mobile):
        """
        判断手机号是否已注册
        """
        api_url = f'{self.root}/admin/account/phone/registered'
        body = {
            "mobile": mobile
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params",
                                paramData=body, headers=self.headers)
        return resp

    def api_admin_account_manager_register(self, name, province, city, mobile, pwd):
        """
        代理商账号注册
        """
        api_url = f'{self.root}/admin/account/manager/register'
        body = {
            "name": name,
            "province": province,
            "city": city,
            "mobile": mobile,
            "pwd": pwd
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json",
                                paramData=body, headers=self.headers)

        return resp

    def api_admin_account_employee_register(self, name, mobile, pwd, leaderUuid):
        """
        员工注册
        """
        api_url = f'{self.root}/admin/account/employee/register'
        body = {
            "name": name,
            "mobile": mobile,
            "pwd": pwd,
            "leaderUuid": leaderUuid
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json",
                                paramData=body, headers=self.headers)
        return resp

    def api_admin_account_info(self, uuid):
        """
        账号信息查询
        """
        api_url = f'{self.root}/admin/account/info'
        body = {
            "uuid": uuid

        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params",
                                paramData=body, headers=self.headers)
        return resp

    def api_admin_account_edit(self, uuid, pwd):
        """
        代理商账号修改
        """
        api_url = f'{self.root}/admin/account/edit'
        body = {
            "uuid": uuid,
            "pwd": pwd
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json",
                                paramData=body, headers=self.headers)
        return resp

    def api_admin_inventory_add(self, uuid, quantity, start, end):
        """
        添加库存
        """
        api_url = f'{self.root}/admin/inventory/add'
        body = {
            "uuid": uuid,
            "quantity": quantity,
            "start": start,
            "end": end
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json",
                                paramData=body, headers=self.headers)
        return resp

    def api_admin_inventory_regular_package_list(self):
        """
        可选择库存包列表
        """
        api_url = f'{self.root}/admin/inventory/regular/package/list'
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params",
                                paramData=None, headers=self.headers)
        return resp

    def api_admin_inventory_regular_add(self, uuid, quantity, packageUuid, start, end):
        """
        增加小课包库存(运营管理后台)
        """
        api_url = f'{self.root}/admin/inventory/regular/add'
        body = {
            "uuid": uuid,
            "quantity": quantity,
            "packageUuid": packageUuid,
            "start": start,
            "end": end
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json",
                                paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    ad = ApiInnerAdmin(admin_token="a97bff4e651e4821b28bafedd4d44b20")
    res = ad.api_admin_inventory_regular_add(uuid="abe5aeaae3ab4a99b385f4130f628b16",quantity=1,
                                             packageUuid="0FCFD9A0-8B74-4088-8977-33BD1402BAE1",
                                             start="2021-04-13 00:00:00", end="2021-05-29 23:59:59")
    print(res)



