# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiBooks(object):
    """
    用户的book信息
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    # 获取word信息
    def api_get_books_word(self, book_id):
        """
        :param book_id:
        :return:
        """
        api_url = "/api/books/word"
        body = {
            "bookId": book_id
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp
