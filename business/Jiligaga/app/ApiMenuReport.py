from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiMenuReport(object):

    def __init__(self, token):
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "platform": "ios",
            "Authorization": token,
            "appversion": "1.29.0",
            "Accept-Language": "zh-tw"
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def menu_report(self, bid):
        api_url = "/api/parent/menu"
        body = {
            "bid": bid
        }
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

# if __name__ == '__main__':
#     a =ApiPurchaseCommoditySpu()
#     a.purchase_commodity_spu(spuNo= "CP90050673",countryCode="tw")
