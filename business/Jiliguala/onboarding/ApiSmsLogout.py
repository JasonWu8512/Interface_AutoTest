"""
=========
Author:Lisa
time:2021/6/16 7:51 下午
=========
"""
import text_unidecode

from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
class ApiSmsLogout():
    '''
        onboading
        SmsLogout 删baby或注销时发送验证码
    '''
    def __init__(self,token,version):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }
    def api_get_sms_logout(self,type):
        '''
        :param type:类型
        :return:
        '''

        api_url = f"{self.host}/api/user/sms_logout"
        body = {
            "type": text
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

if __name__ == '__main__':
    dm=Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("18521030429")
    text=text_unidecode
    token = user.basic_auth
    version=config['version']['ver11.0']
    roadmap = ApiSmsLogout(token, version)
    resp = roadmap.api_get_sms_logout("text")
    print(resp)