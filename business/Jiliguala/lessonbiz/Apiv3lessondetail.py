''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/10
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser


class ApiV3LessonDetail(object):
    """
    课程详情页
    """
    root = '/api/super/v2/lessondetail'

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization" :token,
                # "Basic YmFlZGY0ZWJjYjYwNDk3YTg5ZjlkZGI3OTA4N2U2ZDY6OGVhNmYxM2Q3Y2VjNGM1M2E3MWFiMTExZGUxMmFiMzc=",
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["url"]
        print(self.host)

    def api_v3lessondetailBD(self,bid,nonce):
        """
        发送请求，呱呱爱表达
        """
        api_url = "/api/v3/lesson/detail"
        body = {'lid': 'K1GEE001',
                'bid': bid,
                'nonce': nonce
                }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='params', method='get',
                                 headers=self.headers)

        return resp


    def api_v3lessondetailSk(self,bid,nonce):
        '''
        发送请求，呱呱爱思考
        '''
        api_url = "/api/v3/lesson/detail"
        body = {'lid':'K1MAE001',
                'bid':bid,
                'nonce':nonce}
        resp = send_api_request(url= self.host+api_url,paramData=body, paramType='params',method='get',
                                headers=self.headers)

        return resp



if __name__ == '__main__':

    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = ApiUser()
    v3 = config["v3lessondetail"]
    CS_user = config["CS_user"]
    token = user.get_token(typ='mobile', u=CS_user["user"], p=CS_user["pwd"])
    apiv3lessondetail = ApiV3LessonDetail(token=token)
    resp = apiv3lessondetail.api_v3lessondetailBD(v3["bid"],v3["noncebd"])
    resp2 =apiv3lessondetail.api_v3lessondetailSk(v3["bid"],v3["noncesk"])
    print(resp)
    print(resp2)
