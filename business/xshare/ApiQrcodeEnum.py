# coding=utf-8
# @Time    : 2021/03/15 6:33 下午
# @Author  : qilijun
# @File    : ApiQrcodeEnum.py
# @Software: PyCharm

from enum import Enum

class QrcodeEnum(Enum):
    """"
    xshare服务接口枚举类
    type:"二维码类型", allowableValues = "TEMP, PERM"
    """
    TEMP = "TEMP"
    PERM = "PERM"

