# -*- coding: utf-8 -*-
"""
@Time    : 2020/11/12 11:30 上午
@Author  : Demon
@File    : common.py
"""
import time
import pymysql
from enum import Enum, unique


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "ContentType": "application/json;charset=UTF-8"
}


TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkZW1vbl9qaWFvQGppbGlndWFsYS5jb20iLCJleHAiOjE2MDc0MDUzMjMsImlhdCI6MTYwNzMxODkyM30.4YTzFS0C2B-BvzuwkY6AbPSYB0d76rlFCAA7Z7OUP-OJN5MS3z9lHGzRHlU6FcFn8rsE_iuqjILwNMW0o-TfAQ"

@unique
class Xenum(Enum):
    EQUAL = "="
    # L_EQUAL = "<"
    # G_EQUAL = ">"
    NOT_EQUAL = "<>"
    IS_IN = "in"
    IS_NOT_IN = "not in"
    IS_NULL = "is null"
    IS_NOT_NULL = "is not null"
    LIKE = "like"
    NOT_LIKE = "not like"

@unique
class DEV(Enum):
    DEV = "DEV"
    PRO = "PRO"
    PRE = "PRE"


class REPORT_STATUS(Enum):
    ALLS = (None, "全部")
    DONE = (1, "已通过")
    REFUSED = (2, "已拒绝")
    WAITING = (0, "待通过")
    FAILED = (3, "已作废")



