# -*- coding: utf-8 -*-
"""
@Time    : 2020/11/13 2:44 下午
@Author  : Demon
@File    : DataCheck.py
"""

"""提供json ，DataFrame数据对比"""

import re
import pandas as pd
import datetime
import sys
import jsonpatch
from utils.middleware.mongoLib import Domains
from business.Elephant.commons.common import logger
from pandas.testing import assert_frame_equal


class BigDataCheck(object):
    def __init__(self, ldf=None, rdf=None, db=False):
        """处理数据格式，转为DataFrame"""
        self.ldf = ldf
        self.rdf = rdf
        self.inner_cols = set(self.ldf.columns).intersection(set(self.rdf.columns))

    def __null_num(self, col, df):
        """查询Series 总行数，NAN 的行数"""
        return df[col].count(), df[col].isna().sum()

    def check_series_num(self, lse, rse):
        """按相同列分别排序，对比结果
        :param col:列名
        :param ldf:左
        :param rdf:右
        """
        try:

            print(lse.describe(), rse.describe())
            assert lse.describe().equals(other=rse.describe())
            assert (lse.count(), lse.isna().sum()) == (rse.count(), rse.isna().sum())
            logger.debug("Series is same")
        except:
            raise Exception(f"[{lse.name}<>{rse.name}]，DataDiff")

    def check_volume(self, ldf=None, rdf=None,
                     check_series=False,
                     check_dtype=True,
                     check_index_type="equiv",
                     check_column_type="equiv",
                     check_frame_type=True,
                     check_names=True,
                     ):
        """对比相同列的数学统计值"""
        for col in self.inner_cols:
            try:
                ldf = self.ldf.fillna("").astype(str).sort_values(by=col, ascending=True).reset_index(drop=True)
                rdf = self.rdf.fillna("").astype(str).sort_values(by=col, ascending=True).reset_index(drop=True)
                if check_series:
                    self.check_series_num(self.ldf[col], self.rdf[col])
                # print(ldf.fillna("").astype(str).sort_values(by=col, ascending=True))
                assert_frame_equal(left=ldf,
                                   right=rdf,
                                   check_dtype=check_dtype, check_index_type=check_index_type,
                                   check_column_type=check_column_type,
                                   check_frame_type=check_frame_type, check_names=check_names)
                logger.debug(f"DataFrame order by [{col}] is same")
                # DataFrame.iloc[:, 0] (column name="name") values are different (50.0 %)
            except AssertionError as e:
                exc_type, exc_value, exc_traceback_obj = sys.exc_info()
                m = re.search(r"\(column name=\"(.*)\"\) .* \((\d{1,}\.\d{1,} %)\)", str(exc_value))
                if m:
                    # print('8',m.span(), m.group(0), )
                    print(f'列【{m.group(1)}】, {m.group(2)}')
                print(exc_value)


def assert_bigdata(
    ldf,
    rdf,
    unique='id',
    check_dtype=False,
    check_index_type="equiv",
    check_column_type="equiv",
    check_series=False,
    check_frame_type=True,
    check_names=True,
):
    """
    Check that left and right DATA are equal. Ignore value str and float
    :param :unique 确定唯一排序的key， 可以是str，或者list
    """
    inner_cols = set(ldf.columns).intersection(set(rdf.columns))
    def try_float(df):
        try:
            return float(df)
        except:
            return df
    rdf = rdf.applymap(try_float)
    ldf = ldf.applymap(try_float)

    rdf = rdf.set_index(unique).sort_index()
    ldf = ldf.set_index(unique).sort_index()
    # print(ldf, rdf)
    try:
        # ldf = ldf.fillna("").astype(str).sort_values(by=col, ascending=True).reset_index(drop=True)
        # rdf = rdf.fillna("").astype(str).sort_values(by=col, ascending=True).reset_index(drop=True)
        rdf['value'].astype(float)
        assert_frame_equal(left=ldf,
                           right=rdf,
                           check_dtype=check_dtype, check_index_type=check_index_type,
                           check_column_type=check_column_type,
                           check_frame_type=check_frame_type, check_names=check_names)
        logger.debug(f"DataFrame is same")

    except AssertionError as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        m = re.search(r"\(column name=\"(.*)\"\) .* \((\d{1,}\.\d{1,} %)\)", str(exc_value))
        if m:
            print(f'列【{m.group(1)}】, {m.group(2)}')
        print(exc_value)


