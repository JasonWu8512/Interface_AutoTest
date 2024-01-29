# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 4:28 下午
# @Author  : zoey
# @File    : apollo.py
# @Software: PyCharm

import requests
from utils.format.format import get_any_time


class Apollo:
    host = 'http://zero.jiliguala.com'

    def __init__(self, token):
        self.headers = {'Authorization': token}

    def get_apollo_apps(self):
        """
        获取已配置的应用
        """
        res = requests.get(url=f'{self.host}/v1/dataTool/apollo/config/apps', headers=self.headers)
        res.raise_for_status()
        return res.json()

    def get_app_items(self, app_id):
        """获取应用可编辑的配置项"""
        res = requests.get(url=f'{self.host}/v1/dataTool/apollo/config/app/{app_id}/items', headers=self.headers)
        return res.json()

    def update_item_and_release(self, app_id, key, value):
        """
        修改并发布配置
        """
        edit_item = {}
        datas = self.get_app_items(app_id)['data']
        for data in datas:
            for item in data['items']:
                if item['key'] == key:
                    edit_item = item
                    edit_item['namespace'] = data['namespace']
                    break
        if not edit_item:
            raise ValueError('该key目前没有配置可编辑，请联系相关人员在测试平台添加')
        edit_item['value'] = value
        res = requests.put(url=f'{self.host}/v1/dataTool/apollo/config/app/{app_id}/item/update', json=edit_item, headers=self.headers)
        res.raise_for_status()
        release_body = {
            'comment': '',
            'namespace': edit_item['namespace'],
            'title': get_any_time() + '_release'
        }
        release_res = requests.post(url=f'{self.host}/v1/dataTool/apollo/config/app/{app_id}/item/release', json=release_body,
                                    headers=self.headers)
        release_res.raise_for_status()
        return release_res.json()



if __name__ == '__main__':
    from business.zero.ApiUser.ApiUser import ApiLoginUser
    user = ApiLoginUser('zoey_zhang@jiliguala.com')
    apollo = Apollo(user.get_zero_token)
    # items = apollo.get_app_items('backend.phoenix.home-server')
    res = apollo.update_item_and_release(app_id='backend.phoenix.home-server', key='server.lesson.english.3.switch', value='true')



