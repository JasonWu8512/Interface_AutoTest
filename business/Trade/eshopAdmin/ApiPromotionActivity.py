# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:28 上午
# @Author  : zoey
# @File    : ApiPromotionActivity.py
# @Software: PyCharm
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPromotionActivity:
    """
    eshop 商城管理后台
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain



    def api_get_promotion_activities(self, pageNo=1, pageSize=20, sortBy='-createdAt', eventStatus='all', enable=''):
        """
        拼团管理-获取活动列表
        :param pageNo: 当前页数
        :param pageSize: 每页数据量
        :param sortBy: 排序字段 createdAt 按创建时间倒序
        :param eventStatus:
        :param enable:
        :return:
        """
        api_url = f'{self.host}{self.root}/promotion-activities'
        body = {
            'pageNo': pageNo,
            'pageSize': pageSize,
            'sortBy': sortBy,
            'eventStatus': eventStatus,
            'enable': enable
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params',
                                headers=self.headers)
        return resp

    def api_create_promotion_activity(self, promotionActivityBody):
        """
        -拼团管理 -新增拼团
        :param promotionActivityBody:
        :return:
        """
        api_url = f'{self.host}{self.root}/promotion-activities'
        body = promotionActivityBody
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_get_promotion_activity_detail(self, promotionId):
        """
        -拼团管理 获取拼团活动详情
        :param promotionId:
        :return:
        """
        api_url = f'{self.host}{self.root}/promotion-activity/{promotionId}'
        resp = send_api_request(url=api_url, method='get', headers=self.headers)
        return resp

    def api_edit_promotion_activity_detail(self, promotionId, enable=True, startAt=None, endAt=None, intro=None):
        """
        -拼团管理 编辑拼团活动信息
        :param promotionId: 活动id
        :param enable: 是否启用
        :param startAt: 拼团开始时间
        :param endAt: 拼团结束时间
        :param intro:拼团说明
        :return:
        """
        api_url = f'{self.host}{self.root}/promotion-activity/{promotionId}'
        body = {
            'enable': enable,
            'startAt': startAt,
            'endAt': endAt,
            'intro': intro,
        }
        resp = send_api_request(url=api_url, method='patch', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_create_v2_promotion_activity(self, promotionActivityV2Body):
        """
        -拼团管理 -新增拼团
        :param promotionActivityBody:商品参数
        :return:
        """
        api_url = f'{self.host}{self.root}/v2/promotion-activities'
        body = promotionActivityV2Body
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json',
                                headers=self.headers)
        return resp

    def api_get_v2_promotion_activities(self, pageNo=1, pageSize=10, startAtAfter=None, startAtBefore=None,
                                        intro=None, eventStatus=None, enable=True, promotionPriceAfter=0,
                                        promotionPriceBefore=9999900):
        """
        获取拼团活动列表-v2
        :param pageNo: 页面编号
        :param pageSize: 一页展示的商品数量
        :param startAtAfter: 活动开始时间
        :param startAtBefore: 活动结束时间
        :param intro: 活动名称
        :param eventStatus: 拼团状态（None：全部，pending：未开始，processing：进行中，finished：已结束）
        :param enable: 启用状态（None：全部，True：启用， False：禁用）
        :param promotionPriceAfter：拼团最低价（单位：分）
        :param promotionPriceBefore：拼团最高价（单位：分）
        """
        api_url = f'{self.host}{self.root}/v2/promotion-activities'
        q = f'promotionPrice:>={promotionPriceAfter} promotionPrice:<={promotionPriceBefore}'
        if enable:
            q = q + f' enable:={enable}'
        if startAtAfter:
            q = q + f' startAt:>={startAtAfter}'
        if startAtBefore:
            q = q + f' startAt:<={startAtBefore}'
        if intro:
            q = q + f' intro:={intro}'
        if eventStatus:
            q = q + f' eventStatus:={eventStatus}'
        body = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "q": q
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_get_v2_promotion_activities_csv(self, startAtAfter=None, startAtBefore=None, intro=None, eventStatus=None,
                                            enable=True, promotionPriceAfter=0, promotionPriceBefore=9999900):
        """
        下载活动详情
        :param startAtAfter: 活动开始时间
        :param startAtBefore: 活动结束时间
        :param intro: 活动名称
        :param eventStatus: 拼团状态（None：全部，pending：未开始，processing：进行中，finished：已结束）
        :param enable: 启用状态（None：全部，True：启用， False：禁用）
        :param promotionPriceAfter：拼团最低价（单位：分）
        :param promotionPriceBefore：拼团最高价（单位：分）
        """
        api_url = f'{self.host}{self.root}/v2/promotion-activities/csv'
        q = f'promotionPrice:>={promotionPriceAfter} promotionPrice:<={promotionPriceBefore}'
        if enable:
            q = q + f' enable:={enable}'
        if startAtAfter:
            q = q + f' startAt:>={startAtAfter}'
        if startAtBefore:
            q = q + f' startAt:<={startAtBefore}'
        if intro:
            q = q + f' intro:={intro}'
        if eventStatus:
            q = q + f' eventStatus:={eventStatus}'
        body = {
            "q": q
        }
        resp = send_api_request(url=api_url, method='get', paramData=body,
                                paramType='params', headers=self.headers)
        return resp