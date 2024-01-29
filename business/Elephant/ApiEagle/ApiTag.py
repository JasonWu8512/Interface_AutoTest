# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/24 5:24 下午
@Author  : Demon
@File    : ApiTag.py
"""



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse



class ApiTag(object):

    def __init__(self, token):
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_profile/tag'

    def api_table_list(self):
        """Desc: 拉取Clickhouse库、表、字段
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/tableList')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_fetch_by_id(self, ids):
        """Desc: 根据标签id拉取数据，标签状态不能为空，否则是数据问题
        :param ids
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchById')
        body = {
            id: ids
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_fetch_data(self, ids):
        """Desc: 拉取标签最新数据或者历史数据
        :param ids
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchData')
        body = {
            "id": ids
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_check_name(self, tag_name):
        """Desc: 根据标签名称检查是否重复
        :param tag_name
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/checkName')
        body = {
            "name": tag_name
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_download_data(self):
        """Desc: 下载数据文件
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/downloadData')
        body = {
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_refresh(self, ids, dt):
        """Desc: 刷新数据
        :param dt "2021-03-23"
        :param ids "16"
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/refresh')
        body = {
            "id": ids,
            "dataTime": dt
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_fetch_tag_meta_info(self, ids, dt):
        """Desc: 获取枚举值
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/fetchTagMetaInfo')
        body = {
            "id": ids,
            "dataTime": dt
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_check_status(self, dt):
        """Desc: 检查数据状态
        :return
        """
        url = parse.urljoin(self.host, f'{self.root}/checkStatus')
        body = {
            "dataTime": dt
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

