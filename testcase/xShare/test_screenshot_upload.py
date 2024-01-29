# coding=utf-8
# @Time    : 2021/3/22 11:07 上午
# @Author  : qilijun
# @File    : test_screenshot_upload.py

from business.common.UserProperty import UserProperty
from business.xshare.ApiScreenShot import ApiScreenShot
from config.env.domains import Domains


class TestScreenshotUpload(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path('fat')
        # 设置域名host
        cls.dm.set_domain(cls.config['url'])

        # 初始化不同身份用户
        cls.gmkEnglish_user = UserProperty(cls.config['xshare']['gmkEnglish_user'])  # 构建英语正价课用户user实例
        cls.gmkMath_user = UserProperty(cls.config['xshare']['gmkMath_user'])  # 构建思维正价课用户user实例
        cls.promoter_user = UserProperty(cls.config['xshare']['promoter_user'])  # 构建推广人用户user实例
        cls.refunded_user = UserProperty(cls.config['xshare']['refunded_user'])  # 构建正价课退款用户user实例
        cls.new_user = UserProperty(cls.config['xshare']['new_user'])  # 构建未购课用户user实例

        cls.auth_token = cls.gmkEnglish_user.basic_auth
        cls.user_id = cls.gmkEnglish_user.user_id
        cls.screen_shot = ApiScreenShot(auth_token=cls.auth_token)

    def test_check_gmkEnglish_user(self):
        """
        英语正价课非推广人账号，登录成功
        """
        auth_token = self.gmkEnglish_user.basic_auth
        screenshot = ApiScreenShot(auth_token=auth_token)
        check_resp = screenshot.api_check()
        assert check_resp['code'] == 0
        assert check_resp['data']['qualified'] == True

    def test_check_gmkMath_user(self):
        """
        思维正价课非推广人账号，登录成功
        """
        auth_token = self.gmkMath_user.basic_auth
        screenshot = ApiScreenShot(auth_token=auth_token)
        check_resp = screenshot.api_check()
        assert check_resp['code'] == 0
        assert check_resp['data']['qualified'] == True

    def test_check_promoter_user(self):
        """
        推广人账号，登录成功
        """
        auth_token = self.promoter_user.basic_auth
        screenshot = ApiScreenShot(auth_token=auth_token)
        check_resp = screenshot.api_check()
        assert check_resp['code'] == 0
        assert check_resp['data']['qualified'] == True

    def test_check_notGmkPromoter_user(self):
        """
        非正价课非推广人账号，登录失败
        """
        auth_token = self.new_user.basic_auth
        screenshot = ApiScreenShot(auth_token=auth_token)
        check_resp = screenshot.api_check()
        assert check_resp['code'] == 45001

    def test_check_refunded_user(self):
        """
        正价课退款非推广人账号，登录失败
        """
        auth_token = self.refunded_user.basic_auth
        screenshot = ApiScreenShot(auth_token=auth_token)
        check_resp = screenshot.api_check()
        assert check_resp['code'] == 45001
