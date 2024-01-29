# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 11:33 上午
@Author  : Demon
@File    : ApiUserGroup.py
"""


from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from utils.requests.apiRequests import send_api_request
from urllib import parse

class ApiUserGroup(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_profile/userGroup'

    def api_fetch_filter_list(self):
        """
        获取分群筛选列表
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchFilterList')
        body = {}
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_fetch_all(self, filters=None, pages=20, cpage=1, orders=[]):
        """
        获取分群列表
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchAll')
        body = {
            "filter": filters,
            "pageSize": pages,
            "currentPage": cpage,
            "orders": orders if orders else [{"column": "calculateTime", "orderBy": "desc"}]
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_fetch_by_id(self, group_id):
        """
        获取分群基本信息
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchById')
        body = {
            "id": group_id,
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_fetch_tags(self, group_id,):
        """
        获取分群标签列表数据信息
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchTags')
        body = {
            "id": group_id,
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_refresh(self, group_id,):
        """
        重新计算分群信息
        """
        url = self.host + f'{self.root}/refresh'
        body = {
            "id": group_id,
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_check_name(self, group_name,):
        """
        检测分群名称是否重复
        """
        url = parse.urljoin(self.host, f'{self.root}/checkName')
        body = {
            "name": group_name,
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_add(self, group_name, comment='', show_range=None, source=None, is_update='once'):
        """
        新建用户分群
        """
        url = parse.urljoin(self.host, f'{self.root}/checkName')
        body = {
            "name": group_name,
            "comment": comment,
            "source": source,
            "showRange": show_range,
            "frequencyStatus": None,
            "filterRule": {
                "condition": None,
                "children": [{
                    "name": "宝贝当前月龄标签",
                    "id": "19",
                    "content": "",
                    "sql": "ods.dm_personlabel_base_together_all_d_dis_view.birthday_month_split",
                    "type": "sql",
                    "tagType": "basic",
                    "updateFrequency": "day",
                    "columnType": "String",
                    "filter": {
                        "operator": "is not null",
                        "value": None
                    },
                    "dateRange": ["2020-12-08", "2020-12-09"]
                }]
            }
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_delete(self, group_id):
        """
        删除分群
        """
        url = parse.urljoin(self.host, f'{self.root}/delete')
        body = {
            "group_id": group_id
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_history_data(self, dt):
        """
        获取分群历史数据
        """
        url = parse.urljoin(self.host, f'{self.root}/historyData')
        body = {
            "dateTime": dt,
        }
        return send_api_request(method='post', url=url, paramData=body, paramType='json', headers=self.headers)

    def api_check_status(self, dt):
        """Desc:获取分群计算状态
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/checkStatus')
        body = {
            "dataTime": dt
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_download_data(self):
        """Desc: 下载用户分群历史数据
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/downloadData')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)


if __name__ == '__main__':
    from business.Elephant.ApiBasic.GetUserProper import GetUserProper
    import requests
    Domains.set_domain('http://givendata.jiliguala.com/')
    gup = GetUserProper(user='demon_jiao@jiliguala.com', pwd='demon_jiao123',)
    print(gup.get_token)
    asu = ApiUserGroup(gup.get_token)
    print(asu.api_fetch_filter_list())




