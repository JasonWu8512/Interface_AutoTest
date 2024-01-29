# @Time    : 2021/4/1 5:08 下午
# @Author  : ygritte
# @File    : test_inner_admin

import pytest

from config.env.domains import Domains
from business.mysqlQuery import SaturnQuery
from business.sso.ApiSso import ApiSso
from business.saturn.ApiInnerAdmin import ApiInnerAdmin
from business.saturn.ApiChannel import ApiChannel
from business.saturn.ApiInnerLogin import ApiInnerLogin


class TestInnerAdmin:
    """
    运营商管理系统
    """
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.saturnquery = SaturnQuery()
        cls.channel = ApiChannel()  # 构建实例，用于测试代理商登录web系统的场景

    @classmethod
    def teardown_class(cls):
        """
        删除代理商和员工账号，恢复数据
        """
        # 删除新增代理商账号，恢复数据
        cls.saturnquery.delete_data("DELETE FROM saturn_user_accounts WHERE account_name = 'ygrAuto'")
        # 删除新增员工账号，恢复数据
        cls.saturnquery.delete_data('DELETE FROM saturn_user_accounts WHERE account_name = "miaomiao"')

    @pytest.fixture(scope="class")
    def get_sso_auth(self):
        """
        获取登录sso系统后的authCode和token
        """
        sso = ApiSso(email_address="ygritte_cao@jiliguala.com", pwd="UtlVAqpA")
        auth = sso.sso_code
        res = ApiInnerLogin().api_getInfo(authCode=auth)
        token = res['data']['token']
        admin = ApiInnerAdmin(admin_token=token)  # 构建运营管理系统的admin实例
        return admin

    @pytest.mark.parametrize("name, province, city, mobile, pwd",
                             [("ygrAuto", "陕西省", "宝鸡市", "15555577777", "1234567")])
    def test_add_manager(self, name, province, city, mobile, pwd, get_sso_auth):
        """
        新增代理商账号
        """
        res_manager_reg = get_sso_auth.api_admin_account_manager_register(name, province, city, mobile, pwd)
        # 新增的代理商可以正常登录
        res_login = self.channel.api_admin_login(username=name, password=pwd)
        assert res_manager_reg['msg'] == 'ok'
        assert res_login['data']['name'] == name

    @pytest.mark.parametrize("uuid, pwd, name, pwd2",
                             [("d2d213dd1fa349049e5ec5c9c7893c8c", "1234568", "ygrAuto1", "1234567")])
    def test_edit_manager(self, uuid, pwd, name, pwd2, get_sso_auth):
        """
        修改代理商密码
        """
        # 修改代理商的登录密码
        res_manager_edit = get_sso_auth.api_admin_account_edit(uuid, pwd)
        # 代理商用旧密码无法正常登录
        res_login = self.channel.api_admin_login(username=name, password=pwd2)
        assert res_manager_edit['msg'] == 'ok'
        assert res_login['msg'] == '登陆失败'

    @pytest.mark.parametrize("name, mobile, pwd, leaderUuid",
                             [("miaomiao", "18888877755", "1234567", "d338194d8f9e4573aeccce53a8a16688")])
    def test_add_staff(self, name, mobile, pwd, leaderUuid, get_sso_auth):
        """
        新增员工账号
        """
        # 新增员工账号
        res_staff_reg = get_sso_auth.api_admin_account_employee_register(name, mobile, pwd, leaderUuid)
        # 员工账号登录代理商系统
        res_login = self.channel.api_admin_login(username=name, password=pwd)
        assert res_staff_reg['msg'] == 'ok'
        assert res_login['data']['name'] == name

    @pytest.mark.parametrize("uuid, pwd, name, pwd2",
                             [("66c606e478a645cda73ae0237823afd3", "123459", "mimemie2", "1234567")])
    def test_edit_staff(self, uuid, pwd, name, pwd2, get_sso_auth):
        """
        修改员工账号密码 固定修改员工：mimemie2的密码
        """
        # 修改员工密码
        res_edit_staff = get_sso_auth.api_admin_account_edit(uuid, pwd)
        # 员工旧密码无法登录代理商系统
        res_login = self.channel.api_admin_login(username=name, password=pwd2)
        assert res_edit_staff['msg'] == 'ok'
        assert res_login['msg'] == '登陆失败'









