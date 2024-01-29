from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPurchaseCommoditySpu ( object ):

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "platform": "ios",
            # "dev_uni_id": "C264F398-4132-4162-BC09-8DD21CA8CACC"
        }
        self.dm = Domains ()
        # 设置域名host
        self.host = self.dm.set_env_path ( 'fat' )["gaga_url"]


    def purchase_commodity_spu(self,spuNo,countryCode):
        """机转-c端推荐spu"""
        api_url = "/api/purchase/commodity/spu"
        body = {
            "spuNo":spuNo,
            "countryCode":countryCode
        }
        print ( self.host + api_url )
        resp = send_api_request ( url=self.host + api_url, paramType="json", paramData=body, method="post",
                                  headers=self.headers )
        print ( resp )
        return resp


    def purchase_commodity_spu_renzhuan(self,spuNo_renzhuan,countryCode1):
        """人转-c端推荐spu"""
        api_url = "/api/purchase/commodity/spu"
        body = {
            "spuNo":spuNo_renzhuan,
            "countryCode":countryCode1
        }
        print ( self.host + api_url )
        resp = send_api_request ( url=self.host + api_url, paramType="json", paramData=body, method="post",
                                  headers=self.headers )
        print ( resp )
        return resp
# if __name__ == '__main__':
#     a =ApiPurchaseCommoditySpu()
#     a.purchase_commodity_spu(spuNo= "CP90050673",countryCode="tw")