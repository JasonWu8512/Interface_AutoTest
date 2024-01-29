# -*- coding: utf-8 -*-
# @Time : 2021/3/1 7:36 下午
# @Author : Cassie
# @File : ApiReso.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGetPop():
    """
    11.5及以上版本，客户端获取接入资源位的弹窗
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/reso/portrait'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_get_pop(self, bid, level, mod):
        """
        11.5以下版本调用，获取弹窗信息
        :param bid:宝贝id
        :param level:用户当前级别
        :param mod:对应模块
        :return:
        """
        api_url = f"{self.host}{self.root}/get/byuser"
        body = {
            "bid": bid,
            "level": level,
            "nonce": "0E2AE2A7-B7C0-4833-83D6-4E939F0B6101 HTTP/1.1",
            "bu": "jlgl",
            "prop": "homePopup",
            "mod": mod
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_tab_get(self, bid, mod, prop):
        """
        11.5及以上版本调用，获取弹窗信息
        :param bid:宝贝id
        :param mod:模块（购买tab/用户tab）
        :param prop:类型（弹窗/banner）
        :return:
        """
        api_url = f"{self.host}{self.root}/tab/get"
        body = {
            "bid": bid,
            "mod": mod,
            "nonce": "0E2AE2A7-B7C0-4833-83D6-4E939F0B6101 HTTP/1.1",
            "propType": prop
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_report_pop(self, id, type):
        """
        上报弹窗点击情况
        :param id:弹窗对应的id
        :type: 上报类型（曝光/点击）
        :return:
        """
        api_url = f"{self.host}{self.root}/report"
        body = {
            "id": id,
            "type": type
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("15958112857")
    token = user.basic_auth
    version = config['version']['ver15.0']
    pop = ApiGetPop(token, version)
    # resp = pop.api_get_pop("22ee5af5a227487d8979d73fa34faea3", "K1MA", "math")
    # resp=pop.api_tab_get("3aec6bbdc84048f8b9e68580390a300c","buyTab","popup")
    resp = pop.api_report_pop(155, "expose")
    print(resp)
