# coding=utf-8
# @Time    : 2022/10/28 6:09 下午
# @Author  : Karen
# @File    : test_resource.py


import pytest
from business.MVP.resource.ApiResource import ApiResource
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from config.env.domains import Domains


@pytest.mark.MVP
class TestResource(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = g().get_guest_token()  # 创建游客并获取token
        ApiBaby(token=cls.guest_token).api_put_baby() # 创建宝贝
        cls.guest = ApiResource(token=cls.guest_token)  # 创建游客实例


    def test_get_lesson_package(self):
        """01）获取课程资源包"""
        resp = self.guest.api_resource_package_base()
        assert resp['code'] == 0
        assert resp['data'] != []

    def test_get_book_page(self):
        """02）获取课程内容图片"""
        resp = self.guest.api_resource_book_page('B0000000000001_cover')
        assert resp['code'] == 0
        assert resp['data'][0]['_id'] == 'B0000000000001_cover'
        assert resp['data'][0]['img'] == 'https://cdn.jiliguala.com/reading/page/cover/B0000000000001_cover.png?versionId=gSfXqCSp2TXpcL4_A1x478W5Eh8z.w0c'
