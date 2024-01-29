#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/5/21 4:12 下午
# @Author : liang_li
# @File : ApiPromotion.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPromotion:
    """
    优惠中心相关接口
    """

    def __init__(self):
        self.host = Domains.config['eshop']['promotion_server_url']
        self.root = '/api/promotion'
        self.headers = {"Content-Type": "application/json"}

    def api_promotion_calculate(self, userNo, commodityNo, orderPlatform='ESHOP', activityPrice=None, num=1):
        """
        计算优惠
        :param userNo: 用户uid
        :param commodityNo: sguid
        :param orderPlatform: 平台
        :param activityPrice: 活动价
        :param num: 购买数量
        :return:
        """
        api_url = f'{self.host}{self.root}/calculate'
        body = {
            'user': {
                'userNo': userNo,
            },
            'promotionCalculateCommodityReqList': [
                {
                    'num': num,
                    'commodityNo': commodityNo,
                    'activityPrice': activityPrice
                }
            ],
            'order': {
                'orderPlatform': orderPlatform
            }
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_user_subject_seq_operation(self, userNo, subjectSeqList:list, operationType='SAVE'):
        """
        记录用户学科
        :param userNo: 用户uid
        :param subjectSeqList: 由dict组成的list，dict包含key为：price、subjectCourseType、subjectType
        subjectCourseType(UNKNOWN:未知,FORMAL_COURSE:正价课,TRIAL_COURSE:体验课,FORMAL_TEACHING_AIDS:正价课教具，SIX_WEEK_COURSE：双周课)
        subjectType(UNKNOWN:未知,ENGLISH:英语,LOGIC:思维,CHINESE:语文)
        :param operationType: 操作类型(UNKNOWN:未知,SAVE:保存,DELETE:删除)
        :return:
        """

        api_url = f'{self.host}{self.root}/subject/seq/save'
        body = {
            'userNo': userNo,
            'subjectSeqList': subjectSeqList,
            'operationType': operationType
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    config = Domains.set_env_path('fat')
    promotion = ApiPromotion()
    subject_seq = [{'subjectType': 'ENGLISH', 'subjectCourseType': 'FORMAL_COURSE', 'price': 0}]
    print(promotion.api_user_subject_seq_operation('d2d90cc3b9ff453ba2db476339f80443', subject_seq))
    # print(promotion.api_promotion_calculate(userNo='d2d90cc3b9ff453ba2db476339f80443', commodityNo='Ian-Test-MA'))