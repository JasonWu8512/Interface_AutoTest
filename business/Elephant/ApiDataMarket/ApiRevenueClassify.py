# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/24 4:57 下午
@Author  : Demon
@File    : ApiRevenueClassify.py
"""



from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse



class ApiRevenueClassify(object):

    def __init__(self, token):
        # 请求头文件
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain
        self.root = '/api_visual/revenueClassify'

    def api_get_revenue_classify(self, dates):
        """查询分类营收
        :param dates "2021-03-24"
        """
        url = parse.urljoin(self.host, f'{self.root}/getRevenueClassify')
        body = {
            "date": dates
        }
        return send_api_request(method='post', url=url, paramType='json', paramData=body, headers=self.headers)

