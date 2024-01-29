# coding=utf-8
# @Time    : 2022/9/6 10:28 上午
# @Author  : Karen
# @File    : test_gpen.py


import pytest
from business.goldenTouch.gpen.ApiGpen import ApiGpen
from config.env.domains import Domains
from business.common.UserProperty import UserProperty


@pytest.mark.goldenTouch
class TestGpen(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path('fat')
        # 设置域名host
        cls.dm.set_domain(cls.config['url'])

        cls.notBuy_user = ApiGpen(token=UserProperty(cls.config['goldenTouch']['notBuy_user']).basic_auth) # 13888888885 未购买用户
        cls.st99_user = ApiGpen(token=UserProperty(cls.config['goldenTouch']['st99_user']).basic_auth) # 18600000000 已购实体9.9用户


    def test_goldenTouch_gpen(self):
        """01 请求点读笔首页"""
        resp = self.st99_user.api_goldentouch_gpen_token()
        assert resp['code'] == 0
        assert resp['data']['userId'] != None
        assert resp['data']['thirdCode'] != None
