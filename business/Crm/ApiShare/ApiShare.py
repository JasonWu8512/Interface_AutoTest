# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 6:25 下午
@Author  : Demon
@File    : ApiShare.py
"""
from utils.middleware.dbLib import check_file_is_exists
import os
import uuid
from config.env.domains import Domains, ROOT_PATH
from urllib import parse
from utils.requests.apiRequests import send_api_request

class ApiShare(object):
    def __init__(self, cookies):
        # 请求头文件
        self.host = Domains.domain
        self.cookies = cookies
        self.root = '/api/share'

    def api_get_student_comments(self, own, uid):
        """
        查询学员信息的备注信息
        :param own 用户自己的id
        :param uid uid
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_student_comments")
        body = {
            'self': own,
            'user_id': uid
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    @check_file_is_exists
    def __get_qiniu_file_name(self, file_path):
        """获取七牛云生成uuid名称"""
        self.qiniu_page_name = f'crm/dev/{uuid.uuid4()}{os.path.splitext(file_path)[-1]}'
        return self.qiniu_page_name

    def api_upload_file(self, file_path):
        """
        :param file_path:  文件对象,校验文件路径是否正确，可在任意方法下增加装饰器，参数必须为 file_path-绝对路径
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/upload_file")
        files = {'file': (file_path.split(r'/')[-1], open(file_path, 'rb'), 'image/jpeg')}
        data = {'file_name': self.__get_qiniu_file_name(file_path=file_path)}

        head_qiniu = {
            "Content-Type": "multipart/form-data",
        }
        return send_api_request(url=api_url, paramType="file", method="post", cookies=self.cookies, headers=head_qiniu,
                                data=data, files=files)
        # assert sd.status_code == requests.codes.ok

    def api_qiniucdn_file(self):
        """七牛云cdn存储文件
        :param file_name: 0d828a60-7357-11eb-9d8a-4991b527e952.jpg
        """
        # file_name = '0d828a60-7357-11eb-9d8a-4991b527e952.jpg'
        api_url = parse.urljoin(Domains.config.get('qiniucdn'), f'{self.qiniu_page_name}')
        return send_api_request(url=api_url, method='get', paramType='file', cookies=self.cookies)

    def api_create_student_comment(self, own, uid, comment, pictures=[]):
        """新增学员备注信息
        :param own 用户自己的id
        :param uid uid
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/create_student_comment")
        body = {
            "self": own,
            "user_id": uid,
            "comment_content": comment,
            "picture_list": pictures
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_search_order(self, user_info=None , order_id=None):
        """
        根据用户信息，查询订单信息
        :param userinfo 学员的瓜号OR手机号
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_order")
        body = {
            "search_info": {
                "user_info": user_info,
                "order_id": order_id
            },
            "order_type": "ALL"
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_user_labels_by_guaid(self, gua_id):
        """
        根据用户信息， 获取学员标签
        :param gua_id 学员的瓜号
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_user_labels_by_guaid")
        body = {
            "gua_id": gua_id
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_operate_user_label(self, gua_id, user_id, user_label_list):
        """
        根据用户信息， 修改学员标签
        :param gua_id 学员的瓜号
        :param user_id 用户的UID
        :param user_label_list 	list如下：
        "user_label_list": [{
        "operation": "delete",  operation——修改标签的方法
        "label_level1": "9.9leads服务转化",
        "label_level2": "购买意愿",
        "label_level3": "羊毛党"
        }]
        修改标签列表方法 insert，delete
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/operate_user_label")
        body = {
            "gua_id": gua_id,
            "user_id": user_id,
            "user_label_list": user_label_list
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_user_lesson_detail(self, user_id, subject_type):
        """
        根据用户信息，查询 呱美2.5-课程信息
        :param user_id  学员的UID
        :param subject_type  学科，all，english(传空默认英语)，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_user_lesson_detail")
        body = {
            "user_id": user_id,
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_current_learning_level(self, user_id, baby_id, subject_type):
        """
        根据用户和宝贝信息，查询呱美2.5-获取在学级别
        :param user_id  学员的UID
        :param baby_id  宝贝的ID
        :param subject_type  学科，english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_current_learning_level")
        body = {
            "user_id": user_id,
            "baby_id": baby_id,
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_change_learning_level(self,user_id, baby_id,learning_level, subject_type):
        """
        根据用户信息，切换在学级别
        :param user_id  用户的UID
        :param baby_id  宝贝的ID
        :param learning_level 当前在学级别 (T1GE,T1MA等)
        :param subject_type  学科，english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/change_learning_level")
        body = {
            "user_id": user_id,
            "baby_id": baby_id,
            "learning_level": learning_level,
            "subject_type": subject_type
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_baby_course_detail(self, userinfo, baby_id, subject_type):
        """
        根据用户和宝贝信息，查询 呱美2.5-宝贝学习记录
        :param userinfo  学员的瓜号OR手机号
        :param baby_id  宝贝的ID
        :param subject_type  学科，english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_baby_course_detail")
        body = {
            "id_or_phone": userinfo,
            "baby_id": baby_id,
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp




if __name__ == '__main__':
    from business.Crm.ApiAccount.userProperty import UserProperty
    # from utils.middleware import file_path
    dm = Domains()
    config = dm.set_env_path('dev')
    dm.set_domain(config['crm_number_url'])
    user = UserProperty(email_address=config.get('xcrm').get('email_address'), pwd=config.get('xcrm').get('pwd'))
    crm_share = ApiShare(cookies=user.cookies)
    from config.env.domains import ROOT_PATH

    file = os.path.join(ROOT_PATH, 'utils/static/kb37.jpeg')
    #crm_share.api_get_student_comments(uid=user.uid, own=)
    crm_share.api_upload_file(file_path=file)
    print(crm_share.api_qiniucdn_file())
    # print(crm_share.api_test(file))


