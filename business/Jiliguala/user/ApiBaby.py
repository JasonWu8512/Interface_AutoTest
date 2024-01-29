# -*- coding: utf-8 -*-
# @Time : 2021/5/26 7:48 下午
# @Author : Cassie
# @File : ApiBaby.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiBaby():
    """
    userbiz  C端：宝贝信息相关接口
    BabyController
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/baby'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_level_recommend2(self, bid, bd, account):
        """
        获取对应baby的推荐级别-v2
        :param bid:宝贝id
        :param bd:宝贝生日
        :param account:呱号
        :return:
        """
        api_url = f"{self.host}{self.root}/levelRecommend/v2"
        body = {
            "bid": bid,
            "bd": bd,
            "account": account,
            "device_id": "bf3fffde-bfff-ec6d-97bf-bbfef2ff772b"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_get_level_recommend(self, bid, bd, account):
        """
        获取对应baby的推荐级别
        :param bid:宝贝id
        :param bd:宝贝生日
        :param account:呱号
        :return:
        """
        api_url = f"{self.host}{self.root}/levelRecommend"
        body = {
            "bid": bid,
            "bd": bd,
            "account": account,
            "device_id": "bf3fffde-bfff-ec6d-97bf-bbfef2ff772b"
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


    def api_get_currentLevel(self, bid):
        """
        获取对应baby当前级别
        :param bid:宝贝id
        :return:
        """
        api_url = f"{self.host}{self.root}/currentLevel"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp


    def api_post_enter_sublesson(self, bid, lid):
        """
        sound
        :param bid:宝贝id
        :param lessonId:老呱美课程id
        :return:
        """
        api_url = f"{self.host}{self.root}/enter/sublesson"
        body = {
            "bid": bid,
            "lid": lid
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("15958112857")
    token = user.basic_auth
    version = config['version']['ver16.0']
    baby = ApiBaby(token, version)
    # resp = pop.api_get_pop("22ee5af5a227487d8979d73fa34faea3", "K1MA", "math")
    # resp=pop.api_tab_get("3aec6bbdc84048f8b9e68580390a300c","buyTab","popup")
   # resp = baby.api_get_level_recommend2("3aec6bbdc84048f8b9e68580390a300c", "1653609600000", "1493019")
   # resp = baby.api_get_level_recommend("3aec6bbdc84048f8b9e68580390a300c", "1653609600000", "1493019")
    #resp = baby.api_get_currentLevel("3aec6bbdc84048f8b9e68580390a300c")
    resp = baby.api_post_enter_sublesson("3aec6bbdc84048f8b9e68580390a300c","L1XX001")
    print(resp)
