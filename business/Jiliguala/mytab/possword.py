
''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/4/7
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser
from business.businessQuery import usersQuery
import time
import base64




class Possword(object):
    """
    我的tab页
    """
    root = '/api/user/center/v3'

    def __init__(self, token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "version": "1"
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["url"]
        print(self.host)


    def api_sms_code(self,pandora):
        """
        修改密码，获取验证码
        """
        api_url = "/api/sms/code"
        body = {"pandora": pandora,
                "scene":"modify_password",
                "target": "11111130002"
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_code(self,pandora,code):
        """
        输入验证码
        """
        api_url= "/api/sms/code"
        body= {
               "pandora":pandora,
               "scene":"modify_password",
               "target":"11111130002",
               "code": code
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp

    def api_user(self):
        """
        修改密码
        """
        api_url = "/api/users"
        body = {"p":"Jlgl168."}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="PATCH",
                                headers=self.headers)
        print(resp)
        return resp

if __name__ == '__main__':

    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = ApiUser()
    myBid = config["center"]
    cocosEnv = config["cocosEnv"]
    CS_user = config["CS_user"]
    token = user.get_token(typ="mobile", u="11111130002", p="Jlgl168.")
    print(token)
    myapi = Possword(token=token)
    current_timestamp = int(time.time() * 1000)
    auth_part = '2022090617204537dac25b2d811d716af3478aff70a2e70113ebf958de83b1:50b665b76488e1d3a565d3d05b63cc69'
    pandora = base64.b64encode(f'{current_timestamp}:{auth_part}'.encode('utf-8'))
    print(current_timestamp)

    # print(code)
    # resp3 = myapi.api_cenyer_v3_tab(myBid["bid"])
    # resp1 = myapi.api_currentLevel(myBid["bid"])
    # bid1 = myapi.api_babies(myBid["bid"])
    # resp0 = myapi.api_sms_logout()

    # resp1 = myapi.api_delete_babies(bid1,CS_user["user"],code)
    # resp = myapi.api_delete_check(bid1)
    # resp= myapi.api_sms_code(pandora)
    code = usersQuery().get_users(mobile="11111130002")["sms"]["code"]
    resp1 = myapi.api_code(pandora,code)
    # resp2 = myapi.api_user()

