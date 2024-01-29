# -*- coding: utf-8 -*-
"""
@Time    : 2020/11/23 1:26 下午
@Author  : Demon
@File    : test_check_report.py
"""

import pytest
import random
import itertools
import jsonpatch
import pandas as pd
# from numpy import NaN
from utils.db_helper import DB
# from utils.middleware.dbLib import MySQL
from config.env.domains import Domains
from testcase.Elephant.report_sql import ground_sql
from business.Elephant.ApiRhinoSystem.ApiRhino.ApiReport import ApiReport
from business.Elephant.ApiBasic.GetUserProper import GetUserProper
from business.Elephant.ApiElephant.back_off_get_result import BackOffQuery
from testcase.Elephant.report_config import is_random, SqlIndicators, FilterConfig, generate_date_range



@pytest.mark.Elephant
class TestReport(object):
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        cls.user = GetUserProper(user=cls.config['elephant']['user'], pwd=cls.config['elephant']['pwd'])
        cls.report = ApiReport(cls.user.token)
        cls.db = DB('dev')
        # cls.db = MySQL('xelephant_dev')
        cls.dbtbs = ('jlgl_rpt', 'rpt_lesson_lesson_complete_total_all_d')
        # 初始化该类表下的所有维度和指标数据
        cls.source_details = cls.report.api_report_fetch_source_detail(
            dbname=cls.dbtbs[0],
            tbname=cls.dbtbs[1]
        ).get('data')
        cls.dimensions = [_ for _ in filter(lambda x: x['columnDefine'] == 'dimension', cls.source_details)]
        # {'columnType': 'double', 'columnDefine': 'indicator', 'columnComment': '\xe6', 'columnName': 'after_amount'
        cls.indicators = [_ for _ in filter(lambda x: x['columnDefine'] == 'indicator', cls.source_details)]
        # 初始化每个维度对应的枚举值 {"维度名1":['' , '' ]}
        cls.dimensions_enum = {}
        for col in cls.dimensions:
            e = cls.report.api_report_fetch_column_enum(
                dbname=cls.dbtbs[0],
                tbname=cls.dbtbs[1],
                col=col['columnName']
            ).get('data')
            # 有的接口里数据类型不对，枚举值对应null
            cls.dimensions_enum[col['columnName']] = e if e else []

    def get_indicators(self, indicator_num=1, arith=None, line='line'):
        """
        生成指标计算列表配置
        :param indicator_num :统计的指标的个数
        :param arith :自定义函数
        :return 返回生成好的indatiors 传参
        """
        if not indicator_num:
            raise Exception("未添加指标")
        random_indicor = random.sample(self.indicators, indicator_num)
        sin = SqlIndicators(line=line)
        indicators, opfs = [], []
        for colum in random_indicor:
            str_type = colum['columnType']
            if line == 'pie' and str_type == 'string':
                pass  # 饼图只支持sum指标，
            else:
                func_check = sin.mapping.get(str_type) if sin.mapping.get(str_type) else sin.mapping.get('other')
                indicators.append(func_check(colum))
            if is_random():  # 暂时不加指标的过滤条件
                pass
        else:
            if not indicators:
                print(f'无合适指标{line}')
        print('指标', indicators)
        return indicators

    def get_demisions(self, days=3, dimension_num=1):
        """
        生成维度传参,并根据维度产生过滤规则
        :param dimension_num :统计的维度的个数
        :param days :天数
        :return :
        """
        # [{name: "is_add_ghs", columnType: "string", type: "or", filter: [{operator: "in", value: ["Y"]}]}]
        def select_5000_limit(d_num, limit=5000, days=days):
            """挑选排列组合小于5000的组合数"""
            param = []
            l = days
            for demision, enums in self.dimensions_enum.items():
                if not enums:
                    continue
                if l * len(enums) < limit and len(param) < d_num:
                    l = l * len(enums)
                    param.append(demision)
                else:
                    continue
            return param
        dimen = []
        dimen_filter = []

        select_dimen = select_5000_limit(d_num=dimension_num)
        for demision in self.dimensions:
            if demision['columnName'] in select_dimen:
                dimen.append({
                    'comment': demision['columnComment'],
                    'name': demision['columnName'],
                    'sort': 'asc'
                })
                # 给当前维度增加过滤条件
                fcg = FilterConfig(demision)
                filt = fcg.gene_filters(filter_num=random.randint(0, 2), enums=self.dimensions_enum[demision['columnName']])
                if filt:
                    dimen_filter.append({
                        'name': demision['columnName'],
                        'columnType': demision['columnType'],
                        'type': random.choice(('OR', 'AND')),
                        'filter': filt
                    })
        print('维度', dimen, dimen_filter)

        # 排序数据，插件校验需要
        return sorted(dimen, key=lambda x: x['name'], reverse=False), dimen_filter

    def get_date(self, dtype=None, dat=None, granu='day'):
        """
        生成报告的查询时间
        :param dtype {'between', 'since', 'last'}
        :param dat
        :param granu 日期类型
        :return datetime选择, 默认 最近 N 天
        """
        dtypes = ('between', 'since', 'last')
        param = {
            'granularity': granu,
            # 'date': dat if dtype else random.randint(1, 30),
            'date': 3,
            'type': dtype if dtype else dtypes[2]
        }
        return param

    def get_col_type(self, sear, indis):
        """查询指标字段的对应comment和type属性
        :param sear 指标字段名
        :param indis 指标数据
        :return
        """
        # print(sear, indis)
        for i in indis['indicator']:
            if i['name'] == sear.split('^&^')[0]:
                return i

    def sql_to_api_data(self, df, body):
        """将数据转化成api格式json,  nan
        :param df :Dataframe
        :param body: body 查询参数
        :return :
        """
        jsdata = {}
        key = body['dimension'][0]['name'] if body['chart'] == 'pie' else 'stat_date'
        if body['chart'] == 'pie':
            for dates in df[key].unique():
                jsdata[dates] = []
                r_df = df[df[key] == dates]
                for row in r_df.iterrows():
                    row_d = {}
                    for col in row[1].keys():
                        if '^&^' in col:
                            conf = self.get_col_type(col, indis=body)
                            row_d[col] = {
                                'comment': conf['comment'],
                                'value': None if pd.isnull(row[1][col]) else row[1][col]
                            }
                    jsdata[dates].append(row_d)
        else:
            for dates in df[key].unique():
                # '2020-12-01' -> '20201201'
                # d_date = get_any_type_time(dates, oldfmt='%Y%m%d', newfmt='%Y-%m-%d')
                jsdata[dates] = []
                r_df = df[df[key] == dates]
                for row in r_df.iterrows():
                    row_d = {}
                    for col in row[1].keys():
                        if '^&^' in col:
                            conf = self.get_col_type(col, indis=body)

                            row_d[col] = {
                                'columnType': conf['columnType'],
                                'comment': conf['comment'],
                                'value': None if pd.isnull(row[1][col]) else row[1][col]
                            }
                        elif col != 'stat_date':
                            row_d[col] = None if pd.isnull(row[1][col]) else row[1][col]
                    jsdata[dates].append(row_d)

        return jsdata

    def json_patch(self, first, second, optimization=True, dumps=None, line='line'):
        """json对比，排除value数据为字符串影响"""
        for patch in jsonpatch.JsonPatch.from_diff(first, second, optimization=optimization, dumps=dumps,):
            # print(patch)
            if patch['op'] == 'replace':
                try:
                    patch['value'] = float(patch['value'])
                    jsonpatch.apply_patch(second, [patch], in_place=True)
                    jsonpatch.apply_patch(first, [patch], in_place=True)
                except Exception as e:
                    print(e)
        pat = jsonpatch.JsonPatch.from_diff(first, second)
        print(f'{line}报表：', pat)
        assert (not pat)

    def completion_data(self, rawdata, **kwargs):
        """补全数据"""
        columns = [i for i in kwargs.keys()]
        # indic = kwargs.get('indicator', [])
        print('sql查询数据', rawdata[:5])
        pro = [i for i in itertools.product(*[kwargs[col] for col in columns])]
        df = pd.DataFrame(pro, columns=columns)
        sql_df = pd.DataFrame(data=rawdata[1:], columns=rawdata[0])  # sql查询的原始数据

        merged = pd.merge(df, sql_df, how='outer', on=columns)
        for indix in merged.columns:
            if '^&^' in indix:
                merged[indix] = [_ if _ else '' for _ in merged[indix]]
                # pd.to_numeric(merged[indix])
        print("数据补全", merged.head())
        return merged.sort_values(by=columns, axis=0, ascending=[True] * len(columns))

    def get_db_tbs(self):
        """
        获取所有可以生成报表的库_表信息
        """
        data = self.report.api_report_fetch_all_source().get('data')
        for db in data:
            for tb in data[db]:
                yield (db, tb)

    def deal_sql_data(self, body, sql, date_range):
        # 数据查询sql生成并补全数据,不同类型报表数据格式不同
        print("查询SQL：", sql)
        res = BackOffQuery(sql=sql, token=self.user.get_token).api_get_data()
        if body['chart'] == 'pie':
            dimensions_enum = {}
        else:
            dimensions_enum = {'stat_date': date_range, }
        for dd in body['dimension']:
            dimensions_enum[dd['name']] = self.dimensions_enum[dd['name']]
        sql_df = self.completion_data(rawdata=res, **dimensions_enum)

        sql_data = self.sql_to_api_data(df=sql_df, body=body, )
        print('-' * 10, sql_data)
        return sql_data

    @pytest.mark.parametrize('line', ['line'])
    def test_report_check(self, line):
        """
        线性图：维度 {0, } 指标 {1, } ['pie', 'line', 'scatter']
        散点图：维度 {1, } 指标 1
        饼图：维度 1 指标 1
        """
        date_conf = self.get_date()
        date_range = generate_date_range(date_conf)
        body = {
            "reportType": "preview",
            "tableSource": self.dbtbs[1],
            "databaseName": self.dbtbs[0],

            "chart": line,
            "dateConfig": date_conf,
            "setting": []
        }
        mapping = {
            'pie': (1, 1),  # 饼图  单维度单指标
            'line': (random.randint(0, len(self.dimensions)), random.randint(1, len(self.indicators))), # 线性  多指标，
            'scatter': (random.randint(1, len(self.dimensions)), 1), # 饼图  单指标  多维度
        }
        indicator_conf = self.get_indicators(indicator_num=mapping.get(line)[1], line=line)
        dimension_conf, dimension_filter_conf = self.get_demisions(dimension_num=mapping.get(line)[0], days=len(date_range))
        body = {
            "dimension": dimension_conf,
            "indicator": indicator_conf,
            "dimensionFilter": dimension_filter_conf,
            "indicatorFilter": [],
            **body
        }

        # body = {'dimension': [{'comment': '年龄', 'name': 'age', 'sort': 'asc'}], 'indicator': [{'type': 'sum', 'columnType': 'bigint', 'comment': '单课当日完课用户数（分子）', 'name': 'molecule_single_lesson_complete_1d'}],
        #         'dimensionFilter': [{'name': 'age', 'columnType': 'string', 'type': 'AND', 'filter': [{'operator': 'in', 'value':['其他', '[7,8)', '[8,+∞)', '[5,6)', '[4,5)', '[3,4)', '[2,3)', '[1,2)', '[0,1)', '[6,7)']}]}],
        #         'indicatorFilter': [], 'reportType': 'preview', 'tableSource': 'rpt_lesson_lesson_complete_total_all_d', 'databaseName': 'jlgl_rpt', 'chart': 'pie', 'dateConfig': {'granularity': 'day', 'date': 3, 'type': 'last'},
        #         'setting': []}

        print("入参：", body)
        api_data = self.report.api_manage_save_report(**body)['data']

        sql = ground_sql(**body)
        sql_data = self.deal_sql_data(body=body, sql=sql, date_range=date_range)
        print("sql：", sql_data, )
        # print('api数据', api_data)
        self.json_patch(sql_data, api_data, line=line)




if __name__ == '__main__':
    pytest.main(["-m", "add", "-s"])
