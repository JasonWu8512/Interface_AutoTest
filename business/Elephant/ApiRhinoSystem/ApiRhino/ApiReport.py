# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/6 1:57 下午
@Author  : Demon
@File    : ApiReport.py
"""

# 数据源表管理

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
from business.Elephant.commons.common import HEADERS as header
from urllib import parse

class ApiReport(object):
    def __init__(self, token):
        self.host = Domains.domain
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.root = '/api_bi/report'

    def api_report_fetch_all_source(self):
        """
        获取缓存相关参数, 数据库.表 信息
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchAllSource")
        return send_api_request(url=api_url, headers=self.headers, method="post",)

    def api_report_fetch_by_id(self, ids: int):
        """
        根据报告id查询参数
        :param : ids
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchById")
        body = {"id": ids}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_permission_check(self, ids: int):
        """
        报表权限校验
        :param : ids
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/permissionCheck")
        body = {"id": ids}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_revert(self, ids: int):
        """
        报表重置
        :param : ids
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/reportRevert")
        body = {"id": ids}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_generate_file(self, ids: int):
        """
        报表生成文件
        :param : ids
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/generateFile")
        body = {"id": ids}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_download_file(self, ids: int):
        """
        下载报表数据csv
        :param : ids
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/downloadFile")
        body = {"id": ids}
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_select_dept_user(self, ids):
        """
        修改报告的负责人的时候，获取最高权限人信息,来自api_select_user 下的管理员 id
        :param ids : de86e07c647346468aed3c14038a5530
        :return
        """
        api_url = parse.urljoin(self.host, "/api_basic/dept/selectDeptUser")
        body = {
            "id": ids,
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_fetch_source_detail(self, dbname, tbname):
        """
        新建报告前获取某个表下的相关参数
        :param dbname: 数据库
        :param tbnam: 表名
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchSourceDetail")
        body = {
            "databaseName": dbname,
            "tableName": tbname
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_fetch_column_enum(self, dbname, tbname, col, dat=7, dtyp='last', gr="day", dt=None):
        """
        枚举表中字段对应的枚举值
        :param dbname: 数据库
        :param tbname: 表名
        :param dt:
        :param col: 表中的字段
        :param dat: 日期天数或者日期字符串 {3 , '20201109', ['20201109', '20201109']}
        :param dtyp: 时间类型 {last, since, between}
        :param gr: 时间单位 天
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchColumnEnum")
        body = {
            "databaseName": dbname,
            "tableName": tbname,
            "dt": dt,
            "dateConfig": {
                "date": dat,
                "granularity": gr,
                "type": dtyp
            },
            "columnName": col
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_fetch_sql(self, report_id):
        """
        获取报表SQL
        :param report_id: ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/fetchSql")
        body = {
            "report_id": report_id,
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_refresh_table_enum(self, report_id):
        """
        刷新报表库表对应的维度数据
        :param report_id: ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/refreshTableEnum")
        body = {
            "report_id": report_id,
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_report_refresh_report(self, report_id):
        """
        刷新报表数据，重新计算
        :param report_id: ID
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/refreshReport")
        body = {
            "report_id": report_id,
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

    def api_manage_save_report(self, databaseName, tableSource, setting=[], indicatorFilter=[],
                               dimension=[], indicator=[], ids=None, dimensionFilter=[], chart='line',
                               dateConfig={'date': 7, 'granularity': "day", 'type': "last"},
                               typ="eventSegmentation", reportType="preview", **kwargs):
        """
        新建报告
        :param reportType: 预览or保存 {save,preview} 默认预览
        :param ids: 报告id, 存在则编辑， 默认新建
        :param typ: 类型 {eventSegmentation}
        :param chart: 报表类型 {line,scatter,}
        :param databaseName: 数据库
        :param tableSource: 表名
        :param dimension: 维度列表 []
        :param dimensionFilter: 维度过滤列表 []
        :param indicator: 指标列表 []
        :param indicatorFilter: 指标过滤列表 []
        :param setting: 配置信息 []
        :param dateConfig:
        :return
        """
        api_url = parse.urljoin(self.host, f"{self.root}/save")
        body = {
            "reportType": kwargs.get('reportType') if kwargs.get('reportType') else reportType,
            "id": kwargs.get('ids') if kwargs.get('ids') is not None else ids,
            "type": kwargs.get('typ') if kwargs.get('typ') else typ,
            "tableSource": kwargs.get('tableSource') if kwargs.get('tableSource') else tableSource,
            "databaseName": kwargs.get('databaseName') if kwargs.get('databaseName') else databaseName,
            "dimension": kwargs.get('dimension') if kwargs.get('dimension') else dimension,
            "indicator": kwargs.get('indicator') if kwargs.get('indicator') else indicator,
            "dimensionFilter": kwargs.get('dimensionFilter') if kwargs.get('dimensionFilter') else dimensionFilter,
            "indicatorFilter": kwargs.get('indicatorFilter') if kwargs.get('indicatorFilter') else indicatorFilter,
            "chart": kwargs.get('chart') if kwargs.get('chart') else chart,
            "dateConfig": kwargs.get('dateConfig') if kwargs.get('dateConfig') else dateConfig,
            "setting": kwargs.get('setting') if kwargs.get('setting') else setting,
        }
        return send_api_request(url=api_url, headers=self.headers, method="post", paramType="json", paramData=body)

