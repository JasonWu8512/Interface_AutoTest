# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/3 10:37 上午
@Author  : Demon
@File    : test_user_props.py
"""
import pytest
import pandas as pd
from config.env.domains import Domains
from business.Elephant.ApiBasic.GetUserProper import GetUserProper
from business.Elephant.ApiRhinoSystem.ApiEventConfig.ApiEventConfig import ApiEventConfig

@pytest.mark.Elephant
class TestFunnelEnums(object):
    """

    """
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        # 测试环境的session
        cls.user = GetUserProper(user=cls.config['elephant']['user'], pwd=cls.config['elephant']['pwd'])
        cls.report = ApiEventConfig(token=cls.user.token)

    def test_events_config(self):
        ans = self.report.api_fetch_all_events(project_id='60ec0af9445c46269716a597dcb07ba5')
        print(ans)
        c = 0
        df = pd.read_csv('/Users/bianhua/Downloads/埋点V1.1 最终确认版 -给开发 - 事件-事件属性（兰兰）.csv')
        print(len(set(df['事件（英文名）'].tolist())))
        # for enent in ans.get('data'):
        #     for child in enent.get('children'):
        #         key = child.get('key')
        #         c += 1
        # print(c)

