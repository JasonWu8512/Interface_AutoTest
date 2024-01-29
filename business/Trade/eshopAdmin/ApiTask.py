# -*- coding: utf-8 -*-
# @Time: 2021/5/5 3:42 下午
# @Author: ian.zhou
# @File: ApiTask
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTask:
    """
    eshop 商城管理后台
    """
    root = '/api/admin/eshop/tasks'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_set_spu_batch_task(self, executeAt, state, spuIdList:list):
        """
        批量设置SPU修改状态定时任务
        :param executeAt: 执行时间
        :param state: 目标状态 0：编辑中 1：已启用 2：已下架 3：已禁用
        :param spuIdList: spu id（list类型）
        :return:
        """

        api_url = f'{self.host}{self.root}'
        body = {
            'executeAt': executeAt,
            'taskData': {
                'state': state,
            },
            'spuIdList': spuIdList,
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    task = ApiTask(token='9d6999362eb34e6897716e5f223f8a7a')
    print(task.api_set_spu_batch_task(executeAt=1620204946000, state=1, spuIdList=[1662]))
