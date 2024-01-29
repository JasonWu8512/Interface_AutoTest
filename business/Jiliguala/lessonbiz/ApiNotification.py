# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/6/1  6:36 下午
@Author   : Anna
@File     : ApiNotification.py
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiNotification():
    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/notification'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_post_notification(self, context, icon, target, uids):
        """
        购买大包赠送呱呱阅读vip卡
        @param context:站内信内容
        @param icon：图标
        @param target:站内信目标链接
        @param uids:接收对象
        @return：
        """
        api_url = f"{self.host}{self.root}/vip"
        body = {
            "context": context,
            "icon": icon,
            "target": target,
            "uids": [uids]
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

if __name__ == '__main__':
    dm=Domains()
    config=dm.set_env_path("fat")
    user=UserProperty("19393112340")
    token=user.basic_auth
    version=config['version']['ver11.0']
    vip=ApiNotification(token,version)
    resp=vip.api_post_notification("赠送呱呱阅读vip卡","xx","JLGL://paidlist","c3319c0a6c054599b465c373b20e83a7")
    print(resp)
