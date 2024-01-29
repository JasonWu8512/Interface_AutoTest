''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/1/6
===============
'''

import os
import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.expandTab.expandApi import Apiexpand
from business.Jiliguala.user.ApiUser import ApiUser
from business.Jiliguala.userbiz.ApiDeleteDevices import DeleteDevices


@pytest.mark.menu
class Testexpand(object):
    dm=Domains()

    @classmethod
    def setup_class(cls):
        # 【代码提交用】从环境变量获取env
        env = os.environ.get('env')
        # 【代码提交用】获取环境变量
        cls.config = cls.dm.set_env_path(env)
        # 【代码提交用】
        print(env)
        cls.dm = Domains()
        # cls.config = cls.dm.set_env_path('fat')      # 测试环境
        cls.dm.set_domain(cls.config['url'])         # 准备测试的url地址
        cls.user = ApiUser()
        cls.expandBid = cls.config["expandTab"]       # 读取所用到的bid
        cls.cocosEnv = cls.config["cocosEnv"]              # 读取cocos环境
        cls.CS_user = cls.config["CS_user"]          # 读取账户信息
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])    # 登陆用户获取token
        cls.token1 = cls.user.get_token(typ="mobile", u="11111130149", p="Jlgl168.")                  #获取年课账户登陆token
        cls.expandapi = Apiexpand(token=cls.token)   # 传入token
        cls.expandapi1 = Apiexpand(token = cls.token1)
        cls.SC_tableYK = cls.config["SC_tableYK"]
        cls.user = DeleteDevices()
        cls.token2 = cls.user.get_token()          #获取游客登陆token
        cls.expandapi2 = Apiexpand(token = cls.token2)    #传入游客登陆token


    def test01_Tzxq(self):
        """
        拓展tab详情页
        """
        resp = self.expandapi.api_Tztab(self.expandBid["bid"])
        check.equal(resp["code"], 0)
        # assert resp["data"]["childsong"]['level'] == 'S1GE'
        assert resp["data"]["entrances"][0]["name"] == "0-1岁亲子陪伴资源"
        assert resp["data"]["entrances"][1]["name"] == "口语交流室"

    def test02_Tzer(self):
        """
        拓展tab儿歌电台
        """
        resp = self.expandapi.api_Tzeg()
        check.equal(resp["code"],0)
        assert resp["data"][0]["ttl"] == "泛听电台2" or "泛听电台"

    def test03_Tzer_list(self):
        """
        电台列表
        """
        resp = self.expandapi.api_Tzer_list(self.expandBid["bid"])
        check.equal(resp["code"],0)

    def test04_Tzky(self):
        """
        每日口语
        """
        resp = self.expandapi.api_tzky()
        check.equal(resp["code"],0)

    def test05_Tzch(self):
        """
        每日词汇
        """
        resp = self.expandapi.api_TZch()
        check.equal(resp["code"],0)
        assert resp["data"]["cards"][0]["word"] == "Zebra" or "zebra"

    def test06_Tzch_list(self):
        """
        每日口语列表
        """
        resp = self.expandapi.api_TZch_list()
        check.equal(resp["code"],0)
        assert resp["data"]["cards"][0]["cword"] == "苹果" or "海狮"

    def test07_Tz_gsh(self):
        """
        拓展故事会
        """
        resp = self.expandapi.api_TZ_gsh()
        check.equal(resp["code"],0)
        assert resp["data"][0]["ttl"] == "生活百科"

    def test08_Tzgsh_list(self):
        """
        拓展故事会列表
        """
        resp = self.expandapi.api_TZgsh_list(self.expandBid["bid"])
        check.equal(resp["code"],0)
        assert resp["status_code"] == 200

    def test09_Tz_sc(self):
        """
        点击拓展tab全部专辑区
        """
        resp = self.expandapi.api_sc()
        check.equal(resp["code"],0)
        assert resp["data"]["albums"][0]["_id"] == 'AlbumCIX001'
        assert resp["data"]["albums"][0]["desc"] == '拓展资源在家上'

    def test10_Tzsc_kc(self):
        """
        拓展tab点击全部资源区课程
        """
        resp = self.expandapi.api_sc_kc(self.expandBid["bid"])
        check.equal(resp["code"],0)
        assert resp["data"]["_id"] == 'AlbumCDS009'
        assert resp["data"]["ttl"] == '迪士尼公主系列（下）'              # 学习的课程

    def test11_Tz_junior(self):
        """
        拓展资源亲子早教资源
        """
        resp = self.expandapi.api_junior(self.expandBid["bid"])
        check.equal(resp["code"],0)
        assert resp["data"]["meta"]["pg"]["name"] == "亲子陪伴资源"

    def test12_Tz_course(self):
        """
        拓展tab点击学习亲子早教资源课程
        """
        resp = self.expandapi.api_course(self.expandBid["bid"])
        check.equal(resp["code"],0)
        assert resp["data"]["id"] == 'A1PG045'                    # 学习的第45节课程
        assert resp["data"]["cnTitle"] == "高贵的约克公爵"           # 断言学习的课程

    def test13_Tz_byGameId(self):
        """
        口语交流室
        """
        resp = self.expandapi.api_byGameld(self.cocosEnv["Env"])
        check.equal(resp["code"],0)

    def test14_Tz_byGameId_ggxw(self):
        """
        呱呱小屋
        """
        resp = self.expandapi.api_byGameId_ggxw(self.cocosEnv["Env"])
        check.equal(resp["code"],0)

    def test15_Tz_byGameId_home(self):
        """
        呱呱小屋主页
        """
        resp = self.expandapi.api_byGameId_home(self.expandBid["bid"])
        check.equal(resp["code"],0)
        assert resp["data"]["lv"] == 9 or 1

    def test16_Tz_smartreview_home(self):
        """
        智能闯关
        """
        resp = self.expandapi.api_smartreview_home(self.expandBid["bid"])
        check.equal(resp["code"],0)
        # assert resp["data"][2]["status_code"] == 200


    def test17_childsong(self):
        """
        年课用户每日儿歌
        """
        resp = self.expandapi1.api_childsong(self.expandBid["bid1"],self.expandBid["level"])
        check.equal(resp["code"],0)
        assert resp["data"]["levels"][0]["ttl"] == "Y1"

    def test18_table(self):
        """
        游客拓展tab页
        """
        resp = self.expandapi2.api_table(self.SC_tableYK['bid'])
        check.equal(resp["code"], 0)
        # assert resp["data"]["childsong"]['level'] == 'S1GE'
        assert resp["data"]["entrances"][0]["name"] == "0-1岁亲子陪伴资源"
        assert resp["data"]["entrances"][1]["name"] == "口语交流室"
