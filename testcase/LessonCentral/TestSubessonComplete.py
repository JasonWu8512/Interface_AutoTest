# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/22 5:07 下午
@Author  : Demon
@File    : TestSubessonComplete.py
"""

import pytest
import uuid
from utils.middleware.dbLib import MySQL
from config.env.domains import Domains, ROOT_PATH
from utils.middleware.dbLib import get_connect_config
from business.Crm.ApiAccount.userProperty import UserProperty
from business.zero.ApiLessonCentral import ApiLessonCentral
from business.zero.GetUserProperty import GetUserProperty
from utils.date_helper import get_time_stamp

class TestSublessonComplete(object):
    """
    TestSublessonComplete 接口测试
    """
    uid = f'test-{get_time_stamp()}'
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        # 测试环境的session
        cls.zero_api = ApiLessonCentral.ApiLessonCentral(token=GetUserProperty().get_token)
        # cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd']).session
        # cls.lesson = ApiLessonCentral(session=cls.session)
        cls.uid = f'test-{get_time_stamp()}'

    def __get_uid(self):
        return f'test-{get_time_stamp()}'

    # @pytest.mark.parametrize('table,col_name', [('rpt_traffic_reading_new_user_add_d', 'dt')])
    def get_no_record_uid(self, table, col_name):
        """获取某张表中不存在uid/bid"""
        _col = str(uuid.uuid4())
        try:
            data = MySQL(db_config='default').query(
                f'select count(1) as num from {table} where {col_name}=%s', args=((_col)))
            if data[0].get('num') == 0:
                return _col
            else:
                return self.get_no_record_uid(table, col_name)
        except Exception as e:
            print(e)

    @pytest.mark.repeat(2)
    def test_add_record(self, get_uid):
        # 无对应bid时，新增记录，有则 +1
        data = self.zero_api.api_lesson_get_name(uid=get_uid, table='sublesson_record').get('data')
        db, tb = data.split('.')[0], data.split('.')[1]
        print(get_uid, db, tb)
        mysql = MySQL(pre_db=db, db_name=db)
        con = mysql.query(f'select * from {tb} where bid =%s', args=(get_uid))
        old_count = con[0]['finish_count'] if con else 0
        # 计分一次
        self.zero_api.api_lesson_sublesson_complete(
            params=[{
                "gameId": "game_597",
                "score": 21,
                "finishTime": int(get_time_stamp()),
                "lessonId": "L1XX001",
                "sublessonId": "L1XX00101",
                "bid": get_uid
            }],
            env=self.config.get('env')
        )

        add_data = mysql.query(f'select * from {tb} where bid =%s', args=(get_uid))
        assert add_data[0]['finish_count'] == old_count + 1
        # 不删除脏数据

    @pytest.mark.parametrize('score,sub_les_id', [(50, 'K1GEP00101'),])
    def test_sublesson_complete_last_record(self, score, sub_les_id):
        """sublesson_record 是最后一条 记录""" #  (-1, 'K1GEP00101'), (79, 'K1GEP00101')
        uid = self.__get_uid()
        uid = '01e975c3bf2d4d0fab6bc27851be7009'
        data = self.zero_api.api_lesson_get_name(uid=uid, table='lesson_record').get('data')
        db, tb = data.split('.')[0], data.split('.')[1]
        print(uid, db, tb, score)
        # mysql = MySQL(db_config=get_connect_config(pre_db=db, db_name=db))
        mysql = MySQL(pre_db=db, db_name=db)
        con = mysql.query(f'select * from lesson_record0 where bid ="01e975c3bf2d4d0fab6bc27851be7009"')
        # con = mysql.query(f'select * from {tb} where bid =%s', args=(uid))
        old_count = con[0]['finish_count'] if con else 0
        print(con, '*' * 10, old_count)
        # 计分一次
        self.zero_api.api_lesson_sublesson_complete(
            params=[{
                "gameId": "L1U00W1D2Q7",
                "score": score,
                "finishTime": int(get_time_stamp()),
                "lessonId": "K1GEP001",
                "sublessonId": sub_les_id,
                "bid": "01e975c3bf2d4d0fab6bc27851be7009"
            }],
            env=self.config.get('env')
        )
        con = mysql.query(f'select * from {tb} where bid =%s', args=(uid))
        # old_count = con[0]['finish_count'] if con else 0
        print(con)



