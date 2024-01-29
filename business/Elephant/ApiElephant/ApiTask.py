# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/22 2:09 下午
@Author  : Demon
@File    : ApiTask.py
"""



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse
import os



class ApiTask(object):

    def __init__(self, token):
        # 请求头文件
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_adhoc/task'

    def api_adhoc_task_cancle_task(self, task_id: str, user_name='demon_jiao'):
        """终止sql任务id"""
        url = parse.urljoin(self.host, f'{self.root}/cancelTask')
        body = {"id": [task_id], "user": user_name}

        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)
