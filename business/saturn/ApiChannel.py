# coding=utf-8
# @Time    : 2021/1/25 3:32 下午
# @Author  : jerry
# @File    : ApiChannel.py
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiChannel:
    """ChannelApiController"""

    root = "/api/saturn/channel"

    def __init__(self, token=None, authorization=None):
        self.host = Domains.get_ggr_host()
        self.login_headers = {"version": "1", "Content-Type": "application/json"}
        self.headers = {"admintoken": token, "version": "1", "Content-Type": "application/json","Authorization": authorization}

    def api_admin_login(self, username, password):
        """用户登陆"""
        api_url = f"{self.host}{self.root}/admin/login"
        body = {
            "username": username,
            "password": password

        }
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=self.login_headers)
        return resp

    def api_employee_list(self, page_no, page_size):
        """员工列表"""
        api_url = f'{self.host}{self.root}/admin/employee/list'
        body = {
            "pageNo": page_no,
            "pageSize": page_size
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_employee_fans(self, page_no=1, page_size=20, account_id=None, buy_status=None, mobile=None):
        """线索管理"""
        api_url = f'{self.host}{self.root}/admin/employee/fans'
        body = {
            "pageNo": page_no,
            "pageSize": page_size,
            "accountId": account_id,
            "buyStatus": buy_status,
            "mobile": mobile
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_bind(self, channel):
        """下沉渠道用户锁粉"""
        api_url = f'{self.host}{self.root}/bind'
        body = {
            "channel": channel
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_achievement_monthly_query(self, month):
        """业绩查询"""
        api_url = f'{self.host}{self.root}/admin/achievement/monthly/query'
        body = {
            "month": month
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp


if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path("dev")
    dm.set_domain("https://dev.jiliguala.com")
    # user = UserProperty("17777666666")
    channel = ApiChannel(token="020bb90f4a784ce2840fd455f7874488")
    re = channel.api_achievement_monthly_query("2021-04")
    print(re)
    dic = re['data']['list']
    print(dic)
    # li.sort(key=lambda x: x['lockTime'], reverse=True)
