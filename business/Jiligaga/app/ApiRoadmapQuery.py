# -*- coding: utf-8 -*-
# @Time : 2022/6/22 下午3:34
# @Author : Saber
# @File : ApiRoadmapQuery.py



from ensurepip import version

from paramiko import agent
from business.common.UserProperty import UserProperty
from business.xshare.ApiUser import ApiUser
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiligaga.app.ApiLogin import Login

class ApiRoadmapQuery ():
    """
    app  C端：路线图
    RoadmapController
    """

    def __init__(self, token= None,appversion=None):
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "appversion": appversion,
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def api_roadmap_query(self, bid):
        """
        路线图查询
        :param bid：宝贝id
        :return:
        """
        api_url = '/api/roadmap/query'
        body = {
            "bid": bid
        }
        resp = send_api_request ( url=self.host + api_url, paramType='json', paramData=body, method="post",
                                  headers=self.headers )
        return resp


if __name__ == '__main__':
    # dm = Domains ()
    # dm.set_domain ( "https://fat.jiligaga.com" )
    token = 'Basic NWI4ZWVhZmRkZmRlNGYwOWFjODk4MDgyZjBhNTMyYTI6YmJkOTBhN2Q1ZGZmNGExN2I1NzhmZGRkYzEzMGIyNGQ6NUQxMURCNkItNzg4OC00OTk1LTg4OTEtQzNBOUM1NUVBNUI4'
    appversion = '1.30.0'
    #获取路线图数据
    roadmap = ApiRoadmapQuery(token= token,appversion=appversion)
    resp = roadmap.api_roadmap_query(bid='2e009c7d83954ccbbb5a81281a733873')
    print(resp)
    status = resp.get('data').get('roadmap').get('elements')[1].get('lessons')[2].get('status')
    print(status)
