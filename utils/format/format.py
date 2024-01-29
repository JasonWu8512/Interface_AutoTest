# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 2:22 下午
# @Author  : zoey
# @File    : format.py
# @Software: PyCharm
import base64
import hashlib
import time
import datetime
import math
import os
from dateutil import parser
from config.env.domains import ROOT_PATH
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
Cipher, algorithms, modes
)

def md5(password):
    m = hashlib.md5()
    m.update(password.encode("utf8"))
    return m.hexdigest()

def encrypt(plaintext):
    """AES/GCM/nopadding"""
    CRYPTO_KEY = "609835XIpoL/ngwzEH0J4/farKa53XhT7vEETCBnvXI="
    key = base64.b64decode(bytes(CRYPTO_KEY, "utf-8"))
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize() + encryptor.tag  # 将tag直接追加在最后，即可和java解密代码兼容
    encryptedData = iv + ciphertext
    return base64.b64encode(encryptedData)

def base64_encode(uid, tok):
    """base64加密,用于获取微信鉴权，请求头里面的authorization"""
    auth = uid + ':' + tok
    auth_encode = base64.b64encode(auth.encode('utf-8'))
    authorization = str(auth_encode, encoding="utf-8")
    return 'Basic ' + authorization

def dateToTimeStamp(day=0, hour=0, min=0):
    """获取指定时间的时间戳"""
    dt = (datetime.datetime.now() + datetime.timedelta(days=day, hours=hour, minutes=min)).strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timeStamp = time.mktime(timeArray)
    return timeStamp * 1000

def timeStampToTimeStr(time_stamp:int):
    time_local = time.localtime(time_stamp//1000)
    time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time_local)
    return time_str

def now_timeStr():
    """获取当前时间的字符串形式"""
    dt = time.localtime(time.time())
    time_str = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", dt)
    return time_str

def get_any_time(day=0, hour=0):
    """
    :param n: 与当前日期的天数差，如n=-1时，获取前一天日期，
    :return:
    """
    return (datetime.datetime.now() + datetime.timedelta(days=day, hours=hour)).strftime("%Y-%m-%dT%H:%M:%S")

def get_datetime(day=0, hour=0):
    """
    :param n: 与当前日期的天数差，如n=-1时，获取前一天日期，
    :return:返回时间格式为ISODATE
    """
    dt = (datetime.datetime.now() + datetime.timedelta(days=day, hours=hour)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return parser.parse(dt)

def get_timestr(day=0, hour=0):
    """
    :param n: 与当前日期的天数差，如n=-1时，获取前一天日期，
    :return:返回时间格式为String
    """
    dt = (datetime.datetime.now() + datetime.timedelta(days=day, hours=hour)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return dt

def get_all_page(ins: object, name: str, page_size: int = 10, **kwargs):
    """
    获取分页接口分页的所有数据
    :type ins: object
    :param ins: 实例对象
    :param name: 方法名
    :param page_size: 每页数量
    :return:
    """
    # 获取实例ins中name所对应的可调用方法
    f = getattr(ins, name)
    # 调用f方法
    res = f(pageNo=1, pageSize=page_size, **kwargs).get('data')
    total_page = 1
    datas = []
    content_key = ''
    for key in res.keys():
        # if 'total' in key.lower():
        #     if 'page' in key.lower():
        if 'totalelements' == key.lower() or 'totalcount' == key.lower():
            total_page = math.ceil(res[key] / page_size)
        if isinstance(res[key], list):
            content_key = key
            datas.extend(res[key])
    # 循环调用分页接口获取全量数据
    for page_no in range(2, total_page + 1):
        datas.extend(f(pageNo=page_no, pageSize=page_size, **kwargs)['data'][content_key])
    return datas, res


def get_file_absolute_path(file_name):
    """获取文件的绝对路径,默认存放在static路径下"""
    return os.path.join(ROOT_PATH, f'utils/static/{file_name}')

if __name__ == '__main__':
    appid = "wx6c71f742d227450e"
    t = get_timestr(-30)
    print(t)
    # serverType = "unsilent"
    # userinfo = {
    #     "openid": "oRkr65jD4pTB_fAVTEpn_iqJjKKM",
    #     "unionid": "o0QSN1Q9LrfXC_nJ3y_Wjqw3GEDQ",
    #     "nick": "时光&回忆",
    #     "ava": "https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIEvpEc4PDyPPngDlSyiaFMCp4um7GxkMVeTdXDJ74wXZwITaNRA0mxVANO8SQWaoIR4TLxj7b0pDQ/132"
    # }
    # ee = encryptWechatToken(appid, serverType, userinfo)
    # dt = get_timestr(1)
    # da = parser.parse(dt)
    # print(ee)



