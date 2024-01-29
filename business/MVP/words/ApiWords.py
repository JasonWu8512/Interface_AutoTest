# coding=utf-8
# @Time    : 2022/9/20 6:18 下午
# @Author  : Karen
# @File    : ApiWords.py


from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty

class ApiWords(object):
    ''' 词句库相关 '''

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain


    def api_words_progress(self,source,records):
        """ 01）纠音上报 """
        api_url = "/api/words/progress"
        body = {
            "source": source,
            "records": records
                }
        resp = send_api_request(url=self.host + api_url, paramData=body, paramType="json", method="post",
                                headers=self.headers)
        return resp