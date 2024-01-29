# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/2 3:54 下午
@Author  : Demon
@File    : report_config.py
"""


"""
生成土拨鼠报告所需的配置
"""

import json
import random
import pandas as pd
from testcase.Elephant.report_sql import get_off_set_time
from business.Elephant.commons.common import Xenum
def is_random():
    """
    随机添加数据
    """
    return random.choice((True, False))

class SqlIndicators(object):
    ARITHMETICS = ('distinct_count', 'count', 'min', 'max', 'sum', 'avg', 'sequential_day')
    STRINGS = ('distinct_count', 'count')
    OTHERS = ('min', 'max', 'sum', 'avg', )  #  'sequential_day'n 暂不支持环比计算
    def __init__(self, line='line'):
        self.line = line
        self.mapping = {
            # 'sum': '求和',
            # 'avg': '平均值',
            # 'min': '最小',
            # 'sequential_day': '环比',
            # 'max': '最大',
            # 'count': '计数', # string 才有
            # 'distinct_count': '重复计数', # string 才有
            'string': self.string_check,
            'arithmetic': self.arithmetic_check,
            'other': self.other_check,
        }

    def _rules_filter(self, enums=[], limit=2):
        filters = set()
        while limit > 0:
            typ = random.choice([_ for _ in Xenum])
            if typ in [Xenum.IS_NULL, Xenum.IS_NOT_NULL]:
                filters.add(json.dumps({'operator': typ.value, 'value': None}))
            if typ in [Xenum.IS_NOT_IN, Xenum.IS_IN]:
                filters.add(json.dumps({'operator': typ.value, 'value': random.sample(enums, random.randint(1, len(enums)))}))
            else:
                # 单个字符串或者数值，限定固定数据固定数据，否则无意义
                filters.add(json.dumps({'operator': typ.value, 'value': "1"}))
            limit -= 1
        return [_ for _ in map(lambda x:json.loads(x), filters)]

    def string_check(self, column, enums=[]):
        """获取字符串类型数据的计算方式"""
        op = {
            'type': random.choice(self.STRINGS),
            'columnType': column['columnType'],
            'comment': column['columnComment'],
            'name': column['columnName']
        }
        return op

    def arithmetic_check(self, column, enums=[]):
        op = {
            'type': random.choice(self.ARITHMETICS),
            'columnType': column['columnType'],
            'comment': column['columnComment'],
            'name': column['columnName']
        }
        # opf = {}
        # if is_random():
        #     rule_ = self._rules_filter(enums)
        #     opf = {
        #         'name': column['columnName'],
        #         'columnType': column['columnType'],
        #         'type': random.choice(('OR', 'AND')),
        #         'filter': random.sample(rule_, random.randint(1, len(rule_)))
        #     }
        # return {'type': 'distinct_count', 'columnType': 'string', 'comment': 'ssdd', 'name': 'after_amount'}, {'name': 'after_amount', 'columnType': 'string', 'type': 'AND', 'filter': [{'operator': 'IN', 'value': [',,']}, {'operator': 'IS NULL', 'value': None}]}
        return op

    def other_check(self, column, enums=[]):

        op = {
            'type': 'sum' if self.line == 'pie' else random.choice(self.OTHERS),
            'columnType': column['columnType'],
            'comment': column['columnComment'],
            'name': column['columnName']
        }

        return op


class FilterConfig():
    def __init__(self, column):
        """sql中字段符号对应sql关键词配置"""
        # self.mapping = {
        #     Xenum.IS_IN.value: self.multistr_keywords,
        #     Xenum.IS_NOT_IN.value: self.multistr_keywords,
        #     Xenum.IS_NULL.value: self.isnone_keywords,
        #     Xenum.IS_NOT_NULL.value: self.isnone_keywords,
        #     'other': self.singlestr_keywords
        # }
        self.column = column

    def gene_relate(self, enums):
        """
        enums为空时不能生成 in or  not in
        """
        fenum = []
        for x in Xenum:
            if (not enums) and x in (Xenum.IS_IN, Xenum.IS_NOT_IN):
                continue
            fenum.append(x)
        # fenum = filter(lambda x: x in (Xenum.IS_IN, Xenum.IS_NOT_IN) and not enums, Xenum)
        # print([fenum])
        return random.choice(fenum).value

    def gene_filters(self, filter_num=0, enums=[]):
        gene_filters_list = []
        while filter_num > 0:
            operat = self.gene_relate(enums=enums)
            # opear = '='
            # func = self.mapping.get(opear) if self.mapping.get(opear) else self.mapping.get('other')
            filter_num -= 1
            gene_filters_list.append({"operator": operat, "value": self.get_keywords(operat=operat, enums=enums)})
        if enums and not gene_filters_list:
            gene_filters_list.append({"operator": Xenum.IS_IN.value, "value": enums})
        return gene_filters_list

    def get_keywords(self, operat, enums=[]):
        """
        :param column: {'columnType': 'double', 'columnDefine': 'indicator', 'columnComment': '\xe6', 'columnName': 'after_amount'
        """
        if operat in [Xenum.IS_NULL.value, Xenum.IS_NOT_NULL.value]:
            return None
        if operat in [Xenum.IS_NOT_IN.value, Xenum.IS_IN.value]:
            if not enums:
                raise Exception("请传入枚举值")
            return random.sample(enums, random.randint(1, len(enums)))
        else:
            # 单个字符串或者数值，限定固定数据固定数据，否则无意义
            return '1'


def generate_date_range(dateconfig):
    """
    根据参数dateconfig 对应的时间序列  {'granularity': 'day', 'date': 423, 'type': 'last'}
    :return  ['2020-10-11', '2020-10-12', '2020-10-13']
    """
    if dateconfig['type'] == 'last':
        start_date = get_off_set_time(days=-int(dateconfig['date']))
        end_date = get_off_set_time(days=-1)
    elif dateconfig['type'] == 'since':
        start_date = dateconfig['date']
        end_date = get_off_set_time(days=-1)
    else:
        start_date = dateconfig['date'][0]
        end_date = dateconfig['date'][1]
    date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq="1D"
    )
    return [_.strftime('%Y-%m-%d') for _ in date_range]


if __name__ == '__main__':
    s = {'columnType': 'double', 'columnDefine': 'indicator', 'columnComment': '\xe6', 'columnName': 'after_amount'}
    # print(FilterConfig(s).gene_filters(filter_num=2), )

    # generate_date_range('')

    data_yers = {
        "20201011": [
            ["tims", "_c1"],
            ["2019-10", "2139508"],
            ["2019-09", "5672732"],
            ["2019-11", "5858405"],
            ["2019-12", "5858905"],
        ]
    }
    data_toda = {
        "20201012": [
            ["tims", "_c1"],
            ["2019-10", "30"],
            ["2019-09", "20"],
            ["2019-11", "20"],
            ["2019-12", "30"],
        ]
    }
    a1 = {"aaa": [["count"], ["75271466"]]}
    a2 = {"bbb": [["count"], ["75272966"]]}
    """
    20201011 2019-10 2139528
    """

    import pandas as pd
    # data_yers.update(data_toda)
    # df = pd.DataFrame(data=data_yers, )
    df = pd.DataFrame(data_toda['20201012'][1:], columns=data_toda['20201012'][0])
    df['day'] = '20201012'

    sdf = pd.DataFrame(data_yers['20201011'][1:], columns=data_yers['20201011'][0])
    sdf['day'] = '20201011'
    print(df, sdf)
    df = df.sort_values(by='tims')
    df['_c1'] = df['_c1'].astype(float)
    print(df['_c1'], df['_c1'].diff())
    # df['huanbi'] = df['_c1']/(df['_c1'] - df['_c1'].diff()) - 1

    df = df.append(sdf)
    for tim in df.groupby(by='tims'):
        print(pd.DataFrame(tim[1]))
    sql = """
        SELECT 
            substring(d.stat_date, 1, 7) as tims , count(*) AS counts
        FROM jlgl_rpt.rpt_lesson_lesson_complete_total_all_d as d
        WHERE d.dt='{dt}' 
        GROUP BY substring(d.stat_date, 1, 7)
        """.format(dt=get_off_set_time(days=-1))
    print(sql)