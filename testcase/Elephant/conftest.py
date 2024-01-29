# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/4 12:39 上午
@Author  : Demon
@File    : apirequest.py
"""
import random

import pytest
from business.Elephant.ApiBasic import ApiUser
from config.env.domains import Domains
from business.Elephant.ApiBasic.GetUserProper import GetUserProper



@pytest.fixture(scope='session')
def login():
    asuser = GetUserProper(user='', pwd='')
    Domains.set_env_path('dev')

    return asuser.get_token
