''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/4/24
===============
'''
import base64

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.mytab.possword import Possword
from business.Jiliguala.user.ApiUser import ApiUser
from business.businessQuery import usersQuery
import time




@pytest.mark.menu
class TestMytab(object):
    dm = Domains()

    def setup_class(cls):
        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('fat')  # 测试环境
        cls.dm.set_domain(cls.config['url'])  # 准备测试的url地址
        cls.user = ApiUser()
        cls.myBid = cls.config["center"]  # 读取所用到的bid
        cls.cocosEnv = cls.config["cocosEnv"]  # 读取cocos环境
        cls.CS_user = cls.config["CS_user"]  # 读取账户信息
        cls.token = cls.user.get_token(typ="mobile", u="11111130002", p="Jlgl168.")  # 登陆用户获取token
        cls.myapi = Possword(token=cls.token)
        current_timestamp = int(time.time() * 1000)
        auth_part = '2022090617204537dac25b2d811d716af3478aff70a2e70113ebf958de83b1:50b665b76488e1d3a565d3d05b63cc69'
        cls.pandora = base64.b64encode(f'{current_timestamp}:{auth_part}'.encode('utf-8'))
        print(current_timestamp)
          # 传入token

    def test01_sms_code(self):

        """
        修改密码获取验证码
        """
        resp = self.myapi.api_sms_code(pandora=self.pandora)
        assert resp["code"] == 0
        check.equal(resp["code"], 0)

    def test02_code(self):
        """
        输入验证码
        """
        code = usersQuery().get_users(mobile="11111130002")["sms"]["code"]
        resp = self.myapi.api_code(code=code,pandora=self.pandora)
        assert resp["code"] == 0
        check.equal(resp["code"],0)

    def test03_user(self):
        """
        修改密码
        """
        resp = self.myapi.api_user()
        assert resp["code"] == 0
