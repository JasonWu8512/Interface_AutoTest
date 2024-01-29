# -*- coding: utf-8 -*-
# @Time: 2021/2/7 4:25 下午
# @Author: ian.zhou
# @File: ApiCommon
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCommon:
    """
    eshop 商城管理后台
    """
    root = '/api/admin/eshop/common'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain


    def api_get_qiniu_img_token(self, mediaType='png'):
        """
        获取七牛图片上传图片凭证
        :param mediaType: 上传图片类型
        :return:
        """

        api_url = f'{self.host}{self.root}/media/token/qiniu'
        body = {
            'type': mediaType
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_get_qiniu_video_token(self, mediaType='mp4'):
        """
        获取七牛图片上传视频凭证
        :param mediaType: 上传视频类型，暂时只支持mp4
        :return:
        """

        api_url = f'{self.host}{self.root}/video/token/qiniu'
        body = {
            'type': mediaType
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp
