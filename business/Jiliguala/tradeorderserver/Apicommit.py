'''
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/26
===============
'''



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiCommit(object):
    """
    订单地址修改，修改提交
    """
    root = '/api/trade-order/order/address/commit'

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" : token
                # "Basic MTY3MmJhNWIzNmRkNGNhNDkzY2FlZmM5NjFjNmY0YjU6MDk0ZDdjOGNkYTNkNDU4N2E3NWQwNzFhNjU4Y2ExYTA="
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_commit(self,orderNo):
        """
        recipient : 接收人
        mobile : 电话
        addressStreet : 详情地址
        addressProvince : 地区
        """
        api_url = "/api/trade-order/order/address/commit"
        print(self.host + self.root)
        body = {"orderNo":orderNo,
                "recipientAddress":{"recipient":"测试",
                                    "mobile":"12345670018",
                                    "addressStreet":"测试测试",
                                    "addressProvince":"北京市",
                                    "addressCity":"北京市",
                                    "addressDistrict":"东城区"}}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp


# if __name__ == '__main__':
#     a = ApiCommit()
#     a.api_commit()