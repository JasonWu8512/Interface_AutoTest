# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/6 11:55 上午
@Author  : Demon
@File    : ApiUserInfo.py
"""



from utils.middleware.dbLib import check_file_is_exists
from config.env.domains import Domains, ROOT_PATH
from utils.requests.apiRequests import send_api_request
from business.Elephant.commons.common import HEADERS as header
from urllib import parse


class ApiUserInfo(object):

    def __init__(self, token):
        """
        :param token: token
        """
        self.headers = dict(
            Cookie="user=" + token,
            Authorization="Bearer " + token,
            **header
        )
        self.host = Domains.domain

    def api_version(self):
        """
        版本信息
        :return: version
        """
        api_url = self.host + "/api_version"
        resp = send_api_request(url=api_url, method="post", headers=self.headers)
        return resp.get("version")

    def api_user_select_user(self, uid="4be2756f72e2473c871c38a830cb5943"):
        """
        查询用户信息
        :return
        """
        body = {"id": uid}
        api_url = self.host + "/api_basic/user/selectUser"
        res = send_api_request(url=api_url, headers=self.headers, method="post", paramData=body, paramType="json")
        return res

    def api_qntoken(self, typ="image_img", pla="qiniu", qiniu_token=''):
        """
        打开图片，解析到七牛云
        :param typ: 图片类型
        :return
        """
        qiniu = "Basic MzdiODJhMmFiMWY4NGE2YmEzNTNhMDk2MDFkYzFlOGM6MTc5ZDkwMmUwODhlNDE3NWFmMmQ1OWRjODJlYTFlMTc="
        headers = {"Authorization": qiniu_token if qiniu_token else qiniu}
        api_url = parse.urljoin(self.host, "/api_qntoken")
        body = {
            "platform": pla,
            "typ": typ
        }
        res = send_api_request(url=api_url, headers=headers, method="get",
                               paramType="params",
                               # paramData="&".join([k + "=" + v for k, v in body.items()]))
                               paramData=parse.urlencode(body))
        # res = requests.Request(url=api_url, headers=headers, method="get", params=param)
        return res

    @check_file_is_exists
    def api_upload_qiniup_img(self, key, tok, pref, file_path):
        """
        上传图片到七牛云,来自解析结果
        :param key:
        :param tok:
        :param pref:
        :param file_path: 文件绝对路径
        :return
        """
        api_url = "http://upload.qiniup.com/"
        data = {
            "key": key,
            "token": tok,
            "prefix": pref,
            # "file": fil,
        }
        files = {'file': (file_path.split(r'/')[-1], open(file_path, 'rb'), 'img/jpeg')}
        head_qiniu = {
            "Content-Type": "multipart/form-data",
        }
        return send_api_request(url=api_url, headers=head_qiniu, method="post",
                               paramType="file", data=data, files=files,)

    def api_user_update_user(self, ava, ids="4be2756f72e2473c871c38a830cb5943", dep="测试部",
                            em="demon_jiao@jiliguala.com", mn="武旭俊", tel="18221278748",
                            did="de86e07c647346468aed3c14038a5530",
                            isma=False, un="焦珂珂", sta=True,
                            padid="ea39502e29be40f1bbfbce30f77c06a2", rol=["b667ad2dece74452b9a29a9cffcdfe46"]):
        """
        更新用户的信息
        :param dep: 部门名称
        :param em: 邮箱地址
        :param mn: 管理员名称
        :param tel: 手机号 up
        :param did: 部门ID
        :param isma: 是否是管理员
        :param ids: 用户id
        :param ava: img url
        :param un: 用户名称
        :param sta: 用户状态
        :param padid: 父级部门id
        :param rol: 角色列表
        :return
        """
        api_url = parse.urljoin(self.host, "/api_basic/user/updateUser")
        body = {
            "deptName": dep,
            "emailAddress": em,
            "manager": mn,
            "phone": tel,
            "deptId": did,
            "isManager": isma,
            "id": ids,
            "avatar": ava,
            "roleList": rol,
            "username": un,
            "status": sta,
            "parentDeptId": padid
        }
        res = send_api_request(url=api_url, headers=self.headers, method="post", paramData=body, paramType="json")
        return res

    def api_logout(self):
        """
        退出登录
        """
        api_url = "/api_basic/auth/logout"
        resp = send_api_request(url=self.host + api_url, method="post", headers=self.headers)
        return resp.get("data").get("uuid")



if __name__ == '__main__':
    # dm = Domains()
    # dm.set_domain("http://10.9.4.124:8088")
    from business.Elephant.ApiBasic.ApiUser import ApiUser
    import os

    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkZW1vbl9qaWFvQGppbGlndWFsYS5jb20iLCJleHAiOjE2MTM5MDE2OTQsImlhdCI6MTYxMzgxNTI5NH0.iJgUo70jX9QL6brrxkFwHa3LRFOYXJBxsYuUxwxO-TJwelubp-DQWkcdAl9wTtfHldwMnb2a0X1U_jsbYV4HQA"
    dm = Domains()
    config = dm.set_env_path('dev')
    dm.set_domain(config.get('elephant_number_url'))
    u = ApiUserInfo(token)
    # df = u.api_user_update_user(ava="https://qiniucdn.jiliguala.com/dev/upload/ed678b4513c74530b224a01e0e9700fe_20201113111706.jpeg")
