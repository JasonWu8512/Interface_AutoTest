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
import base64
import time
from business.common.UserProperty import UserProperty


class Mytab(object):
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
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_cenyer_v3_tab(self, bid):
        """
        家长中心详情页
        """
        api_url = "/api/user/center/v3"

        body = {
            'bid': bid,
            'nonce': '9344FEF5-C39D-40D6-8358-F7DF0D84D63A'}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_currentLevel(self, bid):
        """
        切换宝贝，设置该宝贝为当前宝贝
        """
        api_url = "/api/baby/currentLevel"

        body = {
            'bid': bid,
            'nonce': 'a80452f3-ef83-48d7-a617-1a66f1fc8631'}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_babies(self, bid):
        """
        添加新的宝贝
        """
        api_url = "/api/babies"

        """
        bd : 宝贝年龄
        bid ： 当前宝贝bid
        nick ：宝贝名字
        """
        body = {"bd": 1681084800000,
                "bid": bid,
                "choose": 0,
                "nick": "自动化测试",
                "source": "parentCenter"}
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="put",
                                headers=self.headers)["data"]["_id"]
        print(resp)
        return resp

    def api_sms_logout(self):
        """
        获取验证码
        """
        self.api_url = "/api/user/sms_logout"

        body = {
            # "nonce": "40ADFFC5-24EF-420A-92F7-8BEAC5FAD990",
                "type": "text"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


    def api_delete_babies(self, bid1, code, mobile):
        """
        验证码验证
        """
        api_url = "/api/babies"
        body = {"_id": bid1,
                "smsCode": code,
                "mobile": mobile,}
        resp = send_api_request(url=self.host + api_url,paramType="json", paramData=body,method="DELETE",
                                headers=self.headers
                                )
        print(resp)
        return resp

    def api_delete_check(self,bid1):
        """
        删除宝贝
        """
        api_url = "/api/babies/delete_check"
        print(self.host + api_url)
        body = {
            'bid': bid1,
            'nonce': 'a80452f3-ef83-48d7-a617-1a66f1fc8631'}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_sms_code(self):
        """
        修改密码，获取验证码
        """
        api_url = "/api/sms/code"
        body = {"pandora":"MTY4MjMyNDI3NzEwMToyMDIyMDYwODEwMTEyMzYxMmIwN2NjMTI1NDI1NjBlNmQ3N2FmNjQ5YWE2ZWI2MDFjMmJmZDNiMTIzOTc5MzpkNDcyNTYzOGI1YTcwZjkwNWUxNzI1MWM0NGQ5OWU2ZA==",
                "scene":"modify_password",
                "target": "15190529052"
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_code(self,code):
        """
        输入验证码
        """
        api_url= "/api/sms/code"
        body= {"code":code,
               "pandora":"MTY4MjMyNDMwMDI0NzoyMDIyMDYwODEwMTEyMzYxMmIwN2NjMTI1NDI1NjBlNmQ3N2FmNjQ5YWE2ZWI2MDFjMmJmZDNiMTIzOTc5MzpkNDcyNTYzOGI1YTcwZjkwNWUxNzI1MWM0NGQ5OWU2ZA==",
               "scene":"modify_password",
               "target":"15190529052"}
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

    def api_get_home(self):
        """
        魔石商城头部用户魔石信息
        """
        api_url =  '/api/magika/home'
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp

    def api_get_item(self):
        """
        魔石商城商品列表
        """
        api_url =  '/api/magika/item'
        resp = send_api_request(url=api_url, method="get", headers=self.headers)
        return resp

    def api_get_detail(self, commodityno):
        """
        魔石商城商品详情
        :param commodityno:商品id
        :return：
        """
        api_url =  '/api/magika/item/detail'
        body = {
            "commodityNo": commodityno
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_trans(self, page, tab):
        """
        魔石明细页面
        :param page:页码
        :param tab:类型
        :return：
        """
        api_url = "/api/magika/user/trans"
        body = {
            "page": page,
            "tab": tab
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_coupon_available(self, bid, level):
        """
        优惠券
        :status : available 未使用
        :status : expired 已过期
        :status : consumed 已使用

        """
        api_url = "/api/coupon/list/v2"
        body = {
            "bid":bid,
            "level": level,
            "nonce":"759A3947-1DBE-40D3-9F6E-6FC3C911F3E9",
            "page":"0",
            "status":"available"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


    def api_coupon_expired(self, bid, level):
        """
        优惠券
        :status : available 未使用
        :status : expired 已过期
        :status : consumed 已使用

        """
        api_url = "/api/coupon/list/v2"
        body = {
            "bid":bid,
            "level": level,
            "nonce":"759A3947-1DBE-40D3-9F6E-6FC3C911F3E9",
            "page":"0",
            "status":"expired"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_coupon_consumed(self, bid, level):
        """
        优惠券
        :status : available 未使用
        :status : expired 已过期
        :status : consumed 已使用

        """
        api_url = "/api/coupon/list/v2"
        body = {
            "bid": bid,
            "level": level,
            "nonce": "759A3947-1DBE-40D3-9F6E-6FC3C911F3E9",
            "page": "0",
            "status": "expired"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_commodity_spu(self):
        """
        学习材料及周边详情页
        """
        api_url= "/api/eshop/v2/commodity/spu"
        body = {"tagName":"STSC",
                "page":"1"
                }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


    def api_commodity_spu_Liang_SPU_ALL(self):
        """
        学习材料及周边商品详情页
        """
        api_url= "/api/eshop/v2/commodity/spu/Liang_SPU_ALL"
        body = {}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_trade_order(self):
        """
        订单物流页详情页
        """
        api_url = "/api/trade-order/order/myorder"
        body = {"page":0,
                "pageSize":10}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_trade_order_details(self,api_url):
        """
        订单物流详情页，某一定的订单详情
        """
        api_url = api_url
        body = {}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_web_sms(self,mobile):
        """
        站外获取验证码
        """
        api_url = "/api/web/sms"
        body = {"mobile":mobile,
                "source":"NA",
                "crm_source":"NA",
                "yearFlowFlag":"null"}
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_users_token(self,mobile,code,typ):
        """
        站外验证码登陆
        """
        api_url = "/api/users/tokens"
        body = {"u":mobile,
                "p":code,
                "typ":typ
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    # def login(self):
    #     """
    #     游客登陆
    #     """
    #     api_url = '/api/users/guest/v2'
    #     self.headers = {
    #         'Content-Type': 'application/json; charset=UTF-8',
    #         "Authorization": ''}
    #     # "Basic NzEzZDRkZDA1OTU0NDA2ZWIzYzExMjNhYWIxYjQzMTI6MDEwM2Y0MjlkZTgzNGYwNmE0OTJmMGI5Y2MyMGVlNjY="
    #
    #     body = {}
    #     resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="put",
    #                             headers=self.headers)
    #     print(resp)
    #     return resp
    #
    # def get_token(self):
    #     """获取游客登陆token"""
    #     res = self.login()
    #     token = res["data"]["tok"]
    #     uid = res["data"]["_id"]
    #     code = base64.b64encode(f'{uid}:{token}'.encode('utf-8'))
    #     token1 = 'Basic ' + str(code, encoding="utf-8")
    #     print(token1)
    #     guaid = res["data"]["guaid"]
    #     return token1,guaid
    #
    # def api_sms(self,pandora):
    #     """
    #     游客登陆获取验证码
    #     """
    #     api_url = "/api/sms"
    #     body = {"nonce":"A4FB3529-43ED-4EE5-A133-044416266661",
    #             "pandora":pandora,
    #             "target":"11111130189"}
    #     resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
    #     return resp
    #
    # def api_guest_upgrade(self,code):
    #     """
    #     游客输入手机号登陆
    #     """
    #     api_url = "/api/sms/guest/upgrade"
    #     body = {"code": code,
    #             "target": "11111130189"}
    #     resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
    #     return resp

    def api_users_sms_logout(self):
        """
        注销账号获取验证码
        """
        api_url = "/api/user/sms_logout"
        body = {"type":"text"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_security_info(self,mobile,code):
        """
        注销账号
        """
        api_url = "/api/users/security/info"
        body = {"mobile":mobile,
                "smsCode":code
        }
        resp = send_api_request(url=api_url, method="DELETE", headers=self.headers, paramType="params", paramData=body)
        return resp

if __name__ == '__main__':

    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = ApiUser()
    myBid = config["center"]
    cocosEnv = config["cocosEnv"]
    CS_user = config["CS_user"]
    token = user.get_token(typ="mobile", u=CS_user["user"], p=CS_user["pwd"])
    print(token)
    myapi = Mytab(token=token)
    myapi1 = Mytab(token = None)


    resp=myapi1.api_web_sms(mobile=myBid["mobile"])
    print(resp)
    code = usersQuery().get_users(mobile= myBid["mobile"])["sms"]["code"]
    print(code)
    resp2 = myapi1.api_users_token(mobile=myBid["mobile"],code=code,typ=myBid["typ"])
    print(resp2)

    token = resp2["data"]["tok"]
    uid = resp2["data"]["_id"]
    code = base64.b64encode(f'{uid}:{token}'.encode('utf-8'))
    token1 = 'Basic ' + str(code, encoding="utf-8")
    print(token1)

    myapi2 =Mytab(token=token1)

    resp3=myapi2.api_users_sms_logout()
    print(resp3)
    code2 = usersQuery().get_users(mobile= myBid["mobile"])["sms"]["code"]
    print(code2)
    resp4 = myapi2.api_security_info(mobile=myBid["mobile"],code=code2)
    print(resp4)






    # resp = myapi.login()
    # print(resp)
    # resp1 = myapi.get_token()
    # print(resp1)

    # token1 = myapi.get_token()
    # guaid = myapi.get_token()
    # print(guaid)
    # myapi1 = Mytab(token = token1)
    # current_timestamp = int(time.time() * 1000)
    # auth_part = '2022090617204537dac25b2d811d716af3478aff70a2e70113ebf958de83b1:50b665b76488e1d3a565d3d05b63cc69'
    # pandora = base64.b64encode(f'{current_timestamp}:{auth_part}'.encode('utf-8'))
    # resp3 = myapi1.api_sms(pandora= pandora)
    # print(resp3)

    # print(resp)
    # code = usersQuery().get_users(guaid=guaid["sms"]["code"])
    # resp4 = myapi1.api_guest_upgrade(code= code)
    # print(resp4)



    # resp = myapi.api_web_sms(myBid["mobile"])
    # print(resp)
    # code = usersQuery().get_users(mobile=myBid["mobile"])["sms"]["code"]
    # print(code)
    # resp1 = myapi.api_users_token(myBid["mobile"],code,myBid["typ"])
    # print(resp1)
    # resp3 = myapi.api_web_sms(myBid["mobile"])
    # code1 = usersQuery().get_users(mobile=myBid["mobile"])["sms"]["code"]
    # token1 = user.get_token(myBid["mobile"],code1,myBid["typ"])
    # myapi1= Mytab(token = token1)
    # resp2=myapi1.api_users_sms_logout()
    # print(resp)


    # resp2 = myapi1.api_users_sms_logout()
    # print(resp2)

    # resp = myapi.api_trade_order_details(myBid["api_url"])
    # print(resp)
    # resp= myapi.api_trade_order()
    # print(resp)
    # resp = myapi.api_commodity_spu_Liang_SPU_ALL()
    # print(resp)
    # resp = myapi.api_commodity_spu()
    # print(resp)
    # resp1 = myapi.api_coupon_available(myBid["bid"],myBid["level"])
    # print(resp1)
    # resp2 = myapi.api_coupon_consumed(myBid["bid"],myBid["level"])
    # print(resp2)
    # resp3 = myapi.api_coupon_expired(myBid["bid"],myBid["level"])
    # print(resp3)

    # print(code)
    # resp3 = myapi.api_cenyer_v3_tab(myBid["bid"])
    # resp1 = myapi.api_currentLevel(myBid["bid"])
    # bid1 = myapi.api_babies(myBid["bid"])
    # resp0 = myapi.api_sms_logout()

    # resp1 = myapi.api_delete_babies(bid1,CS_user["user"],code)
    # resp = myapi.api_delete_check(bid1)
    # resp = myapi.api_sms_code()
    # code = usersQuery().get_users(mobile="15190529052")["sms"]["code"]
    # resp1 = myapi.api_code(code)
    # resp2 = myapi.api_user()
    # dm = Domains()
    # config = dm.set_env_path("fat")
    # user = UserProperty("19393123455")
    # token = user.basic_auth
    # version = config['version']['ver11.6']
    # 调用魔石商城头部接口
    # resp = myapi.api_get_home()
    # print(resp)
    #
    # # 调用商品列表接口
    # resp01 = myapi.api_get_item()
    # print(resp01)
    #
    # # 调用商品详情接口
    # resp02 = myapi.api_get_detail("MG_goods_012_SPU")
    # print(resp02)
    #
    # resp03 = myapi.api_get_trans("0", "in")
    # print(resp03)
