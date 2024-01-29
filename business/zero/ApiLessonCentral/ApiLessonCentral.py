# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/22 6:01 下午
@Author  : Demon
@File    : ApiLessonCentral.py
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from urllib import parse
from business.zero.ApiUser.ApiUser import ApiLoginUser
from business.zero.GetUserProperty import GetUserProperty

class ApiLessonCentral(object):

    def __init__(self, token):
        # 请求头文件
        self.host = Domains.config.get('zero_url')
        self.headers = {
            'AUTHORIZATION': token
        }
        self.root = '/v1/lesson'

    # 解析库表名称
    def api_lesson_get_name(self, uid, table, env=None):
        """
        :param uid:  uri ID
        :param table:  基础表名
        :param env:  环境不传会根据当前初始化环境获取
        :return:
        """
        api_url = f"{self.root}/get_name"
        body = {
            'table': table,
            'uid': uid,
            'env': env if env else Domains.config.get('env')
        }

        resp = send_api_request(url=parse.urljoin(self.host, api_url), paramType="json", paramData=body,
                                method="post", headers=self.headers)
        return resp

    def __lesson_score(self, params, operation, env=None):
        """
        :param uri:  url 地址
        :param params:  参数
        :param env:  环境
        :param server_name:  服务器名称
        :return:
        """
        api_url = f"{self.root}/get_lesson_score"
        body = {
            "params": params,
            "operation": operation,
            "server_name": "course.course.atom",
            "env": env if env else Domains.config.get('env')
        }
        resp = send_api_request(url=parse.urljoin(self.host, api_url), paramType="json", paramData=body,
                                method="post", headers=self.headers, verify=False)
        return resp

    def api_lesson_score_remove_record(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_remove', env=env)

    def api_lesson_get_baby_lesson_info(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_get_baby_lesson_info', env=env)

    def api_lesson_get_baby_lesson_info_list(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_get_baby_lesson_info_list', env=env)

    def api_lesson_get_baby_sublesson_info(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_get_baby_sublesson_info', env=env)

    def api_lesson_batch_get_sublesson_info(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_batch_get_sublesson_info', env=env)

    def api_lesson_section_complete(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_section_complete', env=env)

    def api_lesson_sublesson_complete(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_sublesson_complete', env=env)

    def api_lesson_get_userlesson_buy_info(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_get_userlesson_buy_info', env=env)

    def api_lesson_create(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_create', env=env)

    def api_lesson_maSectionComplete(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_maSectionComplete', env=env)

    def api_lesson_batchGetLevelInfo(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_batchGetLevelInfo', env=env)

    def api_lesson_getBabyStudyReportInfo(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_getBabyStudyReportInfo', env=env)

    def api_lesson_getNewerStudyRecordByBid(self, params, env=None):
        """
        :param params:  参数
        :param env:  环境
        :return:
        """
        return self.__lesson_score(params=params, operation='lesson_getNewerStudyRecordByBid', env=env)


if __name__ == '__main__':

    Domains.set_env_path('dev')
    alu = ApiLoginUser()
    alu.api_auth_login(user=Domains.config.get('zero_demon').get('user'),
                       pwd=Domains.config.get('zero_demon').get('pwd'))
    zero_api = ApiLessonCentral(token=GetUserProperty().get_token)
    sd= zero_api.api_lesson_getBabyStudyReportInfo(params=[
        "f37f702ad6064c79bbe1079283a33735",
        "K1GEF005"
], )
    print(sd.get('data'))
    print(zero_api.api_lesson_getNewerStudyRecordByBid(['01d5d2b8a75644a0b65780880365910c']))