# coding=utf-8
# @Time    : 2020/11/4 6:02 下午
# @Author  : jerry
# @File    : ApiPromoter.py
from business.common.UserProperty import UserProperty
from business.common.PromoterProperty import PromoterProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPromoter:
    """
    新推广人1.0
    PromoterController
    """
    root = "/api/promoter"

    def __init__(self, wechat_token=None, basic_auth=None):
        self.headers = {"version": "1", "wechattoken": wechat_token, "Content-Type": "application/json",
                        "Authorization": basic_auth}
        self.host = Domains.domain
        self.wechat_token = wechat_token

    """-------------------------------------PromoterController--------------------------------"""

    def api_promoter_config(self):
        """获取加好友页面对应url"""
        api_url = f'{self.host}{self.root}/config'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_recommend_consumed(self):
        """
        查看推广记录已消费数据
        """
        api_url = f'{self.host}{self.root}/recommendation/consumed'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_recommend_view_only(self):
        """
        查看推广记录只查看数据
        """
        api_url = f'{self.host}{self.root}/recommendation/view-only'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_determine_prometer_role(self, itemid):
        """
        判断推广人等级
        """
        api_url = f'{self.host}{self.root}/role'
        body = {
            "itemid": itemid
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_promoter_invitees_fans(self, orderSubject, pageIndex=0, pageSize=20, tags=[]):
        """
        邀请人列表
        """
        api_url = f'{self.host}{self.root}/invitees/fans'
        body = {
            "orderSubject": orderSubject,
            "pageIndex": pageIndex,
            "pageSize": pageSize,
            "tags": tags,
        }
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_promoter_recruit_form_update(self, wechatAccount, province, city, promoterGoals):
        """真推广人表单"""
        api_url = f'{self.host}{self.root}/recruit/form/update'
        body = {
            "wechatAccount": wechatAccount,
            "province": province,
            "city": city,
            "promoterGoals": promoterGoals,
        }
        resp = send_api_request(url=api_url, method='post', paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_prometer_fans_list(self):
        """
        查询历史粉丝查看和消费
        """
        api_url = f'{self.host}{self.root}/fans/list'
        body = {
            "page": 0,
            "status": "registered"
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_prometer_task_group_list(self):
        """
        查询历史粉丝查看和消费
        """
        api_url = f'{self.host}{self.root}/task/group/list'
        body = {
        }
        resp = send_api_request(url=api_url, method='get', paramType='params', paramData=body, headers=self.headers)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    dm.set_domain("https://fat.jiliguala.com")
    promo = UserProperty('13701941089')
    pro = PromoterProperty('13701941089')
    wechattoken = promo.encryptWechatToken_promoter
    basic = pro.basic_auth
    # pro = ApiPromoter()
    promoter = ApiPromoter(wechattoken, basic)
    res = promoter.api_prometer_fans_list()
    # res = promoter.api_promoter_recruit_form_update(wechatAccount="test",province="北京市",city="北京",promoterGoals=["赚回学费","每月为自己加薪3000块","remark"])
    # res = promoter.api_promoter_login("13951782841")
    # res = pro.api_sms("18261930918")
    # res = pro.api_register_user("18261930918", "6923")
    print(res)
