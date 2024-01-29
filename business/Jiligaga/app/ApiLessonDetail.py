# -*- coding: utf-8 -*-
# @Time : 2022/6/24 下午1:54
# @Author : Saber
# @File : ApiLessonDetail.py

import email
import pytest
import lazy_property

from business.common.UserProperty import UserProperty
from config.env.domains import Domains

from testcase.Trade import order
from utils.requests.apiRequests import send_api_request


class ApiLesson ():
    """
    app  C端：课程详情页
    Lesson Controller
    """

    def __init__(self,token= None):
        self.dm = Domains()
        self.gaga_app = self.dm.set_env_path('fat')["gaga_app"]
        self.headers = {
            "authorization": token, "Content-Type": "application/json"
        }
        # 设置域名host
        self.host = self.dm.set_env_path('fat')["gaga_url"]

    def api_lesson_detail_v2(self, bid, lid):
        """
        课程详情页查询
        :param bid：宝贝id,课程id
        :return:
        """
        api_url = '/api/lesson/detail/v2'
        body = {
            "bid": bid,
            "lid":lid
        }
        resp = send_api_request (url=self.host + api_url, paramType='params', paramData=body, method='get',
                                  headers=self.headers )
        return resp


if __name__ == '__main__':
    # dm = Domains()
    # config = dm.set_env_path("fat")

    token = 'Basic NWI4ZWVhZmRkZmRlNGYwOWFjODk4MDgyZjBhNTMyYTI6M2Y2MmUzNWM5NGNjNGJiMGE2ODJmYjcxNTA4NWJkNTY6NUQxMURCNkItNzg4OC00OTk1LTg4OTEtQzNBOUM1NUVBNUI4'
    lessondetail = ApiLesson()
    #查询课程详情页
    resp = lessondetail.api_lesson_detail_v2(bid='2e009c7d83954ccbbb5a81281a733873', lid='12ade73d49813a0d8d3aedabf28c0fe6')
    print(resp)
