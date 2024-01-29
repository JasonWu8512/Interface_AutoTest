# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2022/04/25 2:29 下午
@Author   : Anna
@File     : test_resource.py
"""
import base64
from time import sleep

import pytest
import pytest_check as check

from business.Jiliguala.lesson.ApiPaid import ApiPaid
from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.Jiliguala.onboarding.ApiUseronboarding import ApiUseronboarding
from business.Jiliguala.pay.ApiShoppingTab import ApiShoppingTab
from business.Jiliguala.pay.ApiTrialClass import ApiTrialClass
from business.Jiliguala.reso.getportrait.ApiGet import ApiGet
from business.Jiliguala.systemlesson.ApiHome import ApiHome
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.userbiz.ApiUserCenter import ApiUserCenter
from business.Trade.tradeOrder.ApiOrderApi import ApiOrderApi
from business.businessQuery import usersQuery, pingxxorderQuery
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


class TestResource(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境变量
        cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化ApiSmsInfo类，用户登录调用
        cls.mobile = cls.config['regression']['re01']
        cls.mobile02 = cls.config['regression']['re02']
        cls.pwd = cls.config['regression']['pwd']
        cls.user = UserProperty(cls.mobile)
        # bid
        cls.bid = cls.config['regression']['bid']
        # 获取用户token信息
        cls.token = cls.user.basic_auth
        print(cls.token)
        # 实例化ApiSmsInfo类
        cls.sms = ApiSmsInfo(cls.token)

    """
    步骤：
    1.选择游客登录
    2.选择年龄
    3.登录成功，进入首页
    
    期望：
    首页展示体验课浮窗(9.9或者0元课)
    """

    def test_resource_0(self):
        """用户首页展示0元课浮窗"""
        user_login = self.sms.api_get_password(u=self.mobile, typ='mobile', p=self.pwd)
        bid = user_login['data']['b'][0]['_id']
        uid = user_login['data']['b'][0]['prt']
        tok = user_login['data']['tok']
        mobile = user_login['data']['mobile']
        print(tok)
        print(bid)
        print(uid)
        print(user_login)
        # 用户token信息
        code = base64.b64encode(f'{uid}:{tok}'.encode('utf-8'))
        auth01 = 'Basic ' + str(code, encoding="utf-8")

        """游客登录成功，检查首页，首页内容确认，展示体验营相关信息"""
        # 实例化首页，验证首页内容
        self.home = ApiHome(auth01)
        home = self.home.api_get_v4_home(bid)
        self.reso = ApiGet(auth01)
        print(self.reso)
        resource = self.reso.api_get_usertab(bid=bid, mod='engTab')
        print(resource)

        # 断言首页展示体验课浮窗
        assert resource['data'][0]['content']['title'] == '英语0元限时优惠'

    def test_resource_9(self):
        """用户首页展示9.9浮窗"""
        user_login = self.sms.api_get_password(u=self.mobile02, typ='mobile', p=self.pwd)
        bid = user_login['data']['b'][0]['_id']
        uid = user_login['data']['b'][0]['prt']
        tok = user_login['data']['tok']
        mobile = user_login['data']['mobile']
        print(tok)
        print(bid)
        print(uid)
        print(user_login)
        # 用户token信息
        code = base64.b64encode(f'{uid}:{tok}'.encode('utf-8'))
        auth01 = 'Basic ' + str(code, encoding="utf-8")

        """游客登录成功，检查首页，首页内容确认，展示体验营相关信息"""
        # 实例化首页，验证首页内容
        self.home = ApiHome(auth01)
        home = self.home.api_get_v4_home(bid)
        self.reso = ApiGet(auth01)
        print(self.reso)
        resource = self.reso.api_get_usertab(bid=bid, mod='engTab')
        print(resource)

        # 断言首页展示体验课浮窗
        assert resource['data'][0]['content']['title'] == '英语99限时优惠'
