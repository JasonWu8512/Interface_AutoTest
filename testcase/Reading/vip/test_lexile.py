# coding=utf-8
import pytest
import pytest_check as check

from config.env.domains import Domains
from business.common.UserProperty import UserProperty
from business.Reading.vip.ApiRedeem import ApiRedeem
from business.Reading.vip.ApiLexile import ApiLexile


@pytest.mark.ggrVip
class TestVip(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])
        cls.mobile = cls.config['reading_account']['user']
        user = UserProperty(cls.mobile)
        cls.token = user.basic_auth
        cls.lexile = ApiLexile(token=cls.token)

    def test_api_lexile(self):
        """测试蓝思首页&做蓝思测试"""
        # 生成兑换码
        # user1 = UserProperty(self.config['admin_account']['user'])
        # token1 = user1.basic_auth
        # redeem1 = ApiRedeem(token=token1)
        # res = redeem1.api_circulars_redeem("LexileTestOnce_180")
        # code = res['data']['code'][0]
        # # 兑换
        # redeem2 = ApiRedeem(token=self.token)
        # r = redeem2.api_redeem_exchange(code)
        # print(r)
        # resp = self.lexile.api_get_lexile_home()
        # check.equal(resp["code"], 0)
        # chance_id = resp["data"]['validChance']['id']
        # check.not_equal(chance_id, '')
        # print(resp)
        # # 提交
        # resp1 = self.lexile.api_lexile_submit(chance_id)
        # check.equal(resp1["code"], 0)
        # print(resp1)
        # # 注销兑换码
        # redeem1.api_redeem_refund(code)
        pass #蓝思测试已下线







