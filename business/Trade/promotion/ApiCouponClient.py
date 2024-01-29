#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 6:06 下午
# @Author : liang_li
# @Site : 
# @File : ApiCouponClient.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCouponClient:
    """
    优惠中心-优惠券C端接口
    """

    def __init__(self):
        self.host = Domains.config['eshop']['promotion_server_url']
        self.root = '/api/coupon'
        self.headers = {"Content-Type": "application/json"}

    def api_coupon_grant(self, userNo, couponId, grantNum):
        """
        优惠券-发放优惠券
        :param userNo: 用户uid
        :param couponId: 优惠券数据库id
        :param grantNum: 发放数量
        :return:
        """
        api_url = f'{self.host}{self.root}/grant'
        body = {
            'userNo': userNo,
            'couponId': couponId,
            'grantNum': grantNum
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_coupon_user_query(self, userNo):
        """
        优惠券-查询用户优惠券
        :param userNo: 用户uid
        :return:
        """
        api_url = f'{self.host}{self.root}/getByUserNo'
        body = {
            'userNo': userNo
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_coupon_user_lock(self, userNo, couponNo, bizNo, bizType=1):
        """
        优惠券-锁定用户优惠券
        :param userNo: 用户uid
        :param couponNo: 优惠券编号
        :param bizNo: 业务编码
        :param bizType: 业务编码类型
        :return:
        """
        api_url = f'{self.host}{self.root}/lock'
        body = [
            {
                'userNo': userNo,
                'couponNo': couponNo,
                'bizNo': bizNo,
                'bizType': bizType
            }
        ]
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_coupon_user_unlock(self, userNo, couponNo, bizNo, bizType=1):
        """
        优惠券-解锁用户优惠券
        :param userNo: 用户uid
        :param couponNo: 优惠券编号
        :param bizNo: 业务编码
        :param bizType: 业务编码类型
        :return:
        """
        api_url = f'{self.host}{self.root}/unlock'
        body = [
            {
                'userNo': userNo,
                'couponNo': couponNo,
                'bizNo': bizNo,
                'bizType': bizType
            }
        ]
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_coupon_user_verify(self, userNo, couponNo, bizNo, bizType=1):
        """
        优惠券-核销用户优惠券
        :param userNo: 用户uid
        :param couponNo: 优惠券编号
        :param bizNo: 业务编码
        :param bizType: 业务编码类型（1：订单）
        :return:
        """
        api_url = f'{self.host}{self.root}/verify'
        body = [
            {
                'userNo': userNo,
                'couponNo': couponNo,
                'bizNo': bizNo,
                'bizType': bizType
            }
        ]
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    channel = ApiCouponClient()
    # user_coupon = channel.api_coupon_grant(userNo='b95310284a9040e2b3b7c35b764a9ef2', couponId=30, grantNum=1)
    print(channel.api_coupon_user_query(userNo='b95310284a9040e2b3b7c35b764a9ef2'))
    # print(channel.api_coupon_user_lock(userNo='b95310284a9040e2b3b7c35b764a9ef2', couponNo='C83769084283514880',
    #                                    bizNo=123456, bizType=1))
    # print(channel.api_coupon_user_unlock(userNo='b95310284a9040e2b3b7c35b764a9ef2', couponNo='C83769084283514880',
    #                                    bizNo=123456, bizType=1))
    # print(channel.api_coupon_user_verify(userNo='b95310284a9040e2b3b7c35b764a9ef2', couponNo='C83769084283514880',
    #                                    bizNo=123456, bizType=1))