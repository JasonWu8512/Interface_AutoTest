# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/3 5:48 下午
@Author  : Demon
@File    : bak_bak.py
"""

def limit_report_nums(func, ):
    def inner(*args, **kwargs):
        print('inner')
        data = func(*args, **kwargs)
        return data
    return inner

import itertools

class wraoer(object):
    def __init__(self, name):
        self.name = name

    @limit_report_nums
    def fet_dimens(self, dmine):
        return dmine

if __name__ == '__main__':

    for ip in itertools.product([1, 3, ], [], [3,4]):
        print(ip)

    sd = wraoer('').fet_dimens('abs')
    print(sd)