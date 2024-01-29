# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/13 3:02 下午
@Author  : Demon
@File    : paid_user_9.py
"""

from config.env.domains import Domains
from utils.middleware.dbLib import MySQL
from business.zero.GetUserProperty import GetUserProperty
from business.zero.ApiLessonCentral.ApiLessonCentral import ApiLessonCentral
from utils.date_helper import get_any_time_stamp

class TestLessonData(object):
    """
    TestSublessonComplete 接口测试
    """
    dm = Domains()
    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['zero_url'])
        cls.zero = GetUserProperty()
        cls.lesson = ApiLessonCentral(token=cls.zero.get_token)

    def test_user_9_9_dev(self):
        # 9.9用户数据导入验证
        db, tb = 'eduplatform1', 'eduplatform0'
        mysql1 = MySQL(pre_db=db, db_name=db)
        mysql10 = MySQL(pre_db=tb, db_name=tb)
        with open('./old_99_user', 'r') as f:
            line = f.readline()
            while line:
                uid, uid_date = line.split(r',')[0], line.split(r',')[1]
                resp = self.lesson.api_lesson_get_name(uid=uid, table='eduplatform').get('data')
                if resp.split('.')[0] == db:
                    data = mysql1.query(f'select * from paid_99_user where uid="{uid}"')

                elif resp.split('.')[0] == tb:
                    data = mysql10.query(f'select * from paid_99_user where uid="{uid}"')
                try:
                    assert len(data) == 1
                    assert get_any_time_stamp(uid_date) == data[0]['open_lesson_time']
                except :
                    with open('./temp.txt', 'a') as op:
                        op.write(uid + '\n')
                line = f.readline()


    def test_lesson_upload(self):
        pass