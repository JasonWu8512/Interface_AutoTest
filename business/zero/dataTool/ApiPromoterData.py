# coding=utf-8
# @Time    : 2020/12/11 1:54 下午
# @Author  : jerry
# @File    : ApiPromoterData.py
from utils.format.format import get_timestr
from utils.requests.apiRequests import send_api_request
from dateutil import parser


class ApiPromoterData:
    """
    推广人业务相关数据库交互操作
    """
    root = "/v1/dataTool/data/operate"

    def __init__(self):
        self.host = "http://zero.jlgltech.com"
        # self.host = "http://127.0.0.1:8000"
        self.headers = {"version": "1", "Content-Type": "application/json"}

    def api_set_promoter_data(self, operation, env, mobile=None, content=None, orderId=None):
        """根据不同的测试场景，预置测试数据"""
        api_url = f'{self.host}{self.root}'
        body = {
            "env": env,
            "mobile": mobile,
            "orderId": orderId,
            "operation": operation,
            "content": content
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    content = {
        'level': "partner",
        'oddPartner': True,
        'expireTs': get_timestr(day=1),
        'stockAmount': 0,
        'balance': 45
    }
    pd = ApiPromoterData()
    re = pd.api_set_promoter_data(env='dev', operation='get_promoter', mobile='13951782841')
    print(re)