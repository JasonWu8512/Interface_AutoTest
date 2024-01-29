# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2023/02/21 2:29 下午
@Author   : Anna
@File     : test_c_buy.py
"""
import base64
import os
import time

import pytest
import pytest_check as check

from business.Jiliguala.lessonbiz.ApiSuper import ApiSuper
from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.Jiliguala.sc.ApiList import ApiList
from business.Jiliguala.sc.ApiScAlbum import Apialbum
from business.Jiliguala.sc.ApiScBuy import ApiScBuy
from business.Jiliguala.sc.ApiScLesson import ApiScLesson
from business.common.UserProperty import UserProperty
from config.env.domains import Domains


class TestCBuy(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # 【代码提交用】获取环境变量
        cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        print(env)
        # # 本地调试用，环境变量
        # cls.config = cls.dm.set_env_path('fat')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        # 实例化ApiSmsInfo类，用户登录调用
        cls.mobile = cls.config['regression']['mobile_c']
        cls.pwd = cls.config['regression']['pwd']
        cls.user = UserProperty(cls.mobile)
        # 获取用户token信息
        cls.token = cls.user.basic_auth
        print(cls.token)
        # 实例化ApiSmsInfo类
        cls.sms = ApiSmsInfo(cls.token)
        # 实例化购买TAB
        cls.version = cls.config['version']['ver11.17.0']
        cls.agent = cls.config['User-Agent']['ios_11.17.0']
        # 实例化ApiList 专辑列表页
        cls.scList = ApiList(cls.token)
        # 实例化Apialbum 专辑详情页
        cls.scAlbum = Apialbum(cls.token)
        # 实例化ApiScLesson 课程详情页
        cls.scLesson = ApiScLesson(cls.token)
        # 实例化ApiScBuy 课程专辑购买
        cls.scBuy = ApiScBuy(cls.token)
        # C类专辑名称
        cls.albumId = cls.config['regression']['albumId']
        # C类课程名称
        cls.lessonId = cls.config['regression']['lessonId']

    """
    步骤：
    1.用户密码登录
    2.进入拓展tab
    3.选择全部专辑区
    4.选择趣味拓展资源
    5.【趣味拓展资源】列表，选择杰克与魔豆
    6.点击立即购买
    7.购买选择页面，选择购买本节
    8.购买本节
   
    返回：
    1.登录成功
    2.拓展tab接口返回全部专辑区相关内容
    3.全部专辑区，返回趣味拓展相关内容
    4.趣味拓展列表展示正常，返回杰克与魔豆相关内容
    5.杰克与魔豆专辑介绍页，返回相关内容
    6.购买选择页面，返回购买须知及相关专辑信息
    8.可购买成功
        -趣味拓展资源页面，已拥有1节
        -我的学习内容处，新增趣味拓展相关内容
    """

    def test_c(self):
        """c类课程购买"""
        # time.sleep(10)
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

        # 断言登录成功
        assert user_login['data']['mobile'] == self.mobile
        # 进入专辑列表页
        cList = self.scList.api_list()
        print(cList)
        # 断言拓展tab接口返回全部专辑区相关内容
        assert cList['data']['albums'][00]['ttl'] == '叽里呱啦趣味拓展资源'

        # 选择全部专辑区-趣味拓展资源
        cAlbum = self.scAlbum.api_album(bid, self.albumId)
        print(cAlbum)
        # 断言趣味拓展列表展示正常，返回玩具面对面相关内容
        assert cAlbum['data']['lessons'][2]['cttl'] == '寻找魔法糖果'

        # 【趣味拓展资源】列表，选择寻找魔法糖果
        cLesson = self.scLesson.api_lesson(bid, lessonId=self.lessonId, albumId=self.albumId)
        print(cLesson)
        # 断言寻找魔法糖果专辑介绍页，返回相关内容
        assert cLesson['data']['cttl'] == '寻找魔法糖果'

        # 点击立即购买
        # 进入C类购买页
        cBuy = self.scBuy.api_buy(lessonId=self.lessonId, albumId=self.albumId)
        print(cBuy)
        c_price = cBuy['data']['items'][0]['finalAmount']
        # 下单
        # 实例化购买相关接口
        self.super = ApiSuper(auth01, self.agent)
        order01 = self.super.api_get_Corder(bid=bid, channel="wx", guadou=int(c_price), itemid=self.lessonId)
        print(order01)
        id01 = order01['data']['id']
        print(id01)
        time_paid = order01['data']['created']
        order_no = order01['data']['order_no']
        current_timestamp = int(time.time() * 1000)
        print(current_timestamp)
        transaction_no = 'MOCK4200001986' + str(current_timestamp)
        print(transaction_no)
        mock01 = self.super.api_post_mock(id01, time_paid,order_no,transaction_no)
        print(mock01)
        # 查询趣味拓展列表，已拥有1/52
        af_cAlbum = self.scAlbum.api_album(bid, self.albumId)
        assert af_cAlbum['data']['has'] == 1
        # 还原数据
        self.super.api_post_refund(order_no)
        time.sleep(10)
        # 断言已拥有=0
        af_cAlbum = self.scAlbum.api_album(bid, self.albumId)
        assert af_cAlbum['data']['has'] == 0
