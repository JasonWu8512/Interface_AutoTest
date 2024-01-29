# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 11:28 上午
# @Author  : zoey
# @File    : ApiGroup.py
# @Software: PyCharm
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGroup:
    """
    eshop 商城管理后台
    """
    root = '/api/admin/eshop'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_groups(self, pageNo=1, pageSize=20, mobile=None, startAtAfter=None, startAtBefore=None,
                       status='notcompleted', promotionId=None):
        """
        获取拼团列表
        :param pageNo:
        :param pageSize:
        :param sortBy: 开团时间 sortBy='-cts'
        :param promotionId: 活动ID
        :param status: 成团状态（notcompleted：未成团，completed：已成团，expired：已过期）
        :return:
        """
        api_url = f'{self.host}{self.root}/groups'
        q = ''
        if mobile:
            q = f'mobile:={mobile}'
        if startAtAfter and startAtBefore:
            q = q + f' startAt:>={startAtAfter} startAt:<={startAtBefore}'
        # else:
        #     q = '-cts' + q
        body = {
            'pageNo': pageNo,
            'pageSize': pageSize,
            'q': q,
            'status': status,
            'promotionId': promotionId
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_manual_group(self, groupIdList):
        """
        拼团列表 一键成团
        :param groupIdList: 团编号
        :return:
        """
        api_url = f'{self.host}{self.root}/groups/manual'
        body = {
            'groupIdList': groupIdList
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json', headers=self.headers)
        return resp

    def api_navy_group(self, mobileList: list, promotionId: str):
        """
        拼团管理 水军开团
        :param itemId: 商品ID
        :param mobileList: 手机号列表
        :param promitionId: 活动id
        :return:
        """
        api_url = f'{self.host}{self.root}/groups/navy'
        body = {
            'mobileList': mobileList,
            'promotionId': promotionId
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json', headers=self.headers)
        return resp

    def api_group_one_less(self, promotionId: str, mobileList: list):
        """
        批量N缺1开团
        :param promotionId: 活动id
        :param mobileList: 手机号列表
        :return:
        """
        api_url = f'{self.host}{self.root}/groups/one-less'
        body = {
            'promotionId': promotionId,
            'mobileList': mobileList
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json', headers=self.headers)
        return resp

    def api_group_add_one(self, groupId: str):
        """
        手动添加一个机器人
        :param groupId: 拼团id
        :return:
        """
        api_url = f'{self.host}{self.root}/groups/add-one'
        body = {'groupId': groupId}
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='json', headers=self.headers)
        return resp

    def api_down_groups_csv(self, pageNo=1, pageSize=20, startAtAfter=None, startAtBefore=None, status='notcompleted'):
        """
        下载 groups 的详情
        :param status:成团状态（notcompleted：未成团，completed：已成团，expired：已过期）
        :return:
        """
        api_url = f'{self.host}{self.root}/groups/csv'
        if startAtAfter and startAtBefore:
            q = f'startAt:>={startAtAfter} startAt:<={startAtBefore}'
        else:
            q = '-cts'
        body = {
            'pageNo': pageNo,
            'pageSize': pageSize,
            'q': q,
            'status': status
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    eshop = ApiGroup('a087695ab0654cbeb9334c68f9cf3c73')
    # eshop.api_group_add_one('602100f5edca2b18c0a69728')
    # eshop.api_group_one_less(promotionId='DACT_418', mobileList=['18720996803'])
    print(eshop.api_get_groups(status=None, promotionId='DACT_822'))