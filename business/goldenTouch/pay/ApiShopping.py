# coding=utf-8
# @Time    : 2022/7/18 5:11 下午
# @Author  : Karen
# @File    : ApiShopping.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiShopping(object):

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_goldentouch_shopping_newViewpage(self, spuId):
        """ 01）请求购买页 """
        api_url = "/api/goldenTouch/shopping/newViewpage"
        body = {"spuId": spuId}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)

        return resp


    def api_goldentouch_shopping_newLessonDetail(self, spuId):
        """ 02）购买详情页 """
        api_url = "/api/goldenTouch/shopping/newLessonDetail"
        body = {"spuId": spuId}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp


    def api_goldentouch_shopping_purchase(self, source, click_id, channel, itemid, openid, physical=False):
        """ 03）创建订单 """
        api_url = "/api/goldenTouch/shopping/purchase"
        body = {
            'source': source,
            'click_id': click_id,
            'channel': channel,
            'itemid': itemid,
            'openid': openid,
            'physical': physical

        }

        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json', method="post",
                                headers=self.headers)
        return resp


    def api_goldentouch_shopping_addAdvisor(self,subject):
        """ 04）添加学习顾问 """
        api_url = "/api/goldenTouch/shopping/addAdvisor"
        body = {'subject': subject}  # subject:学科
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="params", method="get",
                                headers=self.headers)

        return resp


    def api_goldentouch_shopping_updateAddress(self, orderNo, addressCity, addressDistrict, addressProvince,
                                                   addressStreet, mobile, recipient):
        """ 05）更新收货地址 """
        api_url = "/api/goldenTouch/shopping/updateAddress"
        body = {}
        body = {
            "addressCity": addressCity,
            "addressDistrict": addressDistrict,
            "addressProvince": addressProvince,
            "addressStreet": addressStreet,
            "mobile": mobile,
            "orderNo": orderNo,
            "recipient": recipient
        }

        resp = send_api_request(url=self.host + api_url, paramData=body, paramType='json',method="post", headers=self.headers)
        return resp