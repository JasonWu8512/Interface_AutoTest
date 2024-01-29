# coding=utf-8
# @Time    : 2021/5/12 5:35 下午
# @Author  : Karen
# @File    : __init__.py.py

from business.common.UserProperty import UserProperty
from business.Reading.user.ApiUser import ApiUser
from business.Reading.vip.ApiVip import ApiVip
import time


def logout_mobile(mobile):
    # 注销config配置中的手机账号
    user = UserProperty(mobile)
    vip = ApiVip(token=user.basic_auth)
    vip.api_get_user_sms_logout(mobile)
    db_user = ApiUser().get_jlgl_user(mobile)
    code = db_user['sms']['code']
    print('注销验证码:', code)
    vip.api_delete_user('mobilecode', mobile, code)
    print('先注销手机账号:', mobile)


def logon_mobile(mobile, ggheader):
    # 注册config配置中的手机账号
    resp = ApiUser().api_get_user_sms_login(mobile, ggheader)
    retry = 1
    db_user = None
    while not db_user and retry < 5:
        db_user = ApiUser().get_jlgl_user(mobile)
        time.sleep(2)
        retry += 1
    else:
        print('重新注册手机账号:', mobile)
        id = db_user['_id']
        code = db_user['sms']['code']
        token = ApiUser().get_token(typ="mobilecode", u=mobile, p=code)
        print('手机号token:', token)
        return token
