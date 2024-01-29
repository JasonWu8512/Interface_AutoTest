# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/21 5:35 下午
@Author  : Demon
@File    : TestindicatorEnum.py
"""

# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/26 8:15 下午
@Author  : Demon
@File    : TestTunnelEnums.py
"""

import pytest
from config.env.domains import Domains
from business.Elephant.ApiBasic.GetUserProper import GetUserProper
from business.Elephant.ApiRhinoSystem.ApiRhino.ApiReport import ApiReport

@pytest.mark.Elephant
class TestFunnelEnums(object):
    """

    """
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        # 测试环境的session
        cls.user = GetUserProper(user=cls.config['elephant']['user'], pwd=cls.config['elephant']['pwd'])
        cls.report = ApiReport(token=cls.user.token)

    def test_public_props(self):
        """
        指标分析中检查纬度对应的枚举值不为空则友好提示
        """
        for db, tb in self.report.api_report_fetch_all_source().get('data').items():
            for tbname in tb:
                enums = self.report.api_report_fetch_source_detail(dbname=db, tbname=tbname).get('data')
                # print(enums)
                for enum in enums:
                    if enum.get('columnDefine') == 'indicator' and enum.get('columnType') == 'string':
                        # col_enums = self.report.api_report_fetch_column_enum(
                        #     dbname=db, tbname=tbname, col=enum.get('columnName'))
                        # if col_enums.get('data'):
                        # print(col_enums)
                        print(db, tbname)
