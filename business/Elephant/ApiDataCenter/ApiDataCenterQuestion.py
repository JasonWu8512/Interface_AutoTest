# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/25 1:25 下午
@Author  : Demon
@File    : ApiDataCenterQuestion.py
"""


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header

class ApiDataCenterQuestion(object):
    def __init__(self, token):
        """
        :param token: token
        """
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_basic/datacenter_question'

    def api_question_select(self):
        """
        查询问题解决描述信息
        :return :
        """
        api_url = self.host + f"{self.root}/question_select"
        return send_api_request(url=api_url, headers=self.headers, method="post")

    def api_question_add(self, user, typ, content, title):
        """
        增加解决描述信息
        :param user :用户名
        :param typ :问题类型
        :param content :问题内容正文
        :param title :问题标题
        :return :
        """
        body = {
            "user": user,
            "type": typ,
            "content": content,
            "title": title
        }
        api_url = self.host + f"{self.root}/question_add"
        return send_api_request(url=api_url, headers=self.headers, method="post", paramData=body, paramType='json')

    def api_question_update(self, uid, user, typ, content, title):
        """
        编辑问题解决描述信息
        :param uid :用户id
        :param user :用户名
        :param typ :问题类型
        :param content :问题内容正文
        :param title :问题标题
        :return :
        """
        body = {
            "id": uid,
            "user": user,
            "type": typ,
            "content": content,
            "title": title
        }
        api_url = self.host + f"{self.root}/question_update"
        return send_api_request(url=api_url, headers=self.headers, method="post", paramData=body, paramType='json')

    def api_question_del(self, article_id):
        """
        删除问题解决描述信息
        :param article_id :要删除的问题id
        :return :
        """
        body = {'id': article_id}
        api_url = self.host + f"{self.root}/question_del"
        return send_api_request(url=api_url, headers=self.headers, method="post", paramData=body, paramType='json')

    def api_question_select_id(self, article_id, title, typ):
        """
        根据问题id查询问题对应的content信息
        :param article_id :要查询的问题id
        :return :
        """
        body = {
            'id': article_id,
            'title': title,
            'type': typ
        }
        api_url = self.host + f"{self.root}/question_select_id"
        return send_api_request(url=api_url, headers=self.headers, method="post", paramData=body, paramType='json')
