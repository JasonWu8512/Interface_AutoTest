#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 1:55 下午
# @Author : liang_li
# @Site : 
# @File : ApiCouponAdmin.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from utils.format.format import dateToTimeStamp
import time
import datetime

class ApiCouponAdmin:
    """
    优惠券
    """
    root = '/api/coupon'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_create_edit_coupon(self, couponName, describes, maxNum, startTime, endTime, refIds, reward, strategyCondition,
                          redirectUrl=None, timeType=0, isEnable=1):
        """
        优惠券-新增优惠券
        :param couponName: 优惠券名称
        :param describes: 优惠券说明
        :param maxNum: 最大发放量
        :param startTime: 优惠券生效开始时间
        :param endTime: 优惠券生效结束时间
        :param refIds: 适用商品list
        :param reward: 优惠券金额（最多两位小数）
        :param strategyCondition: 满XX可用（最多两位小数）
        :param redirectUrl: 跳转链接
        :param isEnable: 是否上架（1：上架，0：下架）
        :param timeType: 有效期类型（0: 固定有效时间，1：获得后有效时间）
        :return:
        """
        api_url = f'{self.host}{self.root}/save'
        body = {
            'coupon': {
                'couponName': couponName,
                'describes': describes,
                'isEnable': isEnable,
                'maxNum': maxNum,
                'redirectUrl': redirectUrl,
                'timeType': timeType,
                'startTime': startTime,
                'endTime': endTime
            },
            'couponScopeList': [
                {
                    'refType': 1,
                    'subRefType': 1,
                    'refIds': ['ALL']
                },
                {
                    'refType': 2,
                    'subRefType': 3,
                    'refIds': refIds
                },
                {
                    'refType': 3,
                    'subRefType': 1,
                    'refIds': ['ALL']
                }
            ],
            'couponStrategySaveReq': {
                'reward': reward,
                'rewardType': 1,
                'strategyCondition': strategyCondition,
                'strategyType': 3
            }
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_query_coupon(self, page=1, pageSize=20):
        """
        优惠券-查询优惠券列表
        :param page: 页面编号
        :param pageSize: 页面大小
        :return:
        """
        api_url = f'{self.host}{self.root}/query'
        body = {
            'page': page,
            'pageSize': pageSize
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_modify_coupon_status(self, couponId, isEnable):
        """
        优惠券-查询优惠券列表
        :param couponId: 优惠券ID
        :param isEnable: 优惠券上下架状态（0：下架，1：上架）
        :return:
        """
        api_url = f'{self.host}{self.root}/status/modify'
        body = {
            'couponId': couponId,
            'isEnable': isEnable
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    channel = ApiCouponAdmin(token='eeb2cb6fdd5740ef9769925a5eb49f3f')
    # print(channel.api_create_edit_coupon(couponName='自动化调试1', describes='自动化调试1', maxNum=10, startTime=1627055999000,
    #                                 endTime=1627055999000, reward=6, strategyCondition=16, refIds=["Liang_SGU_GE"]))
    # print(channel.api_query_coupon())
    # coupon_list = channel.api_query_coupon()
    # edit_coupon = coupon_list['data']['couponList'][0]
    # edit_coupon.update({'maxNum': 20})
    # print(edit_coupon)
    # print(channel.api_edit_coupon(couponbody=edit_coupon, maxNum=20))
    # print(dateToTimeStamp())
    # print(int(time.mktime(datetime.date.today().timetuple())))
    # print(channel.api_create_edit_coupon(couponName='自动化调试3', describes='自动化调试3', maxNum=10, startTime=dateToTimeStamp(),
    #                                      endTime=dateToTimeStamp(day=1), reward=6, strategyCondition=16,
    #                                      refIds=["Liang_SGU_GE"]))
    print(channel.api_modify_coupon_status(couponId=65, isEnable=1))