# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/9 6:13 下午
@Author  : Demon
@File    : table_data_trend.py
"""

'''
 表数据 用例<周级>
 1.数据枚举值外的value值类型及记录数监控
 2.每周入库数据记录数
 3.不为空的字段是否缺失值
 4.关键指标
 5.数据同比环比
 6.数据掉 0监控
 7.数据重复监控；某些字段重复率，
 *8.数据查询性能
告警：
 周级报告，月级报告
 
'''

from utils.middleware.dbLib import MySQL
db = MySQL('default')
# 'jlgl_rpt.rpt_traffic_reading_new_user_add_d'

"""
create table rpt_traffic_reading_new_user_add_d (
    dt varchar(32) not null , 
    stat_date varchar(32) not null , 
    register_source varchar(64) not null , 
    user_id varchar(64) not null 
)partition by dt date_format(now(), '%Y%m%d')



insert into rpt_traffic_reading_new_user_add_d (dt,stat_date,register_source,user_id)
values(date_format(DATE_SUB(curdate(),INTERVAL 2 DAY), '%Y%m%d'), date_format(DATE_SUB(curdate(),INTERVAL 2 DAY), '%Y-%m-%d'),
'瓜瓜阅读', 'uer_id008')


# 日环比
select  stat_date, count(1) from rpt_traffic_reading_new_user_add_d
 where dt between '20201102'
 and '20201219'
 group by  stat_date;
"""


daily_all_count = """
SELECT COUNT(*)
FROM {db_name}.{tb_name} AS t
WHERE t.dt = '{yesterday}'
"""
