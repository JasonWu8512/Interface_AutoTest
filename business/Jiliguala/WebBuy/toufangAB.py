'''
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/12/22
===============
'''


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.businessQuery import usersQuery
import base64
import time
from business.Jiliguala.lessonbiz import ApiSuper
from business.businessQuery import usersQuery, pingxxorderQuery


class Tfab(object):
    """
    新交易站外购买
    """
    def __init__(self,token=None):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "version": "1"
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        self.host1 = self.dm.set_env_path("prod")["mock_url"]
        print(self.host)

    def api_web_sms(self, mobile):
        """
        站外获取验证码
        """
        api_url = "/api/web/sms"
        body = {"mobile": mobile,
                "source": "NA",
                "crm_source": "NA",
                "yearFlowFlag": "null"}
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        print(resp)
        return resp


    def api_users_token(self, mobile, code, typ):
        """
        站外验证码登陆
        """
        api_url = "/api/users/tokens"
        body = {"u": mobile,
                "p": code,
                "typ": typ
                }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_eshop_v2_orders2(self):
        """
        获取99订单
        """
        api_url = "/api/eshop/v2/orders"
        body = {"payPrice":990,
                "sp2xuId":"3845",
                "recipientInfo":{"recipient":"自动化测试",
                                 "addressCity":"北京市",
                                 "addressDistrict":"东城区",
                                 "mobile":"18976766565",
                                 "addressProvince":"北京市",
                                 "addressStreet":"自动化测试"},
                "nonce":"2023-11-22T07:30:33.364Z",
                "promoterId":None,
                "promotionId":None,
                "groupId":"",
                "guaDouNum":0,
                "useGuadou":False,
                "marketingChannelCode":"",
                "number":1,
                "spuNo":"99_KOL"}
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_order_create_V2(self,itemid,url,sp2xuIds,source,xshareInitiator,sharer):
        """
           投放A流程0元
           投放A流程9.9
           投放B流程0元
           投放B流程9.9
        """

        api_url = "/api/mars/order/create/v2"
        body = {"itemid":itemid,
                 "nonce":"2023-12-21T09:25:15.626Z",
                 "source":source,
                 "xshareInitiator":xshareInitiator, #转介绍人使用的邀请人id
                 "sharer": sharer,                   #邀请人id
                 "sp2xuIds":sp2xuIds,
                 "adtrack_key": url,
                 "visitId":""}
        resp = send_api_request(url=api_url, method="put", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_order_charge_V2(self,order,extra):
        """
           投放A流程0元
           投放A流程9.9
           投放B流程0元
           投放B流程9.9
        """

        api_url = "/api/mars/order/charge/v2"
        body = {"channel":"alipay_wap",
                "oid":order,
                "extra":extra}
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp
    """
    年课投放9.9
    """
    def api_order_create_V3(self,sp2xuIds2):
        """
           年课投放
        """

        api_url = "/api/mars/order/create/v3"
        body = {"itemid":"YGEE_99_SGU_new",
                 "nonce":"2023-12-26T06:10:28.712Z",
                 "source":"ORGANIC_USER",
                 "sp2xuIds":[sp2xuIds2],
                 "spuNo": "YGEE_99_SPU_LXTMK_new",
                 "payPrice":990}
        resp = send_api_request(url=api_url, method="put", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_order_charge_V3(self,order):
        """
           年课投放
        """

        api_url = "/api/mars/order/charge/v3"
        body = {"channel":"wx_wap",
                "oid":order,
                "extra":{"result_url":"https://fat-t1.jiliguala.com/exyw"}}
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp



    def api_post_mock(self, id, time_paid, order_no, transaction_no):
        """
        mock支付
        @param id:付款单
        @param time_paid:支付时间
        @param order_no:订单编号
        @param transaction_no:支付id
        @return:
        """
        api_url = f"{self.host1}/api/mock/pingpp/charge/callback"
        body = {
            "type": "charge.succeeded",
            "data": {
                "object": {
                    "id": id,
                    "time_paid": time_paid,
                    "order_no": order_no,
                    "transaction_no": transaction_no
                }
            }
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

    def api_mars_order(self,oid):
        """
        支付成功
        """
        api_url= "/api/mars/order"
        body = {"oid":oid}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_order_address(self,oid):
        """
        投放9.9填写地址
        """
        api_url = "/api/mars/order/address/v2"
        body = {"oid":oid,
                "name":"哈哈哈哈哈",
                "tel":"15769696969",
                "region":"北京市 北京市 东城区",
                "addr":"哈哈哈哈哈哈",
                "spuId":"K1GETC_99_SPU_H5_LXTMK"}
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp



    def api_eshop_ghs_info(self, orderId):
        """

        """
        api_url = "/api/eshop/ghs/info"
        body = {"orderId": orderId}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_tutor_info_v2(self,orderId):
        """
        获取账号购买成功信息
        """
        api_url = "/api/mars/tutor/info/v2"
        body = {"orderId": orderId}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


    def api_fc_tutor_info(self,orderId):
        """
        获取账号购买成功信息
        """
        api_url = "/api/mars/fc/tutor/info"
        body = {"orderId": orderId,
                "uid":"",
                "source":"test"}
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp




if __name__ == '__main__':

    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = ApiUser()
    myBid = config["center"]
    cocosEnv = config["cocosEnv"]
    # # newteade =NewTeade(token = "")
    # getmobile= ApiSmsInfo()
    # mobile1= getmobile.api_get_mobile()
    # mobile = mobile1["data"]
    # print(mobile)
    # # print(mobile1)
    # # resp = newteade.api_web_sms(mobile = mobile)
    # print(resp)
    # code = usersQuery().get_users(mobile=mobile)["sms"]["code"]
    # print(code)
    # resp1 = newteade.api_users_token(mobile=mobile,code= code,typ=myBid["typ"])
    # print(resp1)
    # token = resp1["data"]["tok"]
    # uid = resp1["data"]["_id"]
    # code = base64.b64encode(f'{uid}:{token}'.encode('utf-8'))
    # token1 = 'Basic ' + str(code, encoding="utf-8")
    # print(token1)
    # newteade1= NewTeade(token = token1)
    # resp2 = newteade1.api_eshop_v2_orders()
    # oid = resp2["data"]["orderNo"]
    # print(oid)
    # print(resp2)
    # resp3 = newteade1.api_eshop_v2_orders_charge(oid = oid)
    # print(resp3)
    # id = resp3['data']['id']
    # time_paid = resp3['data']['created']
    # order_no = resp3['data']['orderNo']
    # current_timestamp = int(time.time() * 1000)
    # transaction_no = 'MOCK4200001986' + str(current_timestamp)
    # resp4= newteade1.api_post_mock(id=id, time_paid=time_paid, order_no=order_no, transaction_no=transaction_no)
    # print(resp4)
    # resp5 = newteade1.api_order_status(oid = oid)
    # print(resp5)
    # resp6 = newteade1.api_eshop_ghs_info(orderId= oid)
    # print(resp6)
    # resp7 = newteade1.api_tutor_info_v2(orderId=oid)
    # print(resp7)
    # order = pingxxorderQuery().get_pingxxorder(uid=uid, status='paid', itemid='S1GE_W1_4_SGU_new')['_id']
    # print(order)
    # order_no = order








