'''
@Author : degg_wang
@Date : 2022/9/15
@File : test_Service
'''
import time

import pytest
import pytest_check as check
from pytest_check import check_func
from datetime import datetime
from config.env.domains import Domains
from business.Eduplatform.ApiEduplatform_hw import ApiService

@pytest.mark.Eduplatform_hw
@pytest.mark.reg
class TestService(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path()
        Domains.set_domain(cls.config['hw_eduplatform_url'])
        cls.apiservice = ApiService

    def testcase1_create(self):
        '''
        购买服务-正例

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'code': 0, 'data': {'code': 0, 'requestId': '019138f391c2654f'}
        '''
        #获取当前系统时间
        systime=int(round(time.time() * 1000))
        #将当前系统时间设置为开始时间
        startTime=systime
        #在当前系统时间上+10000000000毫秒
        endTime=systime+ 10000000000
        #设置每次不重复的购买服务的uid
        uid="fat_test_uid" + str(systime)
        resp = self.apiservice.ApiService.api_create(self,
                                                    appId="123",
                                                    startTime=startTime,
                                                    endTime= endTime,
                                                    uid= uid)
        print(resp)
        check.equal(resp["status_code"], 200)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 0)

    def testcase2_create(self):
        '''
        购买服务-重复购买，提示已拥有服务

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'code': 0, 'data': {'code': 500, 'msg': 'service already possessed', 'requestId': 'd7e6c1ddf3b13abd'}
        '''

        resp = self.apiservice.ApiService.api_create(self,
                                                    appId="123",
                                                    startTime="1662795332000",
                                                    endTime= "1689301059000",
                                                    uid= "cccc22fc33c74eb6adee3cc4aafc0a8e")
        print(resp)
        check.equal(resp["status_code"], 200)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 500)
        check.equal(resp["data"]["msg"], "service already possessed")

    def testcase3_create(self):
        '''
        购买服务-必参校验：uid

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'timestamp': '2022-09-15T11:04:29.189+0000', 'status': 500, 'error': 'Internal Server Error', 'message': 'param uid not be null', 'path': '/inner/course/service/possess/create', 'status_code': 500
        '''

        resp = self.apiservice.ApiService.api_create(self,
                                                    appId="123",
                                                    startTime="1662795332000",
                                                    endTime= "1689301059000",
                                                    uid= "")
        print(resp)
        check.equal(resp["status_code"], 500)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param uid not be null")

    def testcase4_create(self):
        '''
        购买服务-必参校验：startTime

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'timestamp': '2022-09-16T01:55:16.313+0000', 'status': 500, 'error': 'Internal Server Error', 'message': 'param startTime not be null', 'path': '/inner/course/service/possess/create', 'status_code': 500, 'headers': {'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Date': 'Fri, 16 Sep 2022 01:55:16 GMT', 'Connection': 'close'}, 'cookies': <RequestsCookieJar[]>}
        '''

        resp = self.apiservice.ApiService.api_create(self,
                                                    appId="123",
                                                    startTime="",
                                                    endTime= "1689301059000",
                                                    uid= "cccc22fc33c74eb6adee3cc4aafc0a8e")
        print(resp)
        check.equal(resp["status_code"], 500)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param startTime not be null")

    def testcase5_create(self):
        '''
        购买服务-必参校验：endTime

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'timestamp': '2022-09-16T01:57:27.490+0000', 'status': 500, 'error': 'Internal Server Error', 'message': 'param endTime not be null', 'path': '/inner/course/service/possess/create', 'status_code': 500, 'headers': {'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Date': 'Fri, 16 Sep 2022 01:57:27 GMT', 'Connection': 'close'}, 'cookies': <RequestsCookieJar[]>}
        '''

        resp = self.apiservice.ApiService.api_create(self,
                                                    appId="123",
                                                    startTime="1662795332000",
                                                    endTime= "",
                                                    uid= "cccc22fc33c74eb6adee3cc4aafc0a8e")
        print(resp)
        check.equal(resp["status_code"], 500)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param endTime not be null")

    def testcase6_create(self):
        '''
        购买服务-必参校验：appId

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'timestamp': '2022-09-16T01:59:15.259+0000', 'status': 500, 'error': 'Internal Server Error', 'message': 'param appId not be null', 'path': '/inner/course/service/possess/create', 'status_code': 500, 'headers': {'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Date': 'Fri, 16 Sep 2022 01:59:15 GMT', 'Connection': 'close'}, 'cookies': <RequestsCookieJar[]>}
        '''

        resp = self.apiservice.ApiService.api_create(self,
                                                    appId="",
                                                    startTime="1662795332000",
                                                    endTime= "1689301059000",
                                                    uid= "cccc22fc33c74eb6adee3cc4aafc0a8e")
        print(resp)
        check.equal(resp["status_code"], 500)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param appId not be null")

    def testcase1_remove(self):
        '''
        停止服务-必参校验：uid

        :param appId: appId
        :param uid: 用户id

        :return:
            {'timestamp': '2022-09-16T03:37:44.281+0000', 'status': 500, 'error': 'Internal Server Error', 'message': 'param uid not be null', 'path': '/inner/course/service/possess/remove', 'status_code': 500, 'headers': {'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Date': 'Fri, 16 Sep 2022 03:37:44 GMT', 'Connection': 'close'}, 'cookies': <RequestsCookieJar[]>}
        '''

        resp = self.apiservice.ApiService.api_remove(self,
                                                     appId="1",
                                                     uid="")
        print(resp)
        check.equal(resp["status_code"], 500)
        check.equal(resp["status"], 500)
        check.equal(resp["message"], "param uid not be null")

    def testcase2_remove(self):
        '''
        停止服务-正例

        :param appId: appId
        :param uid: 用户id

        :return:
            {'code': 0, 'data': {'code': 0, 'requestId': 'c9daf041d2524d19'}
        '''
        # 获取当前系统时间
        systime = int(round(time.time() * 1000))
        # 将当前系统时间设置为开始时间
        startTime = systime
        # 在当前系统时间上+10000000000毫秒
        endTime = systime + 10000000000
        # 设置每次不重复的购买服务的uid
        uid = "fat_test_uid" + str(systime)
        #先购买服务，再将购买的服务停止
        self.apiservice.ApiService.api_create(self,
                                                     appId="123",
                                                     startTime=startTime,
                                                     endTime=endTime,
                                                     uid=uid)

        resp = self.apiservice.ApiService.api_remove(self,
                                                     appId="123",
                                                     uid=uid)
        print(resp)
        check.equal(resp["status_code"], 200)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 0)
        # check.equal(resp["message"], "param uid not be null")

    def testcase1_update(self):
        """
        更新服务时间：更新不拥有服务的时间

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'code': 0, 'data': {'code': 500, 'msg': 'service not possessed', 'requestId': '1e211a6bdb8c51c0'}
        """

        resp=self.apiservice.ApiService.api_update(self,
                                                   appId="12345678",
                                                   startTime="1662795332000",
                                                   endTime="1689301059000",
                                                   uid="cccc22fc33c74eb6adee3cc4aafc0a8e"
                                                   )
        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 500)
        check.equal(resp["data"]["msg"], "service not possessed")

    def testcase2_update(self):
        """
        更新服务时间：正例

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'code': 0, 'data': {'code': 0, 'requestId': '1e211a6bdb8c51c0'}
        """
        updatetime=int(round(time.time() * 1000))+10000000
        resp=self.apiservice.ApiService.api_update(self,
                                                   appId="1",
                                                   startTime="1662795332000",
                                                   endTime=updatetime,
                                                   uid="cccc22fc33c74eb6adee3cc4aafc0a8e"
                                                   )
        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["code"], 0)
        # check.equal(resp["data"]["msg"], "service not possessed")

    def testcase3_update(self):
        """
        更新服务时间：必参校验-uid

        :param appId: appId
        :param startTime: 开始时间
        :param endTime: 结束时间
        :param uid: 用户id

        :return:
            {'code': 500, 'msg': 'internal server error',
        """
        updatetime=int(round(time.time() * 1000))+10000000
        resp=self.apiservice.ApiService.api_update(self,
                                                   appId="1",
                                                   startTime="1662795332000",
                                                   endTime=updatetime,
                                                   uid=""
                                                   )
        print(resp)
        check.equal(resp["code"], 500)
        check.equal(resp["msg"], "internal server error")
        # check.equal(resp["data"]["msg"], "service not possessed")

    def testcase1_getPossessPeriod(self):
        """
        获取用户购课时间-必参校验：uid

        :param appId: appId
        :param uid: 用户id

        :return:
            {'timestamp': '2022-09-19T07:10:22.450+0000', 'status': 500, 'error': 'Internal Server Error', 'message': 'param uid not be null', 'path': '/inner/course/service/possess/getPossessPeriod', 'status_code': 500, 'headers': {'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Date': 'Mon, 19 Sep 2022 07:10:22 GMT', 'Connection': 'close'}, 'cookies': <RequestsCookieJar[]>}
        """
        resp=self.apiservice.ApiService.api_getPossessPeriod(self,
                                                             appId='1',
                                                             uid='')

        print(resp)
        check.equal(resp["status"], 500)
        check.equal(resp["error"], "Internal Server Error")
        check.equal(resp["message"], "param uid not be null")


    def testcase2_getPossessPeriod(self):
        """
        获取用户购课时间-正例

        :param appId: appId
        :param uid: 用户id

        :return:
            {'code': 0, 'data': {'uid': 'cccc22fc33c74eb6adee3cc4aafc0a8e', 'appId': '1', 'startTime': 1662795332000, 'endTime': 1663318752906}, 'requestId': '933eac90c50257f8', 'status_code': 200, 'headers': {'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Date': 'Mon, 19 Sep 2022 07:14:58 GMT', 'Keep-Alive': 'timeout=60', 'Connection': 'keep-alive'}, 'cookies': <RequestsCookieJar[]>}
        """
        resp=self.apiservice.ApiService.api_getPossessPeriod(self,
                                                             appId='1',
                                                             uid='cccc22fc33c74eb6adee3cc4aafc0a8e')

        print(resp)
        check.equal(resp["code"], 0)
        check.equal(resp["data"]["uid"], "cccc22fc33c74eb6adee3cc4aafc0a8e")
        check.equal(resp["data"]["appId"], "1")


    def testcase3_getPossessPeriod(self):
        """
        获取用户购课时间-该用户未购课

        :param appId: appId
        :param uid: 用户id

        :return:
            {'code': 0, 'requestId': '83bcb9f7d60d9ac8', 'status_code': 200,
        """
        resp=self.apiservice.ApiService.api_getPossessPeriod(self,
                                                             appId='1',
                                                             uid='test0919')

        print(resp)
        check.equal(resp["code"], 0)
        # check.equal(resp["data"]["uid"], "cccc22fc33c74eb6adee3cc4aafc0a8e")
        # check.equal(resp["data"]["appId"], "1")