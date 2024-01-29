from business.Jiligaga.app.ApiLogin import Login
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiligaga.app.ApiAccountV3 import ApiAccountV3


class ApiShareGet(object):

    def __init__(self):
        # self.login = Login()
        self.apiAccountV3 = ApiAccountV3()
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        self.token = self.apiAccountV3.login_password(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"],
                                                      countrycode=self.gaga_app["countryCode"])["data"]["auth"]
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "platform": "ios",
            # "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC",
            "Authorization": self.token
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def share_get(self):
        api_url = "/api/share/get"
        # body = {
        #     "bid": bid,
        #     "menuNo": menuNo
        # }
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json",  method="get",
                                headers=self.headers)
        print(resp)
        return resp
# if __name__ == '__main__':
#     a =ApiPurchaseCommoditySpu()
#     a.purchase_commodity_spu(spuNo= "CP90050673",countryCode="tw")
