from business.Jiligaga.app.ApiLogin import Login
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiBabyDelete(object):

    def __init__(self, token=None):
        self.login = Login()
        self.dm = Domains()
        self.host = self.dm.set_env_path('fat')["gaga_url"]
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "platform": "ios",
            # "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC",
            "Authorization": token
        }

    def baby_delete(self, bid):
        api_url = "/api/user/baby/delete"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=self.host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp
# if __name__ == '__main__':
#     a =ApiBabyDelete(token="Basic NGI4NWQ0MzNhM2RlNDQwYWE4NWM5NzEzODE4OTNiOGM6YjJlNDgzMDJhZWM4NGQyOGIxMWEwMzdlMDg5Mjg3MGM6RUU3NTAwNkYtMTYyMy00MUUwLTg3RjMtQjM3RDA2MDdCNUY0")
#     a.baby_delete(bid="d752e09f8176408c90327f510d9416fa")
