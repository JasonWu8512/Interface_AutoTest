# -*- coding: utf-8 -*-
# @Time    : 2021/2/23 10:23 上午
# @Author  : zoey
# @File    : decorators.py
# @Software: PyCharm
import functools
from config.env.domains import Domains


def switch_db(db_key: object) -> object:
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            Domains.DbKey = f'{db_key}_{Domains.Env}'

            try:
                result = func(self, *args, **kw)  # 执行查库操作
            except Exception as e:
                raise e
            return result

        return wrapper

    return decorator