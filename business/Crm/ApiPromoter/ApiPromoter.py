# -*- coding: utf-8 -*-
"""
@Time    : 2021/06/07
@Author  : Grace
@File    : conftest.py
"""
import os
from urllib.parse import urljoin
from config.env.domains import Domains
from urllib import parse
from utils.requests.apiRequests import send_api_request

class ApiPromoter(object):
    def __init__(self, cookies):
        # 请求头文件
        self.host = Domains.domain
        self.cookies = cookies
        self.root = '/api/promoter'

    '''推广人信息表接口'''
    def api_promoter_search(self,search_promoter_infos):
        """查询推广人信息"""
        api_url = parse.urljoin(self.host, f"{self.root}/search")
        body = {
                "request_body": {
                    "search_infos": search_promoter_infos,
                    "search_size": 25,
                    "search_from": 1
                }
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_promoter_all_tags(self):
        """获取配置的所有标签"""
        api_url = parse.urljoin(self.host, f"{self.root}/config/tags/all")
        body = {
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_promoter_tag_update(self,promoter_id,tags):
        """
        更新推广人标签
        "request_body": {
		"promoter_list": [{
			"promoter_id": "JLGL_FP_12472",
			"tags": ["地推", "已入群"]
		}, {
			"promoter_id": "JLGL_FP_12473",
			"tags": ["地推", "已入群"]
		}]
	}
        """
        api_url = parse.urljoin(self.host, f"{self.root}/tags/update")
        body = {
                "request_body": {
                    "promoter_list": [{
			        "promoter_id": promoter_id,
			        "tags": tags
		            }]
                }
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_promoter_state(self,promoter_id,operation):
        """
        封禁和解封推广人
        "operation": 2-解封，1-封禁
        返回参数中，promoter_active_status 2（带封禁） 5（待解禁） 3（无解禁和封禁）
        """
        api_url = parse.urljoin(self.host, f"{self.root}/update_state")
        body = {
                "request_body": {
                    "promoter_id": promoter_id,
                    "operation": operation
                }
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_promoter_sn(self,promoter_id,group_type,leader_id,sn):
        """
        推广人信息表更换组长和期次
        """
        api_url = parse.urljoin(self.host, f"{self.root}/group/update_sn")
        body = {
                "request_body": {
                    "promoter_id": promoter_id,
                    "group_type": group_type,
                    "leader_id": leader_id,
                    "sn": sn
                }
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_promoter_remark(self,promoter_id,remark):
        """
        推广人信息表更新推广人备注
        """
        api_url = parse.urljoin(self.host, f"{self.root}/update_extend")
        body = {
                "request_body": {
                    "promoter_id": promoter_id,
                    "remark": remark
                }
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_group_by_leader_id(self,leader_id):
        """
        获取组长的所有期次
        """
        api_url = parse.urljoin(self.host, f"{self.root}/group/by_leader_id")
        body = {
                "request_body": {
                    "leader_id": leader_id
                }
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    '''关系查询接口'''
    def api_promoter_relationship(self,search_promoter_relationship):
        api_url = parse.urljoin(self.host, f"{self.root}/get_relationship")
        body = {
            "search_infos": search_promoter_relationship,
            "search_size": 25,
            "search_from": 1,
            "sort_by": []
            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)



    '''推广人订单表接口'''
    def api_promoter_order_search(self,search_promoter_order):
        api_url = parse.urljoin(self.host, f"{self.root}/order/search")
        body = {
             "request_body": {
                    "search_infos": search_promoter_order,
                    "search_size": 25,
                    "search_from": 1
                },
            "sort_by": [["create_time", "desc"]]

            }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)



    '''推广人业绩表接口'''


    '''推广人组长管理'''

    def api_promoter_leader_all(self):
        """获取所有组长"""
        api_url = parse.urljoin(self.host, f"{self.root}/leader/all")
        body = {
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_promoter_leader_search(self,promoter_leader_search_infos):
        """查询组长"""
        api_url = parse.urljoin(self.host, f"{self.root}/leader/search")
        body = {
            "request_body": {
                "search_size": 25,
                "search_from": 0,
                "search_infos": promoter_leader_search_infos,
                "sort_by": []
            }
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_promoter_leader_edit(self,leader_id,wechat_type,work_time_type,wechat_qrcode_image_url,wechat_account):
        """编辑组长"""
        api_url = parse.urljoin(self.host, f"{self.root}/leader/edit")
        body = {
            "request_body": {
                "leader_id": leader_id,
                "wechat_type": wechat_type,
                "work_time_type": work_time_type,
                "wechat_qrcode_image_url": wechat_qrcode_image_url,
                "wechat_account": wechat_account
            }
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_promoter_add_queue(self,leader_id,max_member_count):
        """加入分配序列组长"""
        api_url = parse.urljoin(self.host, f"{self.root}/leader/add_queue")
        body = {
            "request_body": {
                "leader_id": leader_id,
                "max_member_count": max_member_count
            }
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_promoter_add_leader(self,add_leader_info):
        """加入分配序列组长"""
        api_url = parse.urljoin(self.host, f"{self.root}/add_leader")
        body = {
            "request_body": add_leader_info
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)


    '''推广人流量分配管理'''
    def api_get_group_flow_list(self,group_type):
        """获取分配序列"""
        api_url = parse.urljoin(self.host, f"{self.root}/get_group_flow_list")
        body = {
            "group_type": group_type
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_period_list(self,search_infos):
        """查询期次管理"""
        api_url = parse.urljoin(self.host, f"{self.root}/get_period_list")
        body = {
            "search_size": 25,
            "search_from": 1,
            "search_infos": search_infos,
            "sort_by": []
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_update_operation_date(self,group_id,started_date,end_date,leader_id):
        """更新期次"""
        api_url = parse.urljoin(self.host, f"{self.root}/update_operation_date")
        body = {
            "group_id": group_id,
            "started_date": started_date,
            "end_date": end_date,
            "leader_id": leader_id
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_group_by_group_type(self,group_type):
        """获取期次信息"""
        api_url = parse.urljoin(self.host, f"{self.root}/group/by_group_type")
        body = {
                "request_body": {
                    "group_type": group_type
                }
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_group_merge_sn(self,group_id,merge_groups_list):
        """合并期次"""
        api_url = parse.urljoin(self.host, f"{self.root}/group/merge_sn")
        body = {
                "request_body": {
                    "group_id": group_id,
                    "merge_groups": merge_groups_list
                }
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    def api_get_group_leaders(self):
        """获取每个营期的组长信息和带过的期次"""
        api_url = parse.urljoin(self.host, f"{self.root}/get_group_leaders")
        body = {
        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)

    '''推广人业绩表'''
    def api_get_promoter_achievement(self,achievement_search_info):
        """搜索推广人业绩表-人维度信息"""
        api_url = parse.urljoin(self.host, f"{self.root}/achievement/promoter/search")
        body = {
                "request_body": {
                "search_from": 1,
                "search_size": 25,
                "search_info": achievement_search_info
            }

        }
        return send_api_request(url=api_url, paramType="json", paramData=body, method="post", cookies=self.cookies)


    '''其他'''