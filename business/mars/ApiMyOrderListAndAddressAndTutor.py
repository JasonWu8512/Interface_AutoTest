# coding=utf-8
# @Time    : 2021/04/01
# @Author  : jing_zhang
# @File    : ApiMyOrderListAndAddressAndTutor.py
# @Software: PyCharm
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiMyOrderList:
    """"
    我的订单列表-api
    """

    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.domain
        self.root = "/api/mars/purchasepage/order/list/v2"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def get_order_list(self, smsuid=None):
        """"
        订单列表
        """
        api_url = self.root
        body = {
            "smsuid": smsuid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp


class ApiPostAddress:
    """
    填地址-api
    """

    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.domain
        self.root = "/api/mars/order/address/v2"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def post_address(self, oid=None):
        api_url = self.host + self.root
        body = {"oid": oid,
                "name": "接口自动化测试",
                "tel": "11111111111",
                "addr": "测试-接口自动化测试case地址",
                "region": "北京市 北京市 东城区"}
        # print("body:", body)
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        return resp


class ApiTutorInfo:
    """"
    添加班主任页面查看班主任接口-api
    """

    def __init__(self, auth_token=None, wechat_token=None):
        self.host = Domains.domain
        self.root = "/api/mars/tutor/info/v2"
        self.headers = {"version": "1", "Content-Type": "application/json",
                        "Authorization": auth_token, "wechattoken": wechat_token}

    def get_tutor_info(self, oid=None, uid=None, source=None, smsuid=None):
        """"
        班主任列表
        """
        api_url = self.host + self.root
        body = {
            "oid": oid,
            "uid": uid,
            "source": source,
            "smsuid": smsuid
        }
        resp = send_api_request(url=api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        return resp


if __name__ == "__main__":
    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = UserProperty('18817320774')
    # auth_token = up.basic_auth
    # token = 'Basic M2M2OTdlZjMxNWU2NDIyNzhlNzUwNjY2YTkyNDgzOTI6ODAzYmVjZjY3OGVlNDAwYjkxZGE1M2MwMzA3MWU4NzU='
    # orderlist = ApiMyOrderList(auth_token=token)
    susmuid = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmUiOjE2MTc5Mzg1OTMsIl9pZCI6Ijc2OGRkZmQyMTBjNDRiYTRhOGIxMDY3OTBmNjc0NGVjIiwiZXhwIjoxNjE3OTM4NTkzfQ.qp8weX8ZEaUnSoSp_-ZAm2tDcJytnnaCHemmm-5lbco'
    orderlist = ApiMyOrderList()
    # result = orderlist.get_order_list(susmuid)
    # print(result)

    Authorization = 'Basic MjMwZjEzY2FmZWQ1NGJiNDhiZDVhNTIzZmU4ZDhhNjg6MzE2MmI5ZTBkY2Q2NGUxMmI2MDY0ZDU4OWEzOGY2M2M='
    # addr = ApiPostAddress(Authorization)
    # res = addr.post_address()
    # print(res)

    tutor = ApiTutorInfo(Authorization)
    res = tutor.get_tutor_info(oid='O46050174019309568')
    print(res)