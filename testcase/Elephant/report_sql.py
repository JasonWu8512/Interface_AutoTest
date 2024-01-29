# -*- coding: utf-8 -*-
"""
@Time    : 2020/11/15 1:13 上午
@Author  : Demon
@File    : report_sql.py
"""
from business.Elephant.commons.common import Xenum
import datetime
from utils.date_helper import get_off_set_time


parfams = {
    "tableSource": "rpt_revenue_reading_forward_order_thin_aggr_add_d",
    "databaseName": "jlgl_rpt",
    "dimension": [{
        "comment": "\u4e1a\u52a1\u6765\u6e90",
        "name": "biz_source",
        "sort": "asc"
        },],
    "indicator": [
        {
            "columnType": "double",
            "comment": "\u6210\u4ea4\u91d1\u989d",
            "name": "after_amount",
            "type": "avg"
        },
    ],
    "dimensionFilter": [{'name': "levelwewe", 'columnType': "string", 'type': "or", 'filter': [
        {'operator': "=", 'value': "22"}, {'operator': "in", 'value': ["2332"]}
    ]},
                        {'name': "level3455", 'columnType': "string", 'type': "or", 'filter': [
                            {'operator': "=", 'value': "22"}
                        ]}],
    "indicatorFilter": [{'name': "level", 'columnType': "string", 'type': "or", 'filter': [
        {'operator': "=", 'value': "22"}, {'operator': "!=", 'value': "2332"}
    ]},
                        # {'name': "level3333", 'columnType': "string", 'type': "or", 'filter': [
                        #     {'operator': "=", 'value': "22"}
                        # ]}
                        ],
    "dateConfig": {
        "granularity": "day",
        "date": 298,
        "type": "last"
        },
    }


def get_between_days(dconf):
    """
    :param dconf :时间配置, 不计算当天时间
    :return : '20201102', '20201108',
    """
    fmt = 'YYYY-MM-DD'
    yester_day = get_off_set_time(days=-1, fmt=fmt)
    if not dconf:
        return [get_off_set_time(days=-3, fmt=fmt), yester_day]
    if dconf.get('type') == 'last':
        return [get_off_set_time(days=-int(dconf['date']), fmt=fmt), yester_day]
    elif dconf.get('type') == 'since':
        return [str(dconf.get('date')), yester_day]
    else:
        return dconf.get('date')

def ground_sql_bak(**kwargs):
    """
    :param body
    :return
    """
    databaseName = kwargs.get('databaseName')
    tableSource = kwargs.get('tableSource')
    dates = get_between_days(kwargs.get('dateConfig'))
    dimension = kwargs.get('dimension')
    indicator = kwargs.get('indicator')
    dimensionFilter = kwargs.get('dimensionFilter')
    indicatorFilter = kwargs.get('indicatorFilter')

    # 拼接sql 时间
    date_filter = f't.`stat_date` BETWEEN {dates[0]} AND {dates[1]}'

    dt_filter = 't.dt = \'{0}\''.format(get_off_set_time(days=-1, fmt='YYYYMMDD'))  # 分区查询
    from_sql = f' FROM {databaseName}.{tableSource} AS t'

    # 拼接sql 维度
    der = ', '.join(['t.`%s` %s' % (dem['name'], dem['sort'].upper()) for dem in dimension])
    rou = ', '.join(['t.`' + dem['name'] + '`' for dem in dimension])
    # orders = 'ORDER BY t.`stat_date` ASC, ' + der if dimension else 'ORDER BY t.`stat_date` ASC'
    groups = 'GROUP BY t.`stat_date`, ' + rou if dimension else 'GROUP BY t.`stat_date`'

    # 拼接sql 指标
    indis = []
    for indicator in indicator:
        if indicator['columnType'] == 'define':
            # 自定义算式，非UDF
            pass
        indis.append(calculate_indicators(indicator))
    indicats = ', '.join(indis)
    dimensis = ', '.join([_['name'] for _ in dimension])
    # 拼接sql 维度过滤规则
    dimension_filter = '(' + ' AND '.join([ground(d) for d in dimensionFilter]) + ')' if len(dimensionFilter) > 1 else ' AND '.join([ground(d) for d in dimensionFilter])
    # 拼接sql 指标规则过滤
    indicator_filter = '(' + ' AND '.join([ground(d) for d in indicatorFilter]) + ')' if len(indicatorFilter) > 1 else ' AND '.join([ground(d) for d in indicatorFilter])
    dt_dime_indi = " AND ".join(filter(lambda x: x, [dimension_filter, indicator_filter, date_filter]))
    sql = f'SELECT t.`stat_date`,' + f'{dimensis + "," if dimensis else " "}' + f'{indicats} {from_sql} WHERE {dt_filter} AND {dt_dime_indi} {groups} '

    return sql

