# coding=utf-8
# @Time    :
# @Author  : anna
import os

import pytest
import pytest_check as check
import hypothesis
import time
import base64

from business.Jiliguala.internal.ApiInternal import ApiInternal
from business.Jiliguala.onboarding.ApiSms import ApiSmsInfo
from business.Jiliguala.onboarding.ApiUseronboarding import ApiUseronboarding
from business.Jiliguala.systemlesson.ApiHome import ApiHome
from business.Jiliguala.systemlesson.ApiPage import ApiPage
from business.businessQuery import usersQuery
from config.env.domains import Domains
import logging
from business.Jiliguala.user.ApiUser import ApiUser
import datetime


@pytest.mark.Login
class TestSms(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # # 【代码提交用】从环境变量获取env
        # env = os.environ.get('env')
        # # 【代码提交用】获取环境变量
        # cls.config = cls.dm.set_env_path(env)
        # # 【代码提交用】
        # print(env)
        # 本地调试用
        cls.config = cls.dm.set_env_path('prod')
        # 获取环境链接
        cls.dm.set_domain(cls.config['url'])
        print(cls.config['url'])
        # 实例化用户
        # user = ApiUser()
        # 获取用户token信息
        # cls.token = user.get_token(typ="mobile", u="11100000001", p="123456")
        cls.version = cls.config['version']['ver11.34.0']
        cls.anVersion = cls.config['anVersion']['ver1']
        cls.xApp = cls.config['xApp']['xApp01']
        # 实例化ApiSmsInfo类
        cls.sms = ApiSmsInfo(version=cls.version, anVersion=cls.anVersion, xApp=cls.xApp)
        # cls.mobile = '11100000001'
        # pandora 自动生成，根据当前时间戳:+固定字段然后base64加密
        current_timestamp = int(time.time() * 1000)
        auth_part = '2022090617204537dac25b2d811d716af3478aff70a2e70113ebf958de83b1:50b665b76488e1d3a565d3d05b63cc69'
        cls.pandora = base64.b64encode(f'{current_timestamp}:{auth_part}'.encode('utf-8'))
        print(current_timestamp)
        print(cls.pandora)
        cls.agent = cls.config['User-Agent']['ios_11.34.0']
        cls.onboard = ApiUseronboarding(cls.version, cls.agent)
        # 宝贝年龄
        cls.birth = cls.config['regression']['birth']
        # 宝贝昵称
        cls.nick = cls.config['regression']['nick']
        cls.pageInfo = ApiPage()
        # 内部接口实例化
        cls.internal = ApiInternal()
        cls.anch = cls.config['regression']['anch']
        cls.anver = cls.config['regression']['anver']
        # 打印日志
        cls.logger = logging.getLogger(__name__)

    """
    【游客登录】
    步骤：
    1.选择游客登录，接口返回正常
    2.选择年龄，开始学习，进入首页，相关接口正常返回
    
    结果：
    1.断言接口返回："typ": "guest"
    2.断言接口返回：digitalVersionImage": "https://h5.jiliguala.com/activity/a6d9da92ac671e067d834568ae8bb4c2.png
    """

    def test_put_guest(self):
        """游客登录成功"""
        guest = self.sms.api_put_guest()
        print(guest)
        # 断言游客，可正常登陆
        check.equal(guest['data']['typ'], 'guest')
        uid = guest['data']['_id']
        tok = guest['data']['tok']
        code = base64.b64encode(f'{uid}:{tok}'.encode('utf-8'))
        auth01 = 'Basic ' + str(code, encoding="utf-8")
        print("uid", uid)
        # 打印用户uid
        self.logger.info(uid)
        print("tok", tok)
        print("code", code)
        print("auth01", auth01)

        """获取数字版权信息"""
        pageInfo = self.pageInfo.api_page()
        print(pageInfo)
        # 断言数字版权信息
        image = 'https://h5.jiliguala.com/activity/a6d9da92ac671e067d834568ae8bb4c2.png'
        check.equal(pageInfo['data']['digitalVersionInfo']['digitalVersionImage'], image)

        """ 登录 """
        bd = self.onboard.api_user_onboarding(self.nick, self.birth, auth01)
        bid = bd['data']['_id']
        print(bid)
        # 断言接口返回游客登录时的uid
        check.equal(bd['data']['prt'], uid)

        """游客登录成功，检查首页，首页内容确认，展示体验营相关信息"""
        # 实例化首页，验证首页内容
        self.home = ApiHome(auth01)
        home = self.home.api_get_v4_home(bid)
        # 断言首页推荐的是英语体验营---待确认，为啥推荐的不是年课
        assert home['data']['roadmap']['elements'][1]['weekTitle'] == '体验营'

    """
    【新用户-验证码注册】
    步骤：
    1.验证码登录，接口返回正常
    2.输入验证码后登录，接口返回手机号与传参一致
    3.选择年龄登录，开始学习，进入首页，相关接口正常返回
    
    
    """

    def test_post_login_success(self):
        """新用户-验证码注册登录成功"""
        # pandora = "MTY1NTc5MzQ2NDIwODoyMDIwMDUxNDE1MDgxOWUzOWU2YzExMDNlYzExZTA0NTg4ODY4ZDY2MDM4MWM3MDFiNmE4MjY3ZGM5MWJkNToxNzEzY2YwNzE2MmM2MzE5ZmRmOTNkYzFmYWVmMmEzYg=="
        print(1, self.pandora)
        # 生成随机用户
        mobile_get = self.internal.api_get_mobile()
        mobile = mobile_get['data']
        print(mobile)
        # 点击获取验证码
        resp01 = self.sms.api_get_login_v2(mobile, self.pandora)
        print(resp01)
        uid = resp01['data']['uid']

        # 通过内部接口查验证码
        sms01 = self.internal.api_get_smsByID(uid)
        print(sms01)
        code = sms01['data']['sms']['code']
        print(code)

        resp02 = self.sms.api_post_login_v2(mobile, self.pandora, uid, code)
        print(resp02)
        # 断言，登陆成功
        check.equal(resp02['code'], 0)
        tok = resp02['data']['tok']
        code = base64.b64encode(f'{uid}:{tok}'.encode('utf-8'))
        auth01 = 'Basic ' + str(code, encoding="utf-8")
        print(auth01)

        """获取数字版权信息"""
        pageInfo = self.pageInfo.api_page()
        print(pageInfo)
        # 断言数字版权信息
        image = 'https://h5.jiliguala.com/activity/a6d9da92ac671e067d834568ae8bb4c2.png'
        check.equal(pageInfo['data']['digitalVersionInfo']['digitalVersionImage'], image)

        """ 登录 """

        bd = self.onboard.api_user_onboarding(self.nick, self.birth, auth01)
        bid = bd['data']['_id']
        # 打印用户uid
        self.logger.info(uid)
        print(bid)
        # 断言接口返回游客登录时的uid
        check.equal(bd['data']['prt'], uid)

        """游客登录成功，检查首页，首页内容确认，展示体验营相关信息"""
        # 实例化首页，验证首页内容
        self.home = ApiHome(auth01)
        home = self.home.api_get_v4_home(bid)
        # 断言首页推荐的是英语体验营---待确认，为啥推荐的不是年课
        assert home['data']['roadmap']['elements'][1]['weekTitle'] == '体验营'

        # 心跳监测接口正常
        ping01 = self.sms.api_post_ping()
        print(ping01)
        # 断言接口返回："code": 0
        check.equal(ping01['code'], 0)

        # 全局用户信息接口正常
        globe = self.home.api_get_globe(anch=self.anch, anver=self.anver, bid=bid)
        print(globe)
        # 断言接口返回："bd"--宝贝年龄，和选择年龄接口传参一致；“prt”=/api/users/guest/v2中返回的u
        formatted_dt = '2018-11-22T00:00:00.000Z'
        check.equal(globe['data']['user']['b'][0]['bd'], formatted_dt)
        check.equal(globe['data']['user']['b'][0]['prt'], uid)

        # 查看用户拥有sgu
        ownsgu01 = self.home.api_get_ownsgu()
        print(ownsgu01)
        check.equal(ownsgu01['code'], 0)
        time.sleep(9)


if __name__ == '__main__':
    pytest.main()
    print()
