# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/5 3:00 下午
@Author  : Demon
@File    : conftest.py
"""
import pytest
from utils.date_helper import get_time_stamp

@pytest.fixture(scope='session')
def get_uid():
    return f'test-{get_time_stamp()}'