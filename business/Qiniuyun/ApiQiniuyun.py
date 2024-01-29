# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/25 11:36 上午
@Author  : Demon
@File    : ApiQiniuyun.py
"""

from config.env.domains import Domains
from urllib.parse import urljoin
from utils.requests.apiRequests import send_api_request
from utils.middleware.dbLib import check_file_is_exists

class ApiQiniuyun(object):
    """七牛云上传文件 / 图片"""
    def __init__(self, ):
        # 初始化对应平台登陆token
        self.headers = dict(Authorization=Domains.config.get('qiniu_token'))

    def api_parse_qiniu_img(self, project_url_path, platform='qiniu', typ='image_jpeg', **kwargs):
        '''根据七牛云api解析待上传文件
        @project_url_path: 各个项目下解析url路径
        @file_path: 文件的绝对路径
        '''
        url = urljoin(Domains.config.get('url'), project_url_path)
        params = dict(platform=platform, typ=typ, **kwargs)
        return send_api_request(method='get', url=url, paramType='params', paramData=params, headers=self.headers)

    def api_upload_qiniup_img(self, key, token, prefix, file_path):
        """
        上传图片到七牛云,来自解析结果
        :param key:
        :param token:
        :param prefix:
        :param file_path: 文件绝对路径
        :return
        """
        api_url = "http://upload.qiniup.com/"
        data = {
            "key": key,
            "token": token,
            "prefix": prefix,
            # "file": fil,
        }
        files = {'file': (file_path.split(r'/')[-1], open(file_path, 'rb'), 'img/jpeg')}
        head_qiniu = {
            "Content-Type": "multipart/form-data",
        }
        return send_api_request(url=api_url, headers=head_qiniu, method="post",
                                    paramType="file", data=data, files=files, )

    @check_file_is_exists
    def one_key_upload(self, project_url_path, file_path, platform='qiniu', typ='image_jpeg', **kwargs):
        """一键上传文件"""
        resp = self.api_parse_qiniu_img(project_url_path=project_url_path, **kwargs).get('data')

        return self.api_upload_qiniup_img(key=resp['key'], token=resp['token'], prefix=resp['prefix'], file_path=file_path)

if __name__ == '__main__':
    from business.Crm.ApiAccount.userProperty import UserProperty
    from utils.format.format import get_file_absolute_path
    dm = Domains()
    dm.set_env_path('dev')
    # crm_user = UserProperty(email_address=dm.config.get('xcrm').get('email_address'), pwd=dm.config.get('xcrm').get('pwd'))

    # crm_user.
    api_qiniu = ApiQiniuyun()
    data = api_qiniu.api_parse_qiniu_img(project_url_path='/api/youzan/api/access/token', file_path='')
    infos = api_qiniu.api_upload_qiniup_img(key=data.get('data')['key'],
                                    token=data.get('data')['token'],
                                    prefix=data.get('data')['prefix'],
                                    file_path=get_file_absolute_path('kb37.jpeg'))
    # print(data)
    # print(infos)
    print(api_qiniu.one_key_upload(project_url_path='/api/youzan/api/access/token', file_path=get_file_absolute_path('kb37.jpeg')))