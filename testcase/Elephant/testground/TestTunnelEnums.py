# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/26 8:15 下午
@Author  : Demon
@File    : TestTunnelEnums.py
"""

import pytest
import pytest_check as check
import pandas as pd
from config.env.domains import Domains
from business.Elephant.ApiBasic.GetUserProper import GetUserProper
from business.Elephant.ApiRhinoSystem.ApiFunnel.ApiFunnelEvent import ApiFunnelEvent
from business.Elephant.ApiFeishu.ApiDemand import ApiDemand

@pytest.mark.Elephant
class TestFunnelEnums(object):
    """
    每期时间属性校验
    """

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        # 测试环境的session
        cls.user = GetUserProper(user=cls.config['elephant']['user'], pwd=cls.config['elephant']['pwd'])
        cls.funnel_event = ApiFunnelEvent(token=cls.user.token)

    @pytest.mark.parametrize("product_ids", ["jlgl"])
    def test_events_check(self, product_ids):
        """
        校验增加的所有的事件的正确
        """
        events = self.funnel_event.api_funnel_fetch_all_events(product_ids=product_ids)
        df = pd.read_excel('/Users/bianhua/test/groundhog/漏斗分析.xlsx', sheet_name='一期事件表', skiprows=1).fillna(method='ffill')
        df = df[df['Event Name'].notnull()]  # 一期事件不做event_name不存在的
        # df['事件分类'] = df['事件分类'].fillna(method='ffill')
        print(df.head())
        # print(df[df['事件分类'] == '通用属性']['Event Description'].tolist())
        for child in events.get("data"):
            if child.get('id') == product_ids:
                apps = [_['id'] for _ in child['children'][0]['children'] if _['parentId'] == 'app']
                print(sorted(apps), sorted(df['事件分类'].unique().tolist()))
                # 获取属性枚举值并校验
                for eve in child['children'][0]['children']:
                    if eve['parentId'] == 'app':
                        for eventid in eve['children']:
                            data_props = self.funnel_event.api_funnel_fetch_event_props(event_id=eventid['id'])
                            df_prop = df[df['Event Name'] == eventid['id']]
                            left = df_prop['Property'].unique().tolist()
                            right = [prop['columnComment'] for prop in data_props.get('data')]
                            if set(right).difference(set(left)):
                                # Teaching Assistant Add Dialog Click {'URL'}
                                # Item Purchase View {'State'}
                                print(eventid['id'], set(right).difference(set(left)))

    def test_public_props(self):
        """
        公共属性校验
        """
        for props in self.funnel_event.api_funnel_fetch_public_props().get('data')['userProperties']:
            enums = self.funnel_event.api_funnel_fetch_column_info(column=props['column']).get('data')['enums']
            print(f'当前属性：{props["columnComment"]}: {len(enums)}')

    def test_event_columns_info(self):
        """
        公共属性校验
        """
        events = self.funnel_event.api_funnel_fetch_all_events(product_ids='jlgl')

        # print(df[df['事件分类'] == '通用属性']['Event Description'].tolist())
        sd = set()
        for child in events.get("data"):
            if child.get('id') == 'jlgl':
                for eve in child['children'][0]['children']:
                    for eventid in eve['children']:

                        for d in self.funnel_event.api_funnel_fetch_event_props(event_id=eventid['id']).get('data'):

                            sdpl = self.funnel_event.api_funnel_fetch_column_info(
                                column=d["column"],
                                event_keys=['jlgl', 'app', eve['id'], eventid['id']],
                                typ='event'
                            )
                            # print(sdpl)
                            sd.add(sdpl.get('data')['type'])
        print(sd)

