'''
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/15
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGet(object):
    """获取资源位信息"""
    root = '/api/reso/portrait/tab/get'

    def __init__(self, token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token

        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_get_usertab(self, bid, mod, channel=None):
        # 我的tab资源位
        api_url = "/api/reso/portrait/tab/get"
        # body = {'mod': 'userTab',
        #         'channel': channel,
        #         'bid': bid,
        #         'nonce': ''}
        body = {'mod': mod,
                'bid': bid,
                'nonce': ''}
        if channel:
            body['channel'] = channel
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    # def Get_buytab(self, bid, channel):
    #     # 购买tab页资源位
    #
    #     api_url = "/api/reso/portrait/tab/get"
    #     print(self.host + self.root)
    #     body = {'mod': 'userTab',
    #             'channel': channel,
    #             'bid': bid,
    #             'nonce': ''}
    #     resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp
    #
    # def Get_endtab(self, bid, channel):
    #     # 学习tab页资源位
    #
    #     api_url = "/api/reso/portrait/tab/get"
    #     print(self.host + self.root)
    #     body = {'mod': 'endtab',
    #             'channel': channel,
    #             'bid': bid,
    #             'nonce': ''}
    #     resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp

# if __name__ == '__main__':
#     a = ApiGet()
#     a.Get_tab()
