import time

import pytest
import pytest_check as check

# def test1():
#     assert 1==1
from pytest_check import check_func
from datetime import datetime
import sys
# a='2'
# b='2'
# c=['2','4','7']
# print(check.equal(a,b,'a=b'))
@check_func
def is_succeed(code):
    assert code == 0 or code ==200

def is_empty(resp_data):
    assert len(resp_data) == 0


def ptest_code():
    pass
    # print(is_succeed(199))
    # print()
    # print(is_succeed(0))
    # print(is_succeed(200))

def ptest_empty():
    try:
        # is_empty('')
        # is_empty({})
        # is_empty({'a':'1','b':'23'})
        is_empty({})
        is_empty([1,2,3,4,'b'])

    except  AssertionError:
        print('该对象不为空')
# ptest_empty()

curtime = datetime.now().microsecond # 获取毫秒 整型格式

systime=int(round(time.time() * 1000))

print(systime)
