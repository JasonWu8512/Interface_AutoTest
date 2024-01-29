'''
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/8/10
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser
from business.businessQuery import usersQuery


class Zpt(object):
    """
    真拼团线上问题，自动化覆盖
    """
    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
                # "Basic MjY5MTljYmQ0YzY2NDIyMjgwOTEzZWIzY2YxZDE0NjI6ODA0NWUwMWY5NWZjNDRjMGFkNmRkM2RmYzg2MDQ2Njc=",
            "Origin": "https://fatspa.jiliguala.com",
            "version":"1"
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["url"]


    def api_WebSms(self):
        """
        使用符合条件的账号获取验证码
        """
        api_url = "/api/web/sms"
        body = {"crm_source": "sampleH5",
                "mobile": "16600010002",
                "source": "NA"
                }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.headers)
        print(resp)
        return resp


    def api_tokensV3(self, mobile, code):
        """
        输入验证码，登录账号，获取账号信息
        """
        api_url = "/api/users/tokens/v3"
        body = {
            "u": mobile,
            "p": code,
            "typ": "mobilecode",
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


    def api_stock_v2(self):
        """

        """
        api_url = "/api/mars/purchasepage/stock/v2"
        body = {
            "spuId": "K1GEFC_0_SPU_WXstore",
            "reSub": "undefined",
            "visitId": "",
            "source": "pintuan",
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_config_v2(self):
        """
        查看参团跳转链接
        """
        api_url = "/api/xshare/grouppurchase/config/v2"
        body = {
            "gpid" : "jlglpintuan202307_ZJS1"
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


if __name__ == '__main__':

    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = ApiUser()
    CS_user = config["Cj_ZptFh"]
    token = user.get_token(typ="mobile", u=CS_user["user"], p=CS_user["pwd"])
    myapi = Zpt(token=token)
    resp = myapi.api_WebSms()
    mobile = config["CJ_Zpt"]
    code = usersQuery().get_users(mobile=mobile["mobile1"])["sms"]["code"]
    print(code)
    resp1 = myapi.api_tokensV3(mobile["mobile1"],code)
    # resp2 = myapi.api_stock_v2()
    # resp3 = myapi.api_config_v2()