# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/3 1:57 下午
@Author  : Demon
@File    : back_off_get_result.py
"""

import backoff
from business.Elephant.ApiElephant.ApiQueryInfo import ApiQueryInfo



class BackOffQuery(object):
    def __init__(self, sql, token):
        self.asr = ApiQueryInfo(token=token)
        self.sql = sql

    @backoff.on_predicate(backoff.constant, interval=5)
    def back_off_query(self, taskid, *args, **kwargs):
        """
        :param taskid :查询ID
        :return
        """
        res = self.asr.api_adhoc_check_status(task_id=taskid, )

        for dat in res['data'][taskid]:
            # print(dat)
            assert dat['id'] == taskid
            if dat['status'] == '2':
                # 查询完成
                return True
            elif dat['status'] == '3':
                raise dat['exception']

    def api_get_data(self):
        try:
            taskid = self.asr.api_adhoc_query_list(sql=self.sql).get('data')[0]
            if self.back_off_query(taskid):
                return self.asr.api_adhoc_sql_result(task_id=taskid).get('data')[taskid]
        except Exception as e:
            print(e)


if __name__ == '__main__':
    sql = """
    select * 
    from jlgl_rpt.rpt_traffic_reading_new_user_add_d as d 
    where d.dt = '20201011'
    """
    # res = BackOffQuery(sql=sql).api_get_data()
    # print(res)