def calculate_indicators(column):
    """
    指标计算 别名  count(distinct t.chech) as `ksja`         # lesson_score^&^avg
    """
    indicator_alias = '`' + column['name'] + '^&^' + column['type'] + '`'
    if column['type'].upper() in ('DISTINCT_COUNT'):
        calculate_typ = ' COUNT(DISTINCT '
    else:
        calculate_typ = column['type'].upper() + '('
    return f'{calculate_typ} t.{column["name"]} ) AS {indicator_alias}'

def ground(filtcol):
    """
    {'name': "level", 'columnType': "string", 'type': "or", 'filter': [{operator: "=", value: "22"}]}
    """
    if not filtcol:
        return ""
    fs = []
    for f in filtcol['filter']:
        if f['operator'].lower() in (Xenum.IS_IN.value, Xenum.IS_NOT_IN.value):

            val = '(' + ', '.join(['\'' + str(_) + '\'' for _ in f['value']]) + ')'
            fsrule = ' `%s` %s %s ' % (filtcol['name'], f['operator'].upper(), val)

        elif f['operator'].lower() in (Xenum.LIKE.value, Xenum.NOT_LIKE.value):
            val = '\'%' + f['value'] + '%\''
            fsrule = ' `%s` %s %s ' % (filtcol['name'], f['operator'].upper(), val)
        elif f['operator'].lower() in (Xenum.IS_NOT_NULL.value, Xenum.IS_NULL.value):
            fsrule = ' `%s` %s ' % (filtcol['name'], f['operator'].upper())
        else:
            fsrule = ' `%s` %s \'%s\' ' % (filtcol['name'], f['operator'].upper(), f['value'])
        fs.append(fsrule)
    return '(' + filtcol['type'].join(fs) + ')' if fs else filtcol['type'].join(fs)


def ground_sql(**kwargs,):
    """
    :param line
    :return
    """
    databaseName = kwargs.get('databaseName')
    tableSource = kwargs.get('tableSource')
    dates = get_between_days(kwargs.get('dateConfig'))
    dimension = kwargs.get('dimension')
    indicator = kwargs.get('indicator')
    dimensionFilter = kwargs.get('dimensionFilter')
    indicatorFilter = kwargs.get('indicatorFilter')
    line = kwargs['chart']

    # 拼接sql 时间
    date_filter = f't.`stat_date` BETWEEN \'{dates[0]}\' AND \'{dates[1]}\''

    dt_filter = 't.dt = \'{0}\''.format(get_off_set_time(days=-1, fmt='YYYYMMDD'))  # 分区查询
    from_sql = f' FROM {databaseName}.{tableSource} AS t'

    # 拼接sql 维度
    # der = ', '.join(['t.`%s` %s' % (dem['name'], dem['sort'].upper()) for dem in dimension])
    rou = ', '.join(['t.`' + dem['name'] + '`' for dem in dimension])
    # orders = 'ORDER BY t.`stat_date` ASC, ' + der if dimension else 'ORDER BY t.`stat_date` ASC'
    if line == 'pie':
        groups = 'GROUP BY ' + rou if dimension else ''
    else:
        groups = 'GROUP BY t.`stat_date`, ' + rou if dimension else 'GROUP BY t.`stat_date`'

    # 拼接sql 指标
    indis = []
    for indicator in indicator:
        if indicator['columnType'] == 'define':
            # 自定义算式，非UDF
            pass
        indis.append(calculate_indicators(indicator))
    indicats = ', '.join(indis)
    dimensis = ', '.join([_['name'] for _ in dimension])
    # 拼接sql 维度过滤规则
    dimension_filter = '(' + ' AND '.join([ground(d) for d in dimensionFilter]) + ')' if len(dimensionFilter) > 1 else ' AND '.join([ground(d) for d in dimensionFilter])
    # 拼接sql 指标规则过滤
    indicator_filter = '(' + ' AND '.join([ground(d) for d in indicatorFilter]) + ')' if len(indicatorFilter) > 1 else ' AND '.join([ground(d) for d in indicatorFilter])
    dt_dime_indi = " AND ".join(filter(lambda x: x, [dimension_filter, indicator_filter, date_filter]))
    if line == 'pie':
        sql = f'SELECT ' + f'{dimensis + "," if dimensis else " "}' + f'{indicats} {from_sql} WHERE {dt_filter} AND {dt_dime_indi} {groups} '
    else:
        sql = f'SELECT t.`stat_date`,' + f'{dimensis + "," if dimensis else " "}' + f'{indicats} {from_sql} WHERE {dt_filter} AND {dt_dime_indi} {groups} '

    return sql