def json_patch_check(first, second, optimization=True, dumps=None, ):
    """json对比，排除value数据为字符串影响"""
    patchs = jsonpatch.JsonPatch.from_diff(first, second, optimization=optimization, dumps=dumps,)
    patsh = filter(lambda x: x['op'] == 'replace', patchs)
    for patch in patsh:
        # try:
        patch['value'] = float(patch['value'])
        # jsonpatch.apply_patch(second, [patch], in_place=True)
        print(patch)
        jsonpatch.apply_patch(first, [patch], in_place=True)
        print('***', first, second)
        # except Exception as e:
        #     print(e)
    # if patch['op'] != 'replace':
    #     raise Exception(patch)
    # else:
    #     try:
    #         patch['value'] = float(patch['value'])
    #         print(first, second)
    #         # jsonpatch.apply_patch(second, [patch], in_place=True)
    #
    #         jsonpatch.apply_patch(first, [patch], in_place=True)
    #         print(first, second)
    #     except Exception as e:
    #         print(e)
    return jsonpatch.JsonPatch.from_diff(second, first)


def select_5000_limit(d_num, limit=50, days=3):
    """挑选排列组合小于5000的组合数"""
    param = []
    l = days
    for demision, enums in {'2':3,'4':7,'5':3}.items():
        if not enums:
            continue
        if l * enums < limit and len(param) < d_num:
            l = l * enums
            param.append(demision)
        else:
            continue

    print(param)

print(select_5000_limit(d_num=0, ))
if __name__ == '__main__':
    dm = Domains()
    a = dm.set_env_path('dev')
    dm.set_domain(a['url'])
    d1 = ['demi1', 'demi100']
    d2 = ['demi2', 'demi200']
    s = ['zhibao1', 'zhibi2']

    # df1 = pd.DataFrame(np.arange(12).reshape(3, 4))
    # df2 = pd.DataFrame(np.arange(12).reshape(3, 4))
    tim = datetime.datetime.now()
    df1 = [{'id': '1b77becd65154133a564ab37649e4302', 'value': 100},
           {'id': '905ead47329f4680a6814f01eebe6313', 'value': 2},
           {'id': '9b83ef94c9c84619b9a8864f61ef2363', 'value': 2},
           {'id': '9dccbd8d44a64704ac09a8e66df073bc', 'value': 2},
           {'id': '45d58ace94864156abcd72e7de0a2309', 'value': 2}]

    df2 = [{'id': '1b77becd65154133a564ab37649e4302', 'value': 100.0},
           {'id': '45d58ace94864156abcd72e7de0a2309', 'value': 2},
           {'id': '905ead47329f4680a6814f01eebe6313', 'value': 2},
           {'id': '9b83ef94c9c84619b9a8864f61ef2363', 'value': 2},
           {'id': '9dccbd8d44a64704ac09a8e66df073bc', 'value': 2}]
    # assert_bigdata(pd.DataFrame(df1), pd.DataFrame(df2))
    # data = [["stat_date","register_source","user_id^&^count"],["2020-11-29","叽里呱啦","2387"],["2020-11-29","呱呱阅读","2833"],["2020-11-30","叽里呱啦","2108"],["2020-11-30","呱呱阅读","2673"],["2020-12-01","叽里呱啦","2086"],["2020-12-01","呱呱阅读","2280"],["2020-12-02","叽里呱啦","2177"],["2020-12-02","呱呱阅读","2420"]]
    # sd = {'2020-11-30': [{'user_id^&^count': {'columnType': 'string', 'comment': '新增注册用户数', 'value': '4781'}}], '2020-12-01': [{'user_id^&^count': {'columnType': 'string', 'comment': '新增注册用户数', 'value': '4366'}}], '2020-12-02': [{'user_id^&^count': {'columnType': 'string', 'comment': '新增注册用户数', 'value': '4597'}}]}
    # df = pd.DataFrame(data=data[1:], columns=data[0])
    # print(df.index)
    df = pd.DataFrame(df2)
    dfww = pd.DataFrame(df1)
    # dfww['value'] = [float(_) for _ in dfww['value']]


