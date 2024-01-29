from business.Jiligaga.app.ApiLogin import Login
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiBabyCreate(object):

    def __init__(self,token=None):
        self.login = Login()
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        # self.token = self.login.phone_pwd_login(phone=self.gaga_app["phone"], pwd=self.gaga_app["pwd"])["data"]["auth"]
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "platform": "ios",
            # "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC",
            "Authorization": token
        }
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def baby_create(self, birth, nick):
        api_url = "/api/user/baby/create"
        body = {
            "birth": birth,
            "nick": nick,
            "headPic": ""
        }
        print(self.host + api_url)
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp
# if __name__ == '__main__':
#     a =ApiPurchaseCommoditySpu()
#     a.purchase_commodity_spu(spuNo= "CP90050673",countryCode="tw")
