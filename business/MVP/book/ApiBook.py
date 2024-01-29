# coding=utf-8
# @Time    : 2022/9/20 4:04 下午
# @Author  : Karen
# @File    : ApiBook.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiBook(object):
    ''' MVP用户领取免费VIP '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_books_mine_read(self,limit=20,page=0):
        """ 01）已读书籍列表 """
        api_url = "/api/books/mine/read"
        body = {
            "limit": limit,
            "page":page
            }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_books_mine_favorite(self,limit=20,page=0):
        """ 02）我的收藏书籍列表 """
        api_url = "/api/books/mine/favorite"
        body = {
            "limit": limit,
            "page": page
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_books(self,level,limit=20,page=0):
        """ 03）某个级别的绘本列表 """
        api_url = "/api/books"
        body = {"level": level,
                "limit": limit,
                "page": page
                }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_books_filters(self):
        """ 04）图书馆查找 """
        api_url = "/api/books/filters"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_books_album(self,albumId):
        """ 05）图书馆专辑详情页 """
        api_url = "/api/books/album"
        body = {"albumId": albumId}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_books_detail(self,bookId):
        """ 06）课程详情页 """
        api_url = "/api/books/detail"
        body = {"bookId": bookId}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp


    def api_book_collect(self,bookId):
        """ 07）收藏绘本 """
        api_url = "/api/books/mine/favorite"
        body = {"bookId": bookId}
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="json", method="post",
                                headers=self.headers)
        return resp


    def api_book_cancel_collect(self,bookId):
        """ 08）取消收藏绘本 """
        api_url = "/api/books/mine/favorite"
        body = {
            "bookId": bookId
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="params", method="delete",
                                headers=self.headers)
        return resp


    def api_book_progress(self,bookId,subLessonId,sections,words):
        """ 09）完课上报 """
        api_url = "/api/books/progress"
        body = {
            "bookId": bookId,
            "subLessonId": subLessonId,
            "sections": sections,
            "words": words
        }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="json", method="post",
                                headers=self.headers)
        return resp


    def api_book_progress_result(self,bookId,subLessonId):
        """ 10）完课结果页 """
        api_url = "/api/books/progress"
        body = {
            "bookId": bookId,
            "subLessonId": subLessonId
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp


    def api_books_word(self,bookId):
        """ 11）课程详情页核心单词 """
        api_url = "/api/books/word"
        body = {"bookId": bookId}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body,method="get", headers=self.headers)
        return resp