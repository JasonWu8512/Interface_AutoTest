"""
=========
Author:Lisa
time:2022/10/24 6:22 下午
=========
"""
import os

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiligaga.app.ApiPurchaseCommoditySpu import ApiPurchaseCommoditySpu
from business.Jiligaga.app.ApiLogin import Login
from utils.middleware.dbLib import MySQL


@pytest.mark.GagaReg
class TestApiPurchaseCommoditySpu:
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 从环境变量获取env
        # env = os.environ.get ( 'fat' )
        # 本地调试环境
        cls.config = cls.dm.set_env_path ( 'fat' )
        # print ( env )
        # 获取环境链接
        cls.dm.set_domain ( cls.config['url'] )
        print ( cls.config['url'] )

        # cls.dm = Domains()
        # # 获取环境
        # cls.gaga_app = cls.dm.set_env_path()
        # cls.config = cls.dm.set_env_path()
        cls.login = Login()
        # 实例化ApiPurchaseCommoditySpu类
        cls.apipurchasecommodityspu = ApiPurchaseCommoditySpu()
        # 获取配置文件中的spuNo信息
        cls.spuNo = cls.config['gaga_app']['spuNo']
        # cls.spuNo=cls.config['gaga_app']['spuNo_renzhuan']
        cls.countryCode=cls.config['gaga_app']['countryCodeTw']
        cls.countryCode1=cls.config['gaga_app']['countryCodeTw']
        # print(cls.spuNo)

    def test_purchase_commodity_spu(self):
        """机转-获取一个spu商品"""
        spuNo = self.spuNo
        countryCode=self.countryCode
        self.apipurchasecommodityspu = ApiPurchaseCommoditySpu()
        resp = self.apipurchasecommodityspu.purchase_commodity_spu(spuNo, countryCode)
        check.equal(resp["code"], 0)

    def test_purchase_commodity_spu(self):
        """人转-领取后商品推荐"""
        spuNo = self.spuNo
        countryCode=self.countryCode1
        self.apipurchasecommodityspu = ApiPurchaseCommoditySpu()
        resp = self.apipurchasecommodityspu.purchase_commodity_spu_renzhuan(spuNo, countryCode)
        # check.equal(spuNo, 'spuNo')
        check.equal(resp["code"], 0)
        # 调试数据库
        # mysql = MySQL ( pre_db='jlgg', db_name='user' )
        # print ( mysql.query ( "SELECT * FROM t_spu where spu_no='CP48363575'" ))