# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/10 4:12 下午
@Author  : Demon
@File    : ApiPlanner.py
"""

from config.env.domains import Domains
from urllib import parse
from utils.requests.apiRequests import send_api_request

class ApiPlanner(object):
    def __init__(self, cookies):
        # 实例存放cookies
        self.host = Domains.domain
        self.cookies = cookies
        self.root = '/api/planner'

    def api_get_valid_ghs_list(self):
        """
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_valid_ghs_list")
        return send_api_request(url=api_url, paramType="json", paramData={}, method="post", cookies=self.cookies)

    def api_get_students_tab_counts(self, student_infos):
        """
        :param student_infos:  学员信息  {"ghs_info": {}}
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_students_tab_counts")
        body = {
            "student_infos": student_infos
        }
        return send_api_request(url=api_url, paramData=body, paramType='json', method="post", cookies=self.cookies)

    def  api_get_students(self, student_infos, change_page=False, sorts=[], search_size=25, search_from=0, **kwargs):
        """
        :param student_infos:  学员信息  {"ghs_info": {}}
        :param sort_by:  排序设置  [["gmk_first_buy_date", "desc"]]
        :param search_from:  搜索来源
        :param search_size:  大小
        :return:
        """
        body = {
            "student_infos": student_infos,
            "change_page": change_page,
            "sort_by": sorts,
            "search_from": search_from,
            "search_size": search_size
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_students")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)
    '''
    def api_get_ghs_reference_id_with_wechat_type_and_grou
    p(self, subject_type=''):
        """
        :param subject_type:  学科类型
        :return:
        """
        body = {
            "subject_type": subject_type,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_reference_id_with_wechat_type_and_group")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)
    '''

    def api_get_ghs_wechat_list(self):
        """
        :return:
        """
        body = {}
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_wechat_list")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_ghs_wechat_account(self, ghs_wechat_infos):
        """
        @params:
        :return:
        """
        body = ghs_wechat_infos
        '''
        {
            "email_address": email_address,
            "wechat_nick": wechat_nick,
            "wechat": wechat,
            "wechat_type": wechat_type,
            "wechat_weights": wechat_weights,
            "wechat_code": wechat_code,
            "wechat_account_id": wechat_account_id
        }'''
        api_url = parse.urljoin(self.host, f"{self.root}/update_ghs_wechat_account")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def fmt_api_update_ghs_wechat_account(self, old_params={}, **kwargs):
        """格式化输出对应api的参数,"""
        # old_params = {} if not old_params else old_params
        old_params.update(**kwargs)
        return old_params

    def api_add_ghs_wechat_account(self, ghs_wechat_infos):
        """
        @params:
        :return:
        """
        body = ghs_wechat_infos
        '''{
            "email_address": email_address,
            "wechat_nick": wechat_nick,
            "wechat": wechat,
            "wechat_type": wechat_type,
            "wechat_weights": wechat_weights,
            "wechat_code": wechat_code,
        }'''
        api_url = parse.urljoin(self.host, f"{self.root}/add_ghs_wechat_account")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_migrate_ghs_wechat_account(self,old_email,new_email,wechat_account_id):
        """
        @params:
        :return:
        """
        body = {
            "old_email": old_email,
            "new_email": new_email,
            "wechat_account_id": wechat_account_id
        }
        api_url = parse.urljoin(self.host, f"{self.root}/migrate_ghs_wechat_account")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_baby_list(self,id_or_phone):
        api_url = parse.urljoin(self.host, f"{self.root}/get_baby_list")
        body = {
            "id_or_phone": id_or_phone
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp
    def api_get_ghs_enum_types(self):
        """
        获取规划师班次状态枚举类型
        :param
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_enum_types")
        body = {

        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_ghs_reference_id_with_wechat_type_and_group(self, subject_type):
        """
        规划师id管理页，根据科目获取规划师相关信息
        :param subject_type  学科，english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_reference_id_with_wechat_type_and_group")
        body = {
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_ghs_user_list(self,subject_type):
        """
        获取某一科目的规划师id和邮箱信息
        :param subject_type  学科，english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_user_list")
        body = {
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_ghs_user(self, user_id):
        """
        根据用户UID获取相关信息
        :param user_id  用户UID
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_user")
        body = {
            "user_id": user_id
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_update_ghs_user_status(self, email_address, ghs_work_time_id, status_id):
        """
        根据用户和宝贝信息，查询 呱美2.5-宝贝学习记录
        :param email_address  规划师邮箱
        :param ghs_work_time_id  规划师班次
        :param status_id  规划师状态，停接，请假，在职，离职
        :return: 该接口的返回是固定的，如下
        {
        "rc": 0,
        "data": null
        }
        需要配合接口：https://dev-crm.jiliguala.com/api/planner/get_ghs_wechat_list 校验更新是否成功

        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/update_ghs_user_status")
        body = {
            "email_address": email_address,
            "ghs_work_time_id": ghs_work_time_id,
            "status_id": status_id
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_auto_generate_ghs_schedule(self, schedule_date_list, subject_type):
        """
        根据学科和排班时间，进行一键排班，需要配合其他接口设计场景case.
        :param schedule_date_list  排班日期list
        :param subject_type  学科，english，math
        :return 是固定的:
        {
        "rc": 0,
        "data": null
        }
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/auto_generate_ghs_schedule")
        body = {
            "subject_type": subject_type,
            "schedule_date_list": schedule_date_list
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_ghs_schedule_by_date(self, schedule_date, subject_type):
        """
        根据当前日期和科目，返回已排班和未排班的规划师信息。
        :param schedule_date 当前排班日期
        :param subject_type  学科，english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_schedule_by_date")
        body = {
            "schedule_date": schedule_date,
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_update_ghs_schedule(self, schedule_date, schedule_info, subject_type):
        """
        保存手动排班结果
        :param schedule_date  当前排班日期
        :param schedule_info  排班详情，已排班A[]，B[]，C[]，未排班 nonScheduleInfo[]
        :param subject_type  学科，english，math
        :return 返回固定:
        {
        "rc": 0,
        "data": null
        }
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/update_ghs_schedule")
        body = {
            "schedule_date": schedule_date,
            "schedule_info": schedule_info,
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_referral_detail(self, userinfo, user_type, subject_type):
        """
        根据用户信息，查询 呱美2.5-课程信息
        :param userinfo  用户的呱号或手机号
        :param user_type  正价课转化 referral_all，referral_succ，referral_fail
        :param subject_type  学科，all，english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_referral_detail")
        body = {
            "id_or_phone": userinfo,
            "user_type": user_type,
            "subject_type": subject_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_learning_map_list(self, uid, search_from, search_size=25, **kwargs):
        """
        根据用户和宝贝信息，查询 呱美2.5-宝贝学习记录
        :param uid  用户UID
        :param search_from  目前参数都为0 ，具体不详
        :param search_size  默认25
        :param subject_type  后续会区分学科，english，math
        :param 非必填参数 **kwargs：
        "day_str": day_str, 学习地图周期，一般是某天"day_str": "2021-03-09",
        "feedback": feedback, 反馈结果
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_learning_map_list")
        body = {
            "uid": uid,
            "search_from": search_from,
            "search_size": search_size
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_lottery_detail(self, userinfo):
        """
        根据用户的呱号或手机号，查询用户活动信息
        :param userinfo  用户的呱号或手机号
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_lottery_detail")
        body = {
            "id_or_phone": userinfo
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_point_detail(self, userinfo):
        """
        根据用户的呱号或手机号，查询用户的魔石和钻石信息
        :param userinfo  用户的呱号或手机号
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_point_detail")
        body = {
            "id_or_phone": userinfo
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_lesson_detail(self, userinfo):
        """
        根据用户的呱号或手机号，查询用户的课程信息
        :param userinfo  用户的呱号或手机号
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_lesson_detail")
        body = {
            "id_or_phone": userinfo
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_search_app_order_v2(self, search_info,change_page=False):
        """
        根据查询条件，查询app订单
        :param search_info 搜索条件
        :param change_page
        "search_info": {
                "stu_info": "",
                "order_id": "",
                "ghs_info": {},
                "period": "",
                "pay_time_start": "",
                "pay_time_end": "",
                "is_in_kpi": "",
                "order_status": "",
                "subject_type": ""
            },
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_app_order_v2")
        body = {
            "search_info": search_info,
            "change_page": change_page,
            "search_from": 0,
            "search_size": 25
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_export_app_order_v2(self, search_info):
        """
        根据查询条件，查询导出订单
        :param search_info  搜索条件
        {
                "ghs_info": {},
                "stu_info": "",
                "order_id": "",
                "platform": "",
                "subject_type": "",
                "pay_time_start": "",
                "pay_time_end": "",
                "order_status": "",
                "period": "",
                "is_in_kpi": ""
            }
        :return:
        {
        "rc": 0,
        "data": {
        "doc_key": "app_order_v2/ee1c2745d7b94336bc9f1295ccd99732_2021-03-05_5fd5c9639a954c81ba173fd98e891b6d.csv"
            }
        }
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/export_app_order_v2")
        body = {
            "search_info": search_info
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_export_student_list(self):
        """
        导出订单第二步骤，返回学生信息
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/export_student_list")
        body = {

        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_search_youzan_order(self, search_info,change_page=False):
        """
        根据查询条件，查询app订单
        :param search_info 搜索条件
        {
                "ghs_info": {},
                "period": "",
                "stu_info": "",
                "order_id": "",
                "pay_time_start": "",
                "pay_time_end": "",
                "is_in_kpi": "",
                "is_kpi_wrong": "",
                "order_status": "",
                "match_source": ""
            }
        :param change_page
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_youzan_order")
        body = {
            "search_info": search_info,
            "change_page": change_page,
            "search_from": 0,
            "search_size": 25
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_search_unmatched_order(self, search_info, change_page=False):
        """
        根据订单号，订单支付时间，订单状态搜索订单
        :param search_info 搜索条件
        {
                    "order_id": "E20200927142721035004117",
                    "pay_time_start": "",
                    "pay_time_end": "",
                    "match_status": ""
                },
        :param
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_unmatched_order")
        body = {
                "search_info": search_info,
                "change_page": change_page,
                "search_from": 0,
                "search_size": 25
            }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_search_match_detail(self, search_info, change_page=False):
        """
        根据订单号，规划师信息，订单支付时间，订单状态搜索订单
        :param search_info 搜索条件
        {
                "ghs_info": {
                    "subject": "math",
                    "group": "M01"
                },
                "order_id": "",
                "match_status": "",
                "apply_time_start": "",
                "apply_time_end": ""
            }
        :param change_page
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_match_detail")
        body = {
            "search_info": search_info,
            "change_page": change_page,
            "search_from": 0,
            "search_size": 25
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_apply_status(self, order_id):
        """
        根据订单id, 查询订单认领状态
        :param order_id  订单id
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_apply_status")
        body = {
            "order_id": order_id
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_ghs_by_guaid(self, gua_id):
        """
        根据呱号信息，查询呱号所属的规划师信息
        :param gua_id  学员的呱号
        :return:
        {
        "rc": 0,
        "data": {
        "ghs_name": "paibanceshi10",
        "ghs_email": "paibanceshi10@jiliguala.com",
        "ghs_group": "Y"
            }
        }
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_by_guaid")
        body = {
            "gua_id": gua_id
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_apply_match_detail(self, order_id, ghs_info, apply_comment, apply_photo, gua_id):
        """
        根据用户和宝贝信息，查询呱美2.5-获取在学级别
        :param order_id  认领订单的编号
        :param ghs_info  规划师信息
        ghs_info :{
                    "ghs_email": "paibanceshi10@jiliguala.com",
                    "ghs_group": "Y"
                }
        :param apply_comment 认领订单备注信息
        :param apply_photo 认领订单上传的图片地址
        :param gua_id 认领订单对应的呱号
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/apply_match_detail")
        body = {
            "order_id": order_id,
            "apply_info": {
                "ghs_info": ghs_info ,
                "apply_comment": apply_comment,
                "apply_photo": apply_photo,
                "gua_id": gua_id
            }
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_current_schedule_period(self):
        """
        查看规划师排班表tab,默认请求当前英语期数的规划师排班信息
        :param
        :return:
        {
        "rc": 0,
        "data": {
        "english": 84,
        "math": ["210301", "210308", "210315", "210322"]
        }
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_current_schedule_period")
        body = {

        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_ghs_home_rank_list(self,rank_type,rank_dimension,period,update_period):
        """
        规划师首页，排行榜信息
        :param rank_type  arpu，rebuy_money，day_check_rate
        :param rank_dimension 含义不明
        :param update_period  默认True
        :param period 期次
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_home_rank_list")
        body = {
                "rank_type": rank_type,
                "rank_dimension": rank_dimension,
                "limit": 10,
                "period": period,
                "update_period": update_period
            }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_ghs_home_pk_list(self,select_date,show_pk_result):
        """
        规划师首页，小组PK榜
        :param select_date PK日期
        :param show_pk_result 展示Pk结果 默认True
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_home_pk_list")
        body = {
            "select_date": select_date,
            "show_pk_result": show_pk_result
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_count_crm_todo_tasks(self, group, email):
        """
         待办任务数量计算 根据组和规划师邮箱
        :param group  小组
        :param email  规划师邮箱
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/count_crm_todo_tasks")
        body = {
            "count_dict": {
                "group": group,
                "email": email
            }
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_pk_rival_options(self, start_time, end_time):
        """
          获取pk对象可选项 时间范围
        :param start_time
        :param end_time
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_pk_rival_options")
        body = {
            "start_time": start_time,
            "end_time": end_time
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_remove_dept_from_pk_round(self, pk_uuid, dept_uuid):
        """
          从当前pk小组局移除pk小组
        :param pk_uuid
        :param dept_uuid
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/remove_dept_from_pk_round")
        body = {
            "pk_uuid": pk_uuid,
            "dept_uuid": dept_uuid
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_all_strategy(self, status, search_from=0, search_size=25):
        """
         参数设置-流量分配-查询所有策略
        :param status  状态默认空
        :param search_from  默认0
        :param search_size  规划师邮箱
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_all_strategy")
        body = {
            "status": status,
            "search_from": search_from,
            "search_size": search_size
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_all_special_definitio(self):
        """
         参数设置-流量设置- 获取所有策略定义
        :param
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_all_special_definitio")
        body = {

        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_edit_strategy(self, strategy_definition_uid, strategy_name, start_datestr,end_datestr,wechat_dict,strategy_uid):
        """
         参数设置-流量分配-编辑流量策略
        :param strategy_definition_uid  策略展示id
        :param strategy_name  策略名称
        :param start_datestr   end_datestr  测试开始和结束时间
        :param wechat_dict 微信号类型 json体
        :param strategy_uid 意义不明
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/edit_strategy")
        body = {
            "strategy_definition_uid": strategy_definition_uid,
            "strategy_name": strategy_name,
            "start_datestr": start_datestr,
            "end_datestr": end_datestr,
            "wechat_dict": wechat_dict,
            "strategy_uid": strategy_uid
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_end_strategy_by_uuid(self, strategy_uid):
        """
         参数设置-流量分配-结束流量策略
        :param strategy_uid
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/end_strategy_by_uuid")
        body = {
            "strategy_uid": strategy_uid
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_check_strategy(self, strategy_uid, start_date_str, end_date_str,ghs_wechat_type,week_type,search_from=0,search_size=25):
        """
         参数设置-流量分配-查看某个流量监控策略
        :param strategy_uid  操作者id
        :param start_date_str  end_date_str  开始结束时间
        :param ghs_wechat_type  规划师邮箱
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/check_strategy")
        body = {
            "strategy_uid": strategy_uid,
            "start_date_str": start_date_str,
            "end_date_str": end_date_str,
            "ghs_wechat_type": ghs_wechat_type,
            "week_type": week_type,
            "search_from": search_from,
            "search_size": search_size
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_create_one_strategy(self, strategy_definition_uid, strategy_name, start_datestr,end_datestr, wechat_dict):
        """
         参数设置-流量分配-创建一个策略
        :param strategy_definition_uid  策略创建者id
        :param strategy_name  策略名称
        :param start_datestr   end_datestr 策略开始和结束时间
        :param wechat_dict
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/create_one_strategy")
        body = {
            "strategy_definition_uid": strategy_definition_uid,
            "strategy_name": strategy_name,
            "start_datestr": start_datestr,
            "end_datestr": end_datestr,
            "wechat_dict": wechat_dict
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_update_ghs_rebuy_money_goal(self, period, aim_rebuy_money, goal_type, ghs_info):
        """
         规划师首页，看板，排行榜，更新绩效金额，账号 [oyingyupaiban4@jiliguala.com]有权限
        :param period 期次
        :param aim_rebuy_money 目标金额
        :param goal_type
        :param ghs_info
        {
                "group": "CWH06",
                "email": "",
                "dept_name": "CWH06组",
                "dept_uuid": "01ad93ea33794438ae729fffbd771033"
            }
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/update_ghs_rebuy_money_goal")
        body = {
            "period": period,
            "aim_rebuy_money": aim_rebuy_money,
            "goal_type": goal_type,
            "ghs_info": ghs_info
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def get_arpu_rank_list(self,dimension,wechat_type,period):
        '''
        @tion
        首页-实时概况-arpu数据
        period:期次
        dimension：维度
        wechat_type：微信号类型
        '''
        #api_url="/api_planner_get_arpu_rank_list"
        api_url = parse.urljoin(self.host, f"{self.root}/get_arpu_rank_list")
        body = {
            "dimension": dimension,
            "wechat_type": wechat_type,
            "period": period
        }

        return send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)

    def get_basic_detail(self,id_or_phone):
        '''
        @tion
        guaid：呱号
        获取学员的基础信息
        '''
        #api_url="/api/planner/get_basic_detail"
        api_url = parse.urljoin(self.host, f"{self.root}/get_basic_detail")
        body={
            "id_or_phone":id_or_phone,
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def get_check_detail(self,id_or_phone):
        '''
        @tion
        id_or_phone:用户呱号，获取用户的打卡信息
        '''
        #api_url = "/api/planner/get_check_detail"
        api_url = parse.urljoin(self.host, f"{self.root}/get_check_detail")
        body={
            "id_or_phone":id_or_phone,
        }
        return send_api_request(url=self.host +api_url,paramType='json',paramData=body,method='post',cookies=self.cookies)

    def get_coupon_detail(self,id_or_phone):
        '''
        @tion
        id_or_phone:用户呱号，获取用户优惠卷信息
        '''
        #api_url='/api/planner/get_coupon_detail'
        api_url = parse.urljoin(self.host, f"{self.root}/get_coupon_detail")
        body={
            "id_or_phone":id_or_phone,
        }
        return send_api_request(url=api_url,paramData=body,paramType='json',method='post',cookies=self.cookies)

    def get_ghs_detail(self,id_or_phone):
        '''
        @tion
        id_or_phone:用户呱号，获取用户绑定的规划师信息
        '''
        #api_url='/api/planner/get_ghs_detail'
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_detail")
        print(api_url)
        body={
            "id_or_phone":id_or_phone,
        }
        return send_api_request(url=api_url,paramData=body,paramType='json',method='post',cookies=self.cookies)

    def get_ghs_rebuy_order_detail_v2(self,group,email,period,subject_type,sort_by=[],time={},ghs_wechat_type='',dimension=1,*kwargs):
        '''
        @tion
        获取绩效表-复购明细表的数据
        ghs_info：规划师信息、period：期次、time：时间、ghs_wechat_type：微信号类型、
        sort_by：排序情况、group:规划师小组、email：规划师邮箱
        '''
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_rebuy_order_detail_v2")
        body={
            "ghs_infos": {
                "ghs_info": {
                    "group": group,
                    "email": email
                },
                "dimension": dimension,
                "period": period,
                "subject_type":subject_type,
                "time": time,
                "ghs_wechat_type":ghs_wechat_type,
            },
            "sort_by": sort_by
        }
        return send_api_request(url=api_url,paramData=body,paramType='json',method='post',cookies=self.cookies)

    def get_ghs_performance_v2(self,group,email,period,dimension,subject_type,*kwargs):
        '''
        @tion
        获取规划师的绩效总表的信息
        ghs_infos：规划师的数据信息
        sort_by：排序情况
        '''
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_performance_v2")
        body={ "ghs_infos":{
            "ghs_info":{
                "group":group,
                "email":email,
            },
            "period":period,
            "dimension":dimension,
            "subject_type":subject_type
        }
        }
        return send_api_request(url=api_url,paramData=body,paramType='json',method='post',cookies=self.cookies)

    def get_ghs_finish_lesson_detail(self, group,email,period,subject_type,sort_by=[],dimension=1,):
        '''
        @tion
        ghs_infos：规划师绑定用户的完课情况统计
        sort_by：排序情况
        '''
        body={
            'ghs_infos':{
                "ghs_info":{
                    "group":group,
                    "email":email,
                },
                "dimension": dimension,
                "period":period,
                "subject_type":subject_type,
            },
            'sort_by':sort_by,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_finish_lesson_detail")
        return send_api_request(url=api_url,paramType='json',paramData=body,method='post',cookies=self.cookies)

    def export_activity_students(self,group,email,stu_info,term,is_enter_screenshot,creenshot_review_status,is_enter_regiment,is_start_regiment,subject_type='english'):
        '''
        @tion
        活动明细表的导出
        subject_type：科目、group：小组、email：邮箱、stu_info：学员呱号或者手机号、term：期次（思维年-月-日）
        is_enter_screenshot：本周进入截图上传活动、creenshot_review_status：审核状态（审核成功、审核失败、审核中、未上传、）、
        is_enter_regiment：是否今日拼团（是\否）、 is_start_regiment：是否发起拼团（是\否）
        '''
        #api_url="/api/planner/export_activity_students"
        body={
            "subject_type":subject_type,
            "group":group,
            "email":email,
            "stu_info":stu_info,
            "term":term,
            "is_enter_screenshot":is_enter_screenshot,
            "creenshot_review_status":creenshot_review_status,
            "is_enter_regiment":is_enter_regiment,
            "is_start_regiment":is_start_regiment,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/export_activity_students")
        return send_api_request(url=api_url,paramData=body,paramType='json',method='post',cookies=self.cookies)

    def get_activity_stduents(self,search_size,search_from,change_page,subject_type,group,email,stu_info,
                              is_enter_screenshot,creenshot_review_status,is_enter_regiment,is_start_regiment):
        '''
        @ tion
        查询活动明细表用户数据
        search_size:每页多少条数据、   search_from：截止此前有多少条数据、  change_page：false，
        subject_type：科目     group：规划师小组、  email：规划师邮箱  、   stu_info：用户呱号、手机号、term：期次（思维：年-月-日）
        is_enter_screenshot：本周进入截图上传活动、creenshot_review_status：审核状态（审核成功、审核失败、审核中、未上传、）、
        is_enter_regiment：是否今日拼团（是\否）、 is_start_regiment：是否发起拼团（是\否）
        '''
        #api_url="/api/planner/get_activity_stduents"
        body={
            "search_size":search_size,
            "search_from":search_from,
            "change_page":change_page,
            "subject_type":subject_type,
            "group":group,
            "email":email,
            "stu_info":stu_info,
            "is_enter_screenshot":is_enter_screenshot,
            "creenshot_review_status":creenshot_review_status,
            "is_enter_regiment":is_enter_regiment,
            "is_start_regiment":is_start_regiment,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_activity_stduents")
        return send_api_request(url=api_url,paramType='json',paramData=body,method='post',cookies=self.cookies)

    def change_user_ghs(self,user_id_dict,ghs_id_dict,subject_type):
        '''
        @ tion
        学员查询页，移交用户
        user_id_dict:json格式，{'微信号类型':[参1，参2...]}
        ghs_id_dict:json格式，{"移交后规划师微信号类型"："移交后规划师id"}
        subject_type：科目
        '''
        #api_url='/api/planner/change_user_ghs'
        body={
            "user_id_dict":user_id_dict,
            "ghs_id_dict":ghs_id_dict,
            "subject_type":subject_type,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/change_user_gh")
        return send_api_request(url=api_url,paramData=body,paramType='json',method='post',cookies=self.cookies)

    def get_ghs_home_rebuy_card(self,period):
        '''
        @ tion
        首页-看版-查询复购金额
        period:要查询的期次
        '''
        #api_url='/api/planner/get_ghs_home_rebuy_card'
        body={
            "period":period,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_home_rebuy_card")
        return send_api_request(url=api_url,paramType='json',paramData=body,method='post',cookies=self.cookies)

    def get_ghs_home_finish_lesson_card(self,period):
        '''
        @tion
        首页-看版-查询完课人数+完课率
        period:期次
        '''
        #api_url='/api/planner/get_ghs_home_finish_lesson_card'
        body={
            "period":period,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_ghs_home_finish_lesson_card")
        return send_api_request(url=api_url,paramData=body,paramType='json',method='post',cookies=self.cookies)

    def update_team_pk_goal(self,start_time,end_time):
        '''
        @tion
        首页-小组pk，设置pk目标
        start_time:pk开始时间
        end_time：pk结束时间
        pk_rivals：竞争对手[{'dept_uuid组的uid'：'xxx','dept_name组名'：'xx'}，
                          {'dept_uuid组的uid'：'xxx'，'dept_name组名'：'xx'}]
        '''
        #api_url='/api/planner/update_team_pk_goal'
        body={
            "start_time":start_time,
            "end_time":end_time,
        }
        api_url=parse.urljoin(self.host, f"{self.root}/update_team_pk_goal")
        return send_api_request(url=api_url,paramType='json',paramData=body,method='post',cookies=self.cookies)

    def get_point_detail(self, id_or_phone):
        '''
        "id_or_phone":手机号
        '''
        body={
            "id_or_phone":id_or_phone,
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_point_detail")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)


if __name__ == '__main__':
    from business.Crm.ApiAccount.userProperty import UserProperty

    # from utils.middleware import file_path
    dm = Domains()
    config = dm.set_env_path('dev')
    dm.set_domain(config['crm_number_url'])
    user = UserProperty(email_address=config.get('xcrm').get('email_address'), pwd=config.get('xcrm').get('pwd'))
    print(user.cookies)
    aper = ApiPlanner(cookies=user.cookies)
    print(aper.api_get_valid_ghs_list())
    # crm_share.api_get_student_comments(uid=user.uid, own=)
