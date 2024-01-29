# -*- coding: utf-8 -*-
# @Time : 2021/4/21 7:42 下午
# @Author : jane
# @File : ApiSuper.py
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
class ApiV2RoadSwitch:
    """
    /api/v2/lesson/roadmap/switch
    v9.0始首页切换课程，切换课程类型/课程级别
    OtherController
    lessonbiz
    """
    def __init__(self,token,version):
        self.host = Domains.config.get('url')
        self.root = '/api/v2/lesson'
        self.headers = {
            "authorization": token,
            "Content-Type": "application/json",
            "X-APP-Version": version
        }
    def api_road_swith_v2(self,bid,type=None,lv=None):
        """
        切换课程类型/课程级别
        :param bid:必须参数宝贝id
        :param type:非必须参数当前课程的类型
        :param lv:非必须参数当前课程的级别
        """
        api_url = f"{self.host}{self.root}/roadmap/switch"
        body={
            "bid":bid,
            "type":type,
            "lv":lv
        }
        resp = send_api_request(method='post',url=api_url,paramType="json",headers=self.headers,paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    users = UserProperty("19991011051")
    token = users.basic_auth
    version = config['version']['ver11.6']
    roadmap = ApiV2RoadSwitch(token,version)
    resp = roadmap.api_road_swith_v2("1b877919e16d4a8682bce4014bf70c6b",lv="L2MC")

    print(resp)