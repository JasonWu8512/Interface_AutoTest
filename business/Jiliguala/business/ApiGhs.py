# -*- coding: utf-8 -*-
# @Time    : 2021/6/4 15:26 下午
# @Author  : 万军
# @File    : ApiGhs.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiGhs:
    """
    通用业务服务
    """
    root = '/api/ghs'

    def __init__(self, token):
        self.headers = {'Authorization': token}
        self.host = Domains.domain

    def api_ghs_qrcode(self, uid):
        """
        获取规划师二维码
        :param uid: 用户id
        :return:
        """

        api_url = f'{self.host}{self.root}/qrcode'
        body = {
            'uid': uid
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_ghs_bind_advisor(self, uid):
        """
        扫描规划师二维码添加规划师并获取用户信息
        :param uid: 用户id
        :return:
        """

        api_url = f'{self.host}{self.root}/bindAdvisor'
        body = {
            'uid': uid

        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_ghs_paid(self):
        """
        扫描规划师二维码添加规划师并获取用户信息
        :return:
        """

        api_url = f'{self.host}{self.root}/paid'

        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_ghs_add_back(self, uid, ghs_id, wechat_nick=None, head_img_url=None, tag=None, subject=None):
        """
        规划师反加好友登记
        :param uid: 用户id
        :param wechat_nick: 微信昵称
        :param head_img_url: 头图
        :param ghs_id: 规划师id
        :param tag: 标签
        :param subject: 科目
        :return:
        """

        api_url = f'{self.host}{self.root}/addBack'
        body = {
            'uid': uid,
            'wechatNick': wechat_nick,
            'headImgUrl': head_img_url,
            'ghsId': ghs_id,
            'tag': tag,
            'subject': subject,

        }
        resp = send_api_request(method='put', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_ghs_problem_sms(self, uid):
        """
        规划师二维码页面反馈信息
        :param uid: 用户id
        :return:
        """

        api_url = f'{self.host}{self.root}/problem/sms'
        body = {
            'uid': uid

        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_ghs_change_id(self, uids, ghs_id, subject=None):
        """
        用户分配的规划师ID信息变更
        :param uids: 要更改规划师信息的用户的id
        :param ghs_id: 规划师id
        :param subject: 科目,     * 暂定取值： 英语： English， 语文： Chinese， 思维： Math
        :return:
        """

        api_url = f'{self.host}{self.root}/changeId'
        body = {
            'uids': uids,
            'ghsId': ghs_id,
            'subject': subject

        }
        resp = send_api_request(method='put', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    Ghs = ApiGhs('Basic YTU2YjA2YTg3NmYzNDEyOWE2MjgxZjczNTY0ZjNlZWQ6MmM4NDc1YjZkMjNmNGFlM2E5YjhlNTFhNTc0YjEzOWU=')
    # print(Ghs.api_ghs_add_back(uid='01dd9a50cdbb4faea73d8fd710f6b7ec', ghs_id='91'))
    # print(Ghs.api_ghs_problem_sms(uid='01dd9a50cdbb4faea73d8fd710f6b7ec'))
    print(Ghs.api_ghs_change_id(uids=['01dd9a50cdbb4faea73d8fd710f6b7ec'], ghs_id=648))
