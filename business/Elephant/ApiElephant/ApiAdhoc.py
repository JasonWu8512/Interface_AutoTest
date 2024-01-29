# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/3 1:17 下午
@Author  : Demon
@File    : ApiElephant.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse
import os



class ApiAdhoc(object):

    def __init__(self, token):
        # 请求头文件
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain

    def api_adhoc_left_tree_list(self, user_name='demon_jiao', ):
        """左侧库表基础信息查询"""
        url = parse.urljoin(self.host, '/api_adhoc/leftTree/list')
        body = {
            "user": user_name,
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_sql_info_sql_list(self, user_name='demon_jiao', ):
        """该用户当前历史查询并保存sql脚本"""
        url = parse.urljoin(self.host, '/api_adhoc/sqlInfo/sqlList')
        body = {
            "user": user_name,
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_adhoc_sql_history(self, page_size=20, filters=None, current_page=1, status=None, orders: list=[]):
        """该用户当前历史查询并保存sql脚本
        :filters 模糊搜索条件
        :status 历史搜索的结果，成功还是失败 {'0': 等待中， '1', '2' }
        :orders 数据排序规则 ，[{"column": "startTime", "orderBy": "desc"}]
        :return
        """
        url = parse.urljoin(self.host, '/api_adhoc/adhoc/sqlHistory')
        body = {
            "filter": filters,
            "tagFilter": {
                "status": status
            },
            "pageSize": page_size,
            "currentPage": current_page,
            "orders": orders if orders else [{"column": "startTime", "orderBy": "desc"}]
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_hdfs_upload_file(self, file, user_name='demon_jiao'):
        """
        该用户当前历史查询并保存sql脚本
        :file 文件打开对象/路径
        """
        url = parse.urljoin(self.host, f'/api_adhoc/hdfs/uploadFile?user={user_name}')
        if isinstance(file, str) and os.path.exists(file):
            with open(file, 'rb') as f:
                return send_api_request(method='post', url=url, paramType='file', paramData=f.read(), headers=self.headers)

        return send_api_request(paramType='file', paramData=file, method='post', url=url, headers=self.headers, )

    def api_adhoc_query_list(self, sql, user_name='demon_jiao', ):
        """生成数据查询的sql—log,单语句查询"""
        url = parse.urljoin(self.host, '/api_adhoc/adhoc/queryList')
        body = {
            "user": user_name,
            "queryList": [sql],
            "type": "Hive",
            "limit": "5001"
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_check_status(self, task_id: str):
        """日志状态轮询"""
        url = parse.urljoin(self.host, '/api_adhoc/adhoc/checkStatus')
        body = {"id": [task_id]}

        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_sql_result(self, task_id: str):
        """获取sql查询结果"""
        url = parse.urljoin(self.host, '/api_adhoc/adhoc/sqlResult')
        body = {"id": [task_id]}

        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_task_cancle_task(self, task_id: str, user_name='demon_jiao'):
        """终止sql任务id"""
        url = parse.urljoin(self.host, '/api_adhoc/task/cancelTask')
        body = {"id": [task_id], "user": user_name}

        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

    def api_adhoc_save_sql(self, sql, name):
        """保存sql为历史脚本
        :param name: 脚本名称
        """
        url = parse.urljoin(self.host, '/api_adhoc/sqlInfo/saveSql')
        body = {
            "user": "demon_jiao",
            "sqlCode": sql,
            "sqlName": name
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)


if __name__ == '__main__':
    from business.Elephant.ApiBasic.GetUserProper import GetUserProper
    import requests
    Domains.set_domain('http://10.9.4.124:8088/')
    gup = GetUserProper(user='demon_jiao@jiliguala.com', pwd='demon_jiao123',)
    print(gup.get_token)
    adc = ApiAdhoc(gup.get_token)

    s = open('/business/Elephant/ApiElephant/groundhog.txt', 'rb')

