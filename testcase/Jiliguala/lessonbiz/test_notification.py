# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/7/20 7:51 下午
@Author   : Anna
@File     : test_notification.py
"""
from business.Jiliguala.lessonbiz.ApiNotification import ApiNotification
from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains
import pytest_check as check
import pytest


@pytest.mark.LessonBiz
class TestNotification(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化用户
        user = ApiUser()
        # 获取用户token信息
        cls.token = user.get_token(typ="mobile", u="19393112340", p="123456")
        cls.version = cls.config['version']['ver11.6']
        # 实例化ApiAddress类
        cls.notification = ApiNotification(cls.token, cls.version)

    # @pytest.mark.skip
    def test_post_notification(self):
        resp = self.notification.api_post_notification("赠送呱呱阅读vip卡", "xx", "JLGL://paidlist",
                                                       "c3319c0a6c054599b465c373b20e83a7")
        # 断言请求正常
        check.equal(resp["status_code"], 200)
        # 断言返回code码正常
        check.equal(resp["code"], 0)
        return resp


if __name__ == '__main__':
    notification = ApiNotification()
    notification.setup_class()
    notification.api_post_notification()
