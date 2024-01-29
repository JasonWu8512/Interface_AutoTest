# -*- coding: utf-8 -*-
# @Time : 2021/3/1 7:40 下午
# @Author : Cassie
# @File : ApiManage.py
from config.env.domains import Domains
from utils.format.format import get_timestr
from utils.requests.apiRequests import send_api_request
from business.sso.ApiSso import ApiSso
from business.Jiliguala.portraitbiz.portraitAdmin.ApiSsoPortrait import ApiSsoPortrait


class ApiManage():
    """
    资源位管理后台：列表查询
    """
    root = '/api/portraitbiz/manage'

    def __init__(self, token):
        self.headers = {"authorization": f"Basic {token}", "Content-Type": "application/json"}
        self.host = Domains.config.get('url')

    def api_get_all(self, limit, page, title="", id=None):
        """
        搜索资源位
        :param limit: 每页大小
        :param page: 页码
        :param title: 资源位名称
        :param id: 资源位ID
        """
        api_url = f'{self.host}{self.root}/get/all'
        body = {
            "limit": limit,
            "page": page,
            "search.title": title,
            "search.manageId": id
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_get_tags(self):
        """
        获取用户标签列表
        """
        api_url = f'{self.host}{self.root}/get/tags'
        body = {
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp

    def api_create(self, modId, propId, redirectType, link, priority=99, cooldown='null', limit="", begin="", end="",
                   times=""):
        """
        新建资源位
        ：param modId: 模块(购买tab/用户tab)
        : param propId: 类型（弹窗/banner）
        : param redirectType: 跳转类型（App/H5/小程序）
        : param link: 跳转链接
        ：param priority: 优先级
        ：param cooldown：间隔时间
        ：param limit: 点击次数
        ：param begin: 有效期开始时间
        ：param end：有效期结束时间
        ：param times: 曝光次数

        """
        api_url = f'{self.host}{self.root}/create'
        body = {"channel": "auto", "content": {"buId": "jlgl", "modId": modId, "propId": propId, "title": "自动化脚本创建",
                                               "redirectType": redirectType, "link": link,
                                               "img": "https://qiniucdn.jiliguala.com/appBanner/6f4dd96fccdf0aea7da68506939753b8_1620611598687_%E8%BF%90%E8%90%A5%E4%BD%8D%E5%BC%B9%E7%AA%97%E5%9B%BE.png"},
                "rule": {"title": "自动化脚本创建", "tags": ["86"], "priority": priority, "limit": limit, "times": times,
                         "begin": begin, "end": end, "cooldown": cooldown}}
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp

    def api_update(self, id, modId, propId, redirectType, link, priority=99, cooldown='null', limit="", begin="",
                   end="",
                   times=""):
        """
        更新资源位
        :param id:资源位弹窗id
        ：param modId: 模块(购买tab/用户tab)
        : param propId: 类型（弹窗/banner）
        : param redirectType: 跳转类型（App/H5/小程序）
        : param link: 跳转链接
        ：param priority: 优先级
        ：param cooldown：间隔时间
        ：param limit: 点击次数
        ：param begin: 有效期开始时间
        ：param end：有效期结束时间
        ：param times: 曝光次数

        """
        api_url = f'{self.host}{self.root}/update'
        body = {"channel": "auto", "id": id,
                "content": {"buId": "jlgl", "modId": modId, "propId": propId, "title": "自动化脚本更新",
                            "redirectType": redirectType, "link": link,
                            "img": "https://qiniucdn.jiliguala.com/appBanner/6f4dd96fccdf0aea7da68506939753b8_1620611598687_%E8%BF%90%E8%90%A5%E4%BD%8D%E5%BC%B9%E7%AA%97%E5%9B%BE.png"},
                "rule": {"title": "自动化脚本更新", "tags": ["86"], "priority": priority, "limit": limit, "times": times,
                         "begin": begin, "end": end, "cooldown": cooldown}}
        resp = send_api_request(url=api_url, method='post', paramData=body,
                                paramType='json', headers=self.headers)
        return resp

    def api_get_id(self, id):
        """
        查询单个资源位详情
        :param id: 资源位id
        """
        api_url = f'{self.host}{self.root}/get/byid'
        body = {
            "id": id
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    sso = ApiSso(email_address=config['sso']['email_address'], pwd=config['sso']['pwd']).sso_code
    token = ApiSsoPortrait().api_get_token(sso)
    begin = get_timestr(hour=-8)
    end = get_timestr()
    # resp = ApiManage(token).api_get_all(10, 0, id=1)
    # resp = ApiManage(token).api_get_id(154)
    # resp = ApiManage(token).api_create("buyTab", "buyPopup", "App", "jlgl://xxcourse-purchase?type=XX",
    #                                    cooldown="120", limit="2", begin=begin, end=end,
    #                                    times="3")
    # resp = ApiManage(token).api_update(156,"buyTab", "buyPopup", "App", "jlgl://xxcourse-purchase?type=XX",
    #                                    cooldown="600", limit="12", begin=begin, end=end,
    #                                    times="13")
    resp=ApiManage(token).api_get_tags()

    # resp = ApiManagePortrait(token).api_update(84, modId="home", priority=22, cooldown=60, limit=3)

    print(resp)
