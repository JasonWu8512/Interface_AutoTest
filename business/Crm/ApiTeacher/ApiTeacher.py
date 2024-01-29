# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/24 6:08 下午
@Author  : Demon
@File    : ApiTeacher.py
"""

from business.Qiniuyun.ApiQiniuyun import ApiQiniuyun
import os
from urllib.parse import urljoin
from config.env.domains import Domains
from urllib import parse
from utils.requests.apiRequests import send_api_request

class ApiTeacher(object):
    def __init__(self, cookies):
        # 请求头文件
        self.host = Domains.domain
        self.leads = Domains.config.get('leadsbind_url')
        self.cookies = cookies
        self.root = '/api/teacher'

    def api_get_home_main_data(self, kpi_term, subject_type="english"):
        """
        查询班主任首页数据
        :param subject_type 学科类型
        :param kpi_term 日期 格式：20210222
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_home_main_data")
        body = {
            "subject_type": subject_type,
            "kpi_term": kpi_term
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_change_wechat_code(self, file_path):
        """更改 规划师/班主任 账户对应的微信二维码
        :return 返回更换后七牛云路径
        """
        api_qiniu = ApiQiniuyun()
        return api_qiniu.one_key_upload(project_url_path='/api/youzan/api/access/token', file_path=file_path)

    def get_change_wechat_code_url(self, file_path):
        """更改 规划师/班主任 账户对应的微信二维码,并获取更新后的完整路径
        :return
        """
        resp = self.api_change_wechat_code(file_path=file_path)
        return urljoin(resp.get('prefix'), resp.get('key'))

    def api_update_cr_wechat_account(self, email_address, cr_wechat_reference_id, update_info):
        """更新班主任id 账户信息
        @update_info: {
                "customers_limit_uuid": "e25de408371f49e5a694d50580a5b896",
                "cr_wechat_type": "A",
                "cr_wechat_weight": 100,
                "cr_wechat_nick": "户口",
                "cr_wechat_channel": "enterprise_wechat",
                "cr_wechat_comment": "12",
                "cr_wechat_account": "企业微信-T1003",
                "cr_wechat_qrcode": "https://qiniucdn.jiliguala.com/dev/upload/68526436ab6f467f892f27569dacf933_20201015061748.jpeg",
                "cr_wechat_in_schedule": 0
            }
        @return
        """
        api_url = urljoin(self.host, f'{self.root}/update_cr_wechat_account')
        body = {
            "email_address": email_address,
            "update_info": update_info,
            "cr_wechat_reference_id": cr_wechat_reference_id
        }
        return send_api_request(method='post', url=api_url, paramData=body, paramType='json', cookies=self.cookies)

    def api_get_cr_basic_detail(self, id_or_phone):
        """
         学员查询获取9.9信息
        :param id_or_phone 搜索条件
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_basic_detail")
        body = {
            "id_or_phone": id_or_phone,
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_add_cr_link_tool(self, tool_name, tool_link,tool_icon,tool_order,tool_comment,tool_dimension):
        """
        新增运营小工具
        :param tool_name  工具名称
        :param tool_link  点击小工具跳转的链接
        :param tool_icon  小工具iocn
        :param tool_order  小工具排序
        :param tool_comment  小工具的备注信息
        :param tool_dimension 小工具所属分组
        :return:{
        "rc": 0,
        "data": null
        }
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/add_cr_link_tool")
        body = {
            "tool_name": tool_name,
            "tool_link": tool_link,
            "tool_icon": tool_icon,
            "tool_order": tool_order,
            "tool_comment": tool_comment,
            "tool_dimension": tool_dimension
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_cr_link_tools(self):
        """
        获取运营小工具
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_link_tools")
        body = {

        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_update_cr_link_tool(self, tool_uuid, update_dict):
        """
        更新小工具
        :param tool_uuid  小工具uuid
        :param update_dict
         {
                "tool_name": "测试创建小工具",
                "tool_link": "www.bilibili.com",
                "tool_icon": "#crm-icon-workorder",
                "tool_order": 1,
                "tool_comment": "123",
                "tool_dimension": "group_member"
            }
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/update_cr_link_tool")
        body = {
            "tool_uuid": tool_uuid,
            "update_dict": update_dict
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp



    def api_search_order(self, user_info=None, order_id=None,order_type="ALL"):
        """
        根据用户信息，订单号，渠道等信息查询订单，参数可以为空返回所有订单
        :param user_info  学员的呱号or手机号 可以为空
        :param order_id  订单编号 可以为空
        :param order_type app，有赞，呱呱阅读 默认为ALL
        :return:
        {
            "rc": 0,
            "data": {
                "result": {
                    "YouZan": [],
                    "App": [],
                    "Ggr": []
                },
                "total_count": 0
            }
        }
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_order")
        body = {
            "search_info": {
                "user_info": user_info,
                "order_id": order_id
            },
            "order_type": order_type
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_search_app_order(self, infos, change_page=False, search_from=0, search_size=5):
        """
        根据搜索条件，查询站内绩效订单
        :param infos  搜索条件json
        {
                "kpi_cr_email": "yuki_li@jiliguala.com",
                "kpi_dept_uuid": "a6dfd952d8f5433581e2f08838cc97f5",
                "stu_info": "",
                "term": ["20210315", "20210405"],
                "order_id": "",
                "order_date_range": ["2021-03-01", "2021-03-10"],
                "order_status": "",
                "subject_type": "english"
            },
        :param change_page  是否为非第一页，第一页 false,非第一页true
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_app_order")
        body = {
            "infos": infos,
            "change_page": change_page,
            "search_from": search_from,
            "search_size": search_size
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_cr_order_adoptions(self, info, change_page=False, sort="desc", search_from=0, search_size=25):
        """
        根据搜索选项，查询认领订单
        :param cr_info  班主任信息
        :param subject_type  学科 english(传空默认英语)，math
        :param gua_id  呱号
        :param order_id  订单号
        :param adoption_status  绩效状态
        :param date_range  申诉日期
        :param change_page  字段意义不明
        :param sort  排序 "desc"
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_order_adoptions")
        body = {
            "info": info,
            "change_page": change_page,
            "search_from": search_from,
            "search_size": search_size,
            "sort": sort
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_create_cr_order_adoption(self, order_id, gua_id, order_pay_time, platform="其他", claim_comment="测试认领订单",
                                     is_external_order=1, subject_type="english",redeem_code="",
                                     evidences=["https://qiniucdn.jiliguala.com/crm/dev/009b0f90-bd1f-11eb-a7f1-77211949c903.jpg"]):
        """
        创建站内，站外订单的认领申请
        :param order_id  订单号
        :param platform  订单来源
        :param gua_id  购买呱号
        :param redeem_code  学员的UID
        :param claim_comment  认领备注信息
        :param is_external_order  站内0，站外1
        :param "order_pay_time": "2021-03-09 00:00:00"  购买时间
        :param evidences  上传图片的七牛地址，不用每次测试上传，直接写死
        :param subject_type  english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/create_cr_order_adoption")
        body = {
            "order_id": order_id,
            "platform": platform,
            "gua_id": gua_id,
            "redeem_code": redeem_code,
            "claim_comment": claim_comment,
            "is_external_order": is_external_order,
            "evidences": evidences,
            "order_pay_time": order_pay_time,
            "subject_type": subject_type
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_audit_cr_order_adoption(self, adoption_uuid, audit_dict):
        """
         修改/审核订单认领申请
        :param adoption_uuid  认领记录的id
        :param audit_dict  认领订单的各字段信息
        {
                "order_id": "H27432",
                "approval": true, 是否纳入绩效
                "gua_id": "1479551",
                "subject_type": "english",
                "adoption_type": "ELSE",
                "amount_cent": 10000,
                "audit_comment": "懂",
                "order_pay_time": "2021-02-25 17:27:27"
            }
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/audit_cr_order_adoption")
        body = {
            "adoption_uuid": adoption_uuid,
            "audit_dict": audit_dict
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_search_class_student_by_guaid(self, guaid, subject_type):
        """
         修改/审批订单认领时，获取该订单下呱号的班级信息
        :param guaid  学员的呱号
        :param subject_type  english，math
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/search_class_student_by_guaid")
        body = {
            "subject_type": subject_type,
            "guaid": guaid
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_update_cr_setting(self, email_address, cr_schedule_id,cr_status_id):
        """
         修改班主任状态和班次
        :param email_address  学员的呱号
        :param cr_schedule_id 班次
        :param cr_status_id 状态
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/update_cr_setting")
        body = {
            "email_address": email_address,
            "update_info": {
                "cr_schedule_id": cr_schedule_id,
                "cr_status_id": cr_status_id
            }
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_teacher_id_wechat_list_v2(self, search_info, change_page=False, sort_by=[], search_from=0, search_size=10):
        """
        查询班主任信息
        :param search_info:
        :param change_page:
        :param sort_by:
        :param search_from:
        :param search_size:
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_teacher_id_wechat_list_v2")
        body = {
            "search_info": search_info,
            "sort_by": sort_by,
            "change_page": change_page,
            "search_from": search_from,
            "search_size": search_size
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_add_cr_wechat_account(self, email_address, wechat_info):
        """
        新增班主任ID
        :param email_address  班主任邮箱
        :param wechat_info 微信号信息
        "wechat_info": {
                "customers_limit_uuid": "07d61e04f98a4495a5090bd3c97c52f4",
                "cr_wechat_type": "B",
                "cr_wechat_weight": 100,
                "cr_wechat_nick": "测试",
                "cr_wechat_channel": "enterprise_wechat",
                "cr_wechat_comment": "测试",
                "cr_wechat_account": "",
                "cr_wechat_qrcode": "https://qiniucdn.jiliguala.com/dev/upload/0eb7972057b64e4c8fa6ea78bae960f5_20210310051011.jpeg",
                "cr_wechat_in_schedule": 1
            }
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/add_cr_wechat_account")
        body = {
            "email_address": email_address,
            "wechat_info": wechat_info
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_batch_update_cr_wechats_weight_or_in_schedule(self, update_type, update_value,cr_wechat_reference_ids):
        """
        修改班主任ID
        :param update_type  修改内容，权重，排班
        :param update_value 修改的值
        :param  cr_wechat_reference_ids 班主任ID list
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/batch_update_cr_wechats_weight_or_in_schedule")
        body = {
            "update_type": update_type,
            "update_value": update_value,
            "cr_wechat_reference_ids": cr_wechat_reference_ids
        }
        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_teacher_email_list(self, subject_type="all"):
        """
        获取老师邮箱列表
        :param subject_type  默认为all
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_teacher_email_list")
        body = {
            "subject_type": subject_type
        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_cr_enum_types(self):
        """
        获取班主任id管理页相关的枚举类型
        :return:
        by:Grace
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_enum_types")
        body = {

        }

        resp = send_api_request(url=api_url, paramType='json', paramData=body, method="post",
                                cookies=self.cookies)
        return resp

    def api_get_students(self, student_infos, change_page=False, search_from=0, search_size=25):
        """
        获取学员信息列表
        :param student_infos: 学员信息
        {"student_infos":
             {"kpi_cr_email": "",
              "kpi_dept_uuid": "",
              "stu_info": "",
              "kpi_term": [],
              "order_id": "",
              "ty_lesson_finish_cnt": [],
              "attendance_num_list": [],
              "is_in_wechat_group": null,
              "is_real_add_teacher": null,
              "is_valid_receiver": null,
              "has_recommender": null,
              "custom_label": "",
              "has_kpi_amount": null,
              "subject_type": "english",
              "order_date_range": [],
              "student_tab": "all",
              "if_fc": null,
              "kpi_cr_email_type": "",
              "kpi_dept_uuid_type": "",
              "ty_lesson_finish_cnt_type": ""
              }
        :param change_page: 是否第一页
        :param search_from: 起始
        :param search_size: 条数
        :return:
        """
        body = {
            "student_infos": student_infos,
            "change_page": change_page,
            "search_from": search_from,
            "search_size": search_size
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_students")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_real_add_teacher(self, identifiers, match_method="guaid", subject_type="english"):
        """
        反加好友
        :param identifiers: 加好友的学员 [""]
        :param match_method: 匹配方式 guaid/tel_number
        :param subject_type: 学科
        :return: matched/unmatched
        """
        body = {
            "identifiers": identifiers,
            "match_method": match_method,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_real_add_teacher")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_attendance_rankings(self, kpi_cr_email, kpi_term, attendance_count=1, subject_type="english"):
        """
        打卡榜单-查询真学员接口
        :param kpi_cr_email: 班主任邮箱
        :param kpi_term: 期次
        :param attendance_count: 打卡次数(>=)
        :param subject_type: 学科
        :return:
        """
        body = {
            "kpi_cr_email": kpi_cr_email,
            "kpi_term": kpi_term,
            "attendance_count": attendance_count,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_attendance_rankings")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_lesson_repeat_times_detail(self, user_id, subject_type="english"):
        """
        获取课程完成累计次数详情明细
        :param user_id:
        :param subject_type:
        :return:
        """
        body = {
            "user_id": user_id,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_lesson_repeat_times_detail")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_all_schedule_term_list(self, future_term_count=0, is_current_transfer=True):
        """
        获取所有可选的学员期次列表
        :param future_term_count: 获取未来期次的数量
        :param is_current_transfer: current是否返回当前转化期 False返回当前最新期次
        :return:
        """
        body = {
            "future_term_count": future_term_count,
            "is_current_transfer": is_current_transfer
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_all_schedule_term_list")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_optional_kpi_cr_email(self, subject_type="english"):
        """
        获取绩效邮箱
        :param subject_type:
        :return:
        """
        body = {
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_optional_kpi_cr_email")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_optional_kpi_dept(self, subject_type="english"):
        """
        获取绩效组别（小组）
        :param subject_type:
        :return:
        """
        body = {
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_optional_kpi_dept")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_all_class_teacher_dept_tree(self, subject_type="english"):
        """
        获取班主任组织架构（区域-大区-小组）
        :param subject_type:
        :return:
        """
        body = {
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_all_class_teacher_dept_tree")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_cr_kpi_list(self, info, sort_by=[]):
        """
        获取绩效总表
        :param info: {"subject_type":"english","term":["20210308"],"dimension":"cr_id"}
        :param sort_by:
        :return:
        """
        body = {
            "info": info,
            "sort_by": sort_by
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_kpi_list")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_realtime_kpi_list(self, info={"subject_type": "english", "dimension": "cr_id"}, sort_by=[]):
        """
        获取实时绩效表
        :param info: {"subject_type":"english","dimension":"cr_id"}
        :param sort_by:
        :return:
        """
        body = {
            "info": info,
            "sort_by": sort_by
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_realtime_kpi_list")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_cr_home_pk_list(self, kpi_term, subject_type="english"):
        """
        获取小组PK榜
        :param kpi_term:
        :param subject_type:
        :return:
        """
        body = {
            "kpi_term": kpi_term,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_home_pk_list")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_team_pk_goal(self, pk_type, kpi_term, pk_dept_uuids, subject_type="english"):
        """
        新增小组PK
        :param pk_type: arpu/kpi_amount_avg
        :param kpi_term:
        :param pk_dept_uuids: []
        :param subject_type:
        :return:
        """
        body = {
            "pk_type": pk_type,
            "kpi_term": kpi_term,
            "pk_dept_uuids": pk_dept_uuids,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_team_pk_goal")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_remove_dept_from_pk_round(self, dept_uuid, pk_uuid):
        """
        移除小组PK
        :param dept_uuid:
        :param pk_uuid:
        :return:
        """
        body = {
            "dept_uuid": dept_uuid,
            "pk_uuid": pk_uuid
        }
        api_url = parse.urljoin(self.host, f"{self.root}/remove_dept_from_pk_round")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_cr_hall_of_fame(self):
        """
        获取名人堂列表
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_hall_of_fame")
        return send_api_request(url=api_url, method="post", cookies=self.cookies)

    def api_create_cr_hall_of_fame_collection(self, title, sort_position, orientation="PORTRAIT", subject_type="english"):
        """
        新增名人堂模块
        :param title:
        :param orientation: PORTRAIT/LANDSCAPE 竖版/横版
        :param sort_position: 位置
        :param subject_type:
        :return:
        """
        body = {
            "title": title,
            "orientation": orientation,
            "sort_position": sort_position,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/create_cr_hall_of_fame_collection")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_parse_batch_add_cr_wechats(self, file_path):
        """
         班主任批量增加ID上传模版
        :param file_path 维护在static/下的静态文件绝对路径
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/parse_batch_add_cr_wechats")
        payload = {}
        files = {'file': (file_path.split(r'/')[-1], open(file_path, 'rb'), 'text/csv')}

        return send_api_request(url=api_url, paramType="file", files=files, method="post", data=payload, cookies=self.cookies)


    def api_create_cr_hall_of_fame_content(self, article, collection_uuid, media_url, sort_position):
        """
        新增名人堂内容
        :param article: 内容
        :param collection_uuid: 模块id
        :param media_url: 图片链接
        :param sort_position: 位置
        :return:
        """
        body = {
            "article": article,
            "collection_uuid": collection_uuid,
            "media_url": media_url,
            "sort_position": sort_position
        }
        api_url = parse.urljoin(self.host, f"{self.root}/create_cr_hall_of_fame_content")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_cr_hall_of_fame_collection(self, updated_collections):
        """
        更新名人堂模块（标题/排序）
        :param updated_collections: [{"collection_uuid","title"/"sort_position"}] 排序需传参所有模块
        :return:
        """
        body = {
            "updated_collections": updated_collections
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_cr_hall_of_fame_collection")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_cr_hall_of_fame_content(self, updated_contents):
        """
        更新名人堂内容（文字/图片/排序）
        :param updated_contents: [{"content_uuid","sort_position"/"article","media_url"}]
        :return:
        """
        body = {
            "updated_contents": updated_contents
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_cr_hall_of_fame_content")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_auto_generate_cr_schedule_v2(self, schedule_date_list, subject_type="english"):
        """
        一键排班
        :param schedule_date_list: 排班的日期 []
        :param subject_type:
        :return:
        """
        body = {
            "schedule_date_list": schedule_date_list,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/auto_generate_cr_schedule_v2")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_cr_schedule_v2(self, schedule_date, schedule_id_list, wechat_type, subject_type="english"):
        """
        修改排班
        :param schedule_date:
        :param schedule_id_list: []
        :param wechat_type: A/B/C
        :param subject_type:
        :return:
        """
        body = {
            "schedule_date": schedule_date,
            "schedule_id_list": schedule_id_list,
            "wechat_type": wechat_type,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_cr_schedule_v2")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_cr_schedule_v2(self, schedule_date, wechat_type, subject_type="english"):
        """
        获取排班表
        :param schedule_date:
        :param wechat_type:
        :param subject_type:
        :return:
        """
        body = {
            "schedule_date": schedule_date,
            "wechat_type": wechat_type,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_schedule_v2")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_realtime_student_traffic_monitor(self, info, sort_by=[]):
        """
        获取实时流量监控表
        :param info: {"cr_info":{},"channel":"ALL","subject_type":"english"} channel:ALL/A/B/C/S/EXTRA
        :param sort_by: [["total_student_count","desc"]]
        :return:
        """
        body = {
            "info": info,
            "sort_by": sort_by
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_realtime_student_traffic_monitor")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_student_traffic_monitor(self, infos, sort_by=[]):
        """
        获取流量监控表
        :param infos: {"cr_info":{},"channel":[],"order_date_range":[],"term":["20210405"]}
        :param sort_by: [["total_student_count","desc"]]
        :return:
        """
        body = {
            "infos": infos,
            "sort_by": sort_by
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_student_traffic_monitor")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_water_army_list(self, cr_account_uuid):
        """
        获取选定班主任的水军
        :param cr_account_uuid: 班主任的用户ID
        :return:
        """
        body = {
            "cr_account_uuid": cr_account_uuid
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_water_army_list")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_add_water_army(self, cr_account_uuid, wechat_nick, baby_name):
        """
        添加水军
        :param cr_account_uuid:
        :param wechat_nick:
        :param baby_name:
        :return: water_army_uuid
        """
        body = {
            "cr_account_uuid": cr_account_uuid,
            "wechat_nick": wechat_nick,
            "baby_name": baby_name
        }
        api_url = parse.urljoin(self.host, f"{self.root}/add_water_army")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_remove_water_army_by_uuid(self, water_army_uuid):
        """
        删除水军
        :param water_army_uuid:
        :return:
        """
        body = {
            "water_army_uuid": water_army_uuid
        }
        api_url = parse.urljoin(self.host, f"{self.root}/remove_water_army_by_uuid")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_student_kpi_owner(self, guaids, update_dict, subject_type="english"):
        """
        更新绩效归属
        :param guaids: []
        :param update_dict:
        :param subject_type: {"kpi_term": "", "kpi_cr": [{"kpi_cr_wechat_ref_id":"" ,"kpi_dept_uuid": ""},{},{}]}
        :return: error_list
        """
        body = {
            "guaids": guaids,
            "update_dict": update_dict,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_student_kpi_owner")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_delete_cr_hall_of_fame(self, **kwargs):
        """
        删除名人堂模块/内容
        :param kwargs: collection_uuid/content_uuid
        :return:
        """
        body = kwargs
        api_url = parse.urljoin(self.host, f"{self.root}/delete_cr_hall_of_fame")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_cr_wechat_id_list(self, subject_type="english"):
        """
        获取TID列表（更新绩效归属）
        :param subject_type:
        :return:
        """
        body = {
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_wechat_id_list")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_all_class_teacher_depts(self, subject_type="english"):
        """
        获取组别列表（更新绩效归属）
        :param subject_type:
        :return:
        """
        body = {
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, "/api/account/get_all_class_teacher_depts")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_student_service_term_days(self, guaids, service_term_days, subject_type="english"):
        """
        修改运营天数
        :param guaids: []
        :param service_term_days: 7/14/21
        :param subject_type:
        :return:
        """
        body = {
            "guaids": guaids,
            "service_term_days": service_term_days,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_student_service_term_days")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_pk_rival_options(self, kpi_term, pk_type, subject_type="english"):
        """
        获取可参与小组PK的组别
        :param kpi_term:
        :param pk_type: arpu/kpi_amount_avg
        :param subject_type:
        :return:
        """
        body = {
            "kpi_term": kpi_term,
            "pk_type": pk_type,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_pk_rival_options")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_settings_v2(self):
        """
        获取班主任TID的参数配置
        :return:
        """
        api_url = parse.urljoin(self.host, f"{self.root}/get_settings_v2")
        return send_api_request(url=api_url, method="post", cookies=self.cookies)

    def api_leads_assign_v3(self, kwargs):
        """
        流量分配
        :param kwargs:
                "subject_type": "english/mayh",
                "uid": "",
                "oid": "",
                "opensource": "",
                "itemid": "",
                "lessonIdList": [],
                "initiator_uid": "",
                "is_initiator_paidxx": Bool,
                "bind_status": "pre/notpaid",
                "assignType": "normal/dummy/active",
                "is_combined_subject": Bool,
                "pts": time_stamp,
                "lesson_start_at_same_time": Bool,
                "marketingChannelCode": ""
        :return:
        """
        body = {
            "args": [],
            "kwargs": kwargs
        }
        api_url = parse.urljoin(self.leads, "/service-teacherbiz/leads_assign_v3")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post")

    def api_update_student_kpi_owner_v2(self, guaids, update_dict, subject_type="english"):
        """
        :param guaids: [呱号]
        :param subject_type: english/math
        :param update_dict: kpi_cr_ref_id_normal/kpi_cr_ref_id_post_term/kpi_cr_ref_id_week1/kpi_cr_ref_id_week2/kpi_term
        :return: error_list
        """
        body = {
            "guaids": guaids,
            "subject_type": subject_type,
            "update_dict": update_dict
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_student_kpi_owner_v2")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_cr_wechat_id_list_v2(self, subject_type="english"):
        """
        获取TID列表（更新绩效归属）
        :param subject_type:
        :return:
        """
        body = {
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/get_cr_wechat_id_list_v2")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_student_cr_assign(self, cr_wechat_reference_id, guaids, subject_type="english"):
        """
        修改假人分配班主任
        :param cr_wechat_reference_id: ""
        :param guaids: []
        :param subject_type:
        :return:
        """
        body = {
            "cr_wechat_reference_id": cr_wechat_reference_id,
            "guaids": guaids,
            "subject_type": subject_type
        }
        api_url = parse.urljoin(self.host, f"{self.root}/update_student_cr_assign")
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)



if __name__ == '__main__':
    from business.Crm.ApiAccount.userProperty import UserProperty
    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['crm_number_url'])
    crm_user = UserProperty(email_address=config.get('xcrm').get('email_address'), pwd=config.get('xcrm').get('pwd'))
    api_teacher = ApiTeacher(cookies=crm_user.cookies)

