#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/3/16 4:10 下午
# @Author : liang_li
# @Site : 
# @File : test_promotion_admin.py
# @Software: PyCharm

import pytest
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from utils.enums.businessEnums import EshopAdminEnum
from business.Trade.eshopAdmin.ApiPromotionActivity import ApiPromotionActivity
from business.Trade.eshopAdmin.ApiGroup import ApiGroup
from business.businessQuery import promotionQuery
from business.mysqlQuery import EshopQuery
from utils.format.format import dateToTimeStamp
import time
import datetime


@pytest.mark.Trade
@pytest.mark.EshopAdmin
@pytest.mark.TradeCommodity
class TestPromotionAdmin:
    """后台拼团活动管理相关用例"""
    promotionId = None

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_commodity = ApiCommodity(token=a_token)
        cls.eshop_admin_promotionActivity = ApiPromotionActivity(token=a_token)
        cls.eshop_admin_group = ApiGroup(token=a_token)
        cls.promotionQuery = promotionQuery()
        cls.EshopQuery = EshopQuery()

    @pytest.fixture(scope='class')
    def get_spu_one_commodity(self):
        """获取一个SPU商品"""
        res = self.eshop_admin_commodity.api_get_spu_list(state=1)
        spu = res['data']['content'][0]
        return spu

    @pytest.mark.parametrize("enable, autoComplete, instantShip", [('True', 'True', 'True'), ('True', 'False', 'True'),
                                                                   ('True', 'False', 'False'),
                                                                   ('False', 'False', 'True')])
    def test_create_promotion_activity(self, get_spu_one_commodity, enable, autoComplete, instantShip):
        """
        新增拼团活动（假拼团，真拼团立即开课，真拼团成团开课，活动未启用）
        """
        intro = '新增拼团自动化测试hyrz'
        # 获取SPU中包含的SXU
        spu_no = get_spu_one_commodity['commodityNo']
        spu_id = self.eshop_admin_commodity.api_get_spu_list(commodityNo=spu_no)['data']['content'][0]['id']
        spu_detail = self.eshop_admin_commodity.api_get_spu_detail(spuId=spu_id)['data']
        spu_no, sxu_list = spu_detail['commodityNo'], spu_detail['skuSpecBriefList']
        sxu_no = [sxu['commodityNo'] for sxu in sxu_list]
        item_ids = []
        for sxu in sxu_no:
            item_ids.append({'sxuNo': sxu, 'promotionPriceRmb': 800})
        # 手动构造一个SPU的payload
        pro_body = {
            'spuNo': spu_no,
            'intro': '新增拼团自动化测试hyrz',
            'startAt': dateToTimeStamp(),
            'endAt': dateToTimeStamp(day=1),
            'autoComplete': autoComplete,
            'enable': enable,
            'instantShip': instantShip,
            'groupDuration': 3600,
            'groupSize': 3,
            'itemIds': item_ids,
            'type': 'groupon'
        }
        # 调用新增拼团活动接口
        res = self.eshop_admin_promotionActivity.api_create_v2_promotion_activity(promotionActivityV2Body= pro_body)
        # 断言调用新增拼团活动接口是否成功
        assert res['code'] == 0
        # 断言新增后的拼团活动参数是否与请求的参数一致
        assert intro == res['data']['intro']
        assert enable == str(res['data']['enable'])
        assert autoComplete == str(res['data']['autoComplete'])
        assert instantShip == str(res['data']['instantShip'])

    @pytest.mark.parametrize("event_status", [None, 'pending', 'processing', 'finished'])
    @pytest.mark.parametrize("enable", [None, True, False])
    def test_promotion_list(self, event_status, enable):
        """
        测试拼团活动管理列表，不同的查询条件不同的结果
        """
        # 获取拼团活动列表
        res = self.eshop_admin_promotionActivity.api_get_v2_promotion_activities(eventStatus=event_status,
                                                                                 enable=enable)
        # 拼团活动列表包含的eventStatus活动状态
        event_status_set = set([item['eventStatus'] for item in res['data']['content']])
        # 拼团活动列表包含的enable启用状态
        enable_set = set([item['enable'] for item in res['data']['content']])
        if event_status:
            assert event_status_set in [{EshopAdminEnum.get_chinese(event_status)}, set()]
        else:
            assert event_status_set.issubset({'进行中', '未开始', '已结束'})
        if enable:
            assert enable_set in [{enable}, set()]
        else:
            assert enable_set.issubset({True, False})

    @pytest.mark.parametrize("enable", ['True', 'False'])
    def test_edit_promotion_activity(self, enable):
        """
        编辑拼团活动
        """
        # 生成四位随机字符串
        # intro_set = [chr(i) for i in range(97, 123)]
        # intro_value = "".join(random.sample(intro_set, 4))
        # 将生成的随机字符串与活动命名拼接成intro参数
        # intro = f'编辑拼团自动化测试{intro_value}'
        # 获取当前时间
        nowtime = datetime.datetime.now()
        # 将当前时间转换成毫秒级时间戳
        nowtime_stamp = int(round(time.mktime(nowtime.timetuple())*1000))
        # 当前时间+6天
        before_nowtime6 = nowtime + datetime.timedelta(days=+6)
        # 当前时间+6天后的毫秒级时间戳
        before_nowtime6_stamp = int(round(time.mktime(before_nowtime6.timetuple())*1000))
        # 编辑通过商品列表接口获取的活动id的活动信息
        res = self.eshop_admin_promotionActivity.api_get_v2_promotion_activities()
        promotion_activity_id = res['data']['content'][0]['id']
        # 调用编辑拼团活动接口
        res = self.eshop_admin_promotionActivity.api_edit_promotion_activity_detail(promotionId=promotion_activity_id,
                                                                                    enable=enable,
                                                                                    startAt=nowtime_stamp,
                                                                                    endAt=before_nowtime6_stamp)
        # 断言调用编辑拼团活动接口是否成功
        assert res['code'] == 0
        # 断言编辑后的拼团活动参数是否与请求的参数一致
        assert enable == str(res['data']['enable'])

    def test_navy_group(self):
        """
        水军开团
        """
        # 获取拼团活动列表
        activity_list = self.eshop_admin_promotionActivity.api_get_v2_promotion_activities(eventStatus='processing')
        # 定义一个全局变量
        global promotionId
        mobileList = ['17521157698', '17521157697']
        # 遍历拼团活动列表，找出真拼团活动
        for activity in activity_list['data']['content']:
            if activity['autoComplete'] is False:
                promotionId = activity['id']
                break
        # 水军开团
        navy_group = self.eshop_admin_group.api_navy_group(mobileList=mobileList, promotionId=promotionId)
        # 将成功开团的手机号输出成一个集合
        mobileList_res = set([mobileList['mobile'] for mobileList in navy_group['data']['groups']])
        # 断言调用水军开团接口是否成功
        assert navy_group['code'] == 0
        # 断言成功开团的手机号与输入的手机号是否一致
        assert mobileList_res.issubset(set(mobileList))

    def test_group_one_less(self):
        """
        开差一人团
        """
        # 获取拼团活动列表
        activity_list = self.eshop_admin_promotionActivity.api_get_v2_promotion_activities(eventStatus='processing')
        # 定义一个全局变量
        global promotionId
        mobileList = ['17521157698', '17521157697']
        # 遍历拼团活动列表，找出真拼团活动
        for activity in activity_list['data']['content']:
            if activity['autoComplete'] is False:
                promotionId = activity['id']
                break
        # 开差一人团
        group_one_less = self.eshop_admin_group.api_group_one_less(mobileList=mobileList, promotionId=promotionId)
        # 将成功开团的手机号输出成一个集合
        mobileList_res = set([mobileList['mobile'] for mobileList in group_one_less['data']['groups']])
        # 断言调用开差一人团接口是否成功
        assert group_one_less['code'] == 0
        # 断言成功开团的手机号与输入的手机号是否一致
        assert mobileList_res.issubset(set(mobileList))

    def test_promotion_activities_csv(self):
        """
        导出拼团活动列表
        """
        # 查询拼团活动列表
        promotion_activity_list = self.eshop_admin_promotionActivity.api_get_v2_promotion_activities()
        # 导出csv文件数据
        activity_csv = self.eshop_admin_promotionActivity.api_get_v2_promotion_activities_csv()
        # 断言查询的拼团活动数量与导出的拼团活动数量是否一致
        assert len(activity_csv['text'].split('\n')) == promotion_activity_list['data']['totalElements']+1


    @pytest.mark.parametrize("status", [None, 'notcompleted', 'completed', 'expired'])
    def test_get_groups(self, status):
        """
        获取拼团团列表，不同的查询条件返回不同的结果
        """
        # 获取当前时间
        nowtime = datetime.datetime.now()
        # 将当前时间转换成毫秒级时间戳
        nowtime_stamp = int(round(time.mktime(nowtime.timetuple()) * 1000))
        # 当前时间-1天
        after_nowtime1 = nowtime + datetime.timedelta(days=-1)
        # 当前时间-1天后的毫秒级时间戳
        after_nowtime1_stamp = int(round(time.mktime(after_nowtime1.timetuple()) * 1000))
        # 获取拼团列表
        groups_list = self.eshop_admin_group.api_get_groups(status=status, startAtAfter=after_nowtime1_stamp,
                                                            startAtBefore=nowtime_stamp)
        # 将当前列表包含的拼团状态status值组合成一个集合
        status_set = set([groups['status'] for groups in groups_list['data']['content']])
        if status !=None:
            # 断言调用获取拼团列表是否成功
            assert groups_list['code'] == 0
            # 断言获取到的拼团状态是否正确
            assert status_set in [{status}, set()]
        else:
            # 断言调用获取拼团列表是否成功
            assert groups_list['code'] == 0
            # 断言获取到的拼团状态是否正确
            assert status_set.issubset({'notcompleted', 'completed', 'expired'})

    def test_manual_group(self):
        """
        一键成团
        """
        # 获取拼团未成团的团列表
        group_list = self.eshop_admin_group.api_get_groups(mobile='17521157698')
        # 将团id组装成一个列表
        group_id_list = group_list['data']['content'][0]['id'].split()
        # 一键成团
        manual_group = self.eshop_admin_group.api_manual_group(groupIdList=group_id_list)
        # 断言调用一键成团接口是否成功
        assert manual_group['code'] == 0

    def test_add_one_robot(self):
        """
        手动添加一个机器人
        """
        # 获取拼团未成团的团列表
        group_list = self.eshop_admin_group.api_get_groups()
        # 将团id组装成一个列表
        group_id = group_list['data']['content'][0]['id']
        # 添加机器人
        add_one_robot = self.eshop_admin_group.api_group_add_one(groupId=group_id)
        # 断言调用添加机器人接口是否成功
        assert add_one_robot['code'] == 0

    def test_groups_csv(self):
        """
        导出拼团活动团列表
        """
        # 查询团列表
        group_list = self.eshop_admin_group.api_get_groups()
        # 导出团列表
        groups_csv = self.eshop_admin_group.api_down_groups_csv()
        # 断言查询团列表的团数量是否与导出团列表的数量一致
        assert len(groups_csv['text'].split('\n')) == group_list['data']['totalElements']+1

    def test_delete_group(self):
        """
        删除水军开团和开差一人团的团
        """
        # 获取拼团列表团id
        groups_list = self.eshop_admin_group.api_get_groups(mobile='17521157698', status=None)
        groups_list_id = list(group_id['id'] for group_id in groups_list['data']['content'])
        groups_list_b = self.eshop_admin_group.api_get_groups(mobile='17521157697', status=None)
        groups_list_id_b = list(group_id['id'] for group_id in groups_list_b['data']['content'])
        # 两个手机号的列表相加
        groups_list_id += groups_list_id_b
        # 删除团
        for group_id in groups_list_id:
            self.promotionQuery.delete_promotion_activity_group(_id=group_id)

    def test_delete_promotion_activity(self):
        """
        删除新增的活动
        """
        # 获取拼团活动列表
        activity_list = self.eshop_admin_promotionActivity.api_get_v2_promotion_activities(enable=None)
        # 删除数据库拼团活动名称为"新增拼团自动化测试hyrz"的拼团活动
        for activity_id in activity_list['data']['content']:
            if activity_id['intro'] == '新增拼团自动化测试hyrz':
                self.EshopQuery.delete_promotion_record(activity_id['id'])