def pie_sql():
    """WITH post AS(
        SELECT
            '20201206' AS dt, l.is_add_ghs, l.lesson_score
        FROM jlgl_rpt.rpt_lesson_lesson_complete_total_all_d AS l
        WHERE l.dt = '20201206'
        AND l.stat_date = '2020-12-04'
        AND l.is_add_ghs IN ('Y', 'N')
        )
        SELECT
          t1.is_add_ghs, t1.molecular / t2.denominator AS ratio
        FROM (
          SELECT dt, is_add_ghs, SUM(lesson_score) AS molecular FROM post GROUP BY dt, is_add_ghs
        ) AS t1,
        (
          SELECT dt, SUM(lesson_score) AS denominator FROM post GROUP BY dt
        ) AS t2
        WHERE t1.dt = t2.dt
    """

if __name__ == '__main__':
    print(get_off_set_time(days=-8, fmt='YYYYMMDD'), get_off_set_time(days=-1, fmt='YYYYMMDD'))
    ds = [{'name': "jiaoke", 'type': '0', 'comment': '55'}, {'name': "name", 'type': '2', 'comment': '55'}]

    body = {"reportType": "preview", "id": None, "type": "eventSegmentation",
            "tableSource": "rpt_lesson_lesson_complete_total_all_d", "databaseName": "jlgl_rpt",
            "dimension": [{"name": "is_add_ghs", "sort": "asc", "comment": "是否添加规划师"}],
            "indicator": [{"name": "lesson_score", "type": "distinct_count", "comment": "课后得分", "columnType": "double"}],
            "dimensionFilter": [], "indicatorFilter": [], "chart": "line",
            "dateConfig": {"date": 3, "granularity": "day", "type": "last"}, "setting": []}

    # body = {'reportType': 'preview', 'id': None, 'type': 'eventSegmentation', 'tableSource': 'rpt_lesson_lesson_complete_total_all_d', 'databaseName': 'jlgl_rpt', 'dimension': [{'name': 'city_level', 'sort': 'asc', 'comment': '城市等级'}], 'indicator': [{'name': 'lesson_score', 'type': 'sum', 'comment': '课后得分', 'columnType': 'double'}], 'dimensionFilter': [], 'indicatorFilter': [], 'chart': 'pie', 'dateConfig': {'date': 3, 'granularity': 'day', 'type': 'last'}, 'setting': []}
    # body = {"reportType":"preview","id":None,"type":"eventSegmentation","tableSource":"rpt_lesson_lesson_complete_total_all_d","databaseName":"jlgl_rpt","dimension":[{"name":"city_level","sort":"asc","comment":"城市等级"}],"indicator":[{"name":"lesson_score","type":"sum","comment":"课后得分","columnType":"double"}],"dimensionFilter":[],"indicatorFilter":[],"chart":"scatter","dateConfig":{"date":3,"granularity":"day","type":"last"},"setting":[]}
    print(ground_sql(line='line', **body))

    # print(get_any_type_time('2021-10-20 16:36:08', oldfmt='%Y-%m-%d %H:%M:%S', newfmt='%Y-%m-%d'))