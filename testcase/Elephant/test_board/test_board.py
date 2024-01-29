# -*- coding: utf-8 -*-
"""
@Time    : 2021/8/4 15:17 下午
@Author  : cora
@File    : test_board.py
接口：看板的增删改查
 /api_board/board/add
 /api_board/board/save
 /api_board/board/fetchList
 /api_board/board/fetchById
 /api_board/board/delete
"""

import pytest
from config.env.domains import Domains
from business.Elephant.ApiBasic.GetUserProper import GetUserProper
from business.Elephant.ApiBoard.ApiBoard import ApiBoard
import random
import time
import pytest_check

@pytest.mark.Elephant
class TestBoard(object):
    """

    """
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        # 测试环境的session
        cls.user = GetUserProper(user=cls.config['elephant']['user'], pwd=cls.config['elephant']['pwd'])
        cls.report = ApiBoard(token=cls.user.token)

    @pytest.mark.parametrize("name,pub", [('l6', False), ('p6', True)])
    # 对新增和删除接口进行校验
    def test_board_add_delete(self, name, pub):
        res = self.report.api_board_add(name=name, is_public=pub)
        assert res.get('status') == 1
        if res.get('status') == 1:
            self.report.api_board_delete(ids=res.get('data').get('id'))

    # 对看板列表、看板详情以及看板更新进行校验
    # updateTime: "2021-08-04 17:00:27.0"
    @pytest.mark.parametrize("update_time", [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])
    def test_board_fetch_save(self, update_time):
        # 校验拉取看板列表的接口
        res = self.report.api_board_list()
        assert res.get('status') == 1
        # 随机选择一个看板id，进行获取看板详情页的接口的校验
        if res.get('status') == 1:
            # ids = random.choice(res.get('data')).get('id')
            res1 = self.report.api_board_fetch_id(ids=random.choice(res.get('data')).get('id'))
            assert res1.get('status') == 1
            if res1.get('status') == 1:
                res2 = res1.get('data')
                res3 = self.report.api_board_save(name=res2.get('name')+'666', update_time=update_time, ids=res2.get('id'),
                                                  chart_config=res2.get('chartConfig'), is_public=res2.get('isPublic'),
                                                  has_permission=res2.get('hasPermission'), global_filter=res2.get('globalFilter'),
                                                  owner=res2.get('owner'), desc=list(res2.get('desc')), index_rpt=res2.get('indexRpt'),
                                                  rpt_count=res2.get('rptCount'))
                print("修改之前的名称", res2.get('name')+'666')
                print("描述", res2.get('desc'))
                pytest_check.equal(res3.get('status'), 1)















