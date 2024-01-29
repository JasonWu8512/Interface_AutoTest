# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/22 2:06 下午
@Author  : Demon
@File    : ApiHDFS.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse
import os



class ApiHDFS(object):

    def __init__(self, token):
        # 部分接口未开放，暂不维护
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_adhoc/hdfs'

    def api_adhoc_hdfs_upload_file(self, file, user_name='demon_jiao'):
        """
        该用户当前历史查询并保存sql脚本
        :file 文件打开对象/路径
        """
        url = parse.urljoin(self.host, f'{self.root}/uploadFile?user={user_name}')
        if isinstance(file, str) and os.path.exists(file):
            with open(file, 'rb') as f:
                return send_api_request(method='post', url=url, paramType='file', paramData=f.read(), headers=self.headers)

        return send_api_request(paramType='file', paramData=file, method='post', url=url, headers=self.headers, )

