# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/30
@Author  : Grace
@File    : test_planner_info.py
接口：重构一下，新增先不写，因为没有删除的接口，只做更新和迁移吧
 /api/planner/add_ghs_wechat_account
 /api/planner/get_ghs_enum_types
 /api/planner/get_ghs_user 默认可信接口
 /api/planner/get_ghs_user_list 默认可信接口
 /api/planner/get_ghs_wechat_list
 /api/planner/update_ghs_user_status
 /api/planner/update_ghs_wechat_account
"""

import pytest
from config.env.domains import Domains, ROOT_PATH
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiShare.ApiShare import ApiShare
from business.Crm.ApiTeacher.ApiTeacher import ApiTeacher
import pytest_check
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.CrmQuery import CrmAllianceQuery
from business.CrmQuery import CrmJainaQuery
from testcase.Crm.TestPlanner import conftest
import random
import datetime

@pytest.mark.xCrm
class TestPlannerInfo(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        print(cls.config)
        cls.user = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.share = ApiShare(cls.user.cookies)
        cls.planner = ApiPlanner(cls.user.cookies)
        cls.teacher = ApiTeacher(cls.user.cookies)
        cls.query_alliance = CrmAllianceQuery()
        cls.query_jaina = CrmJainaQuery()
        '''生成一个微信号'''
        cls.wechat_msg = "crmauto" + datetime.datetime.now().strftime('%Y%m%d%H%M')
        '''随机获取一个规划师'''
        cls.planner_data = random.choice(cls.planner.api_get_ghs_user_list(subject_type='english').get('data').get('emailList'))

        '''数据库查询规划师对应的组信息'''
        cls.ghs_sql_account = cls.query_jaina.query_jaina_info(table='ghs_account_dept', time_removed=0,ghs_account_uuid=cls.planner_data['userId'])
        # '''新建一个规划师微信号供使用'''
        # cls.row = cls.planner.api_add_ghs_wechat_account(
        #     ghs_wechat_infos(cls.planner_data['emailAddress'], wechat_nick=cls.wechat_msg,
        #                      wechat=cls.wechat_msg)).get('data').get('row')

    @pytest.mark.reg
    def test_get_ghs_user_info(self):
        """
        @Author  : Grace
        1：获取规划师信息
        """
        api_data = self.planner.api_get_ghs_user(user_id=self.planner_data['userId']).get('data')
        pytest_check.equal(api_data['emailAddress'], self.planner_data['emailAddress'])
        pytest_check.equal(api_data['deptId'], self.ghs_sql_account[0]['dept_uuid'])
        pytest_check.equal(api_data['deptName'], self.ghs_sql_account[0]['dept_name'])

    @pytest.mark.skip #目前没有删除接口，所以尽量不跑添加微信号的接口
    def test_add_ghs_wechat_account(self):
        """
        @Author  : Grace
        1：规划师新增微信号
        """
        pytest_check.equal(self.row['ghs_wechat_account'],self.wechat_msg)
        pytest_check.equal(self.row['ghs_wechat_nick'], self.wechat_msg)
        pytest_check.equal(self.row['ghs_wechat_type'], 'type_a')
        row_list = self.planner.api_get_ghs_wechat_list().get('data')
        for data in row_list:
            if data['email'] == self.planner_data['emailAddress']:
                wechat_list = data['wechatList']
                pytest_check.is_in(self.wechat_msg, wechat_list['wechat'])
                break
            else:
                print('没有找到规划师邮箱')

    @pytest.mark.reg
    def test_update_ghs_wechat_account(self,ghs_wechat_infos):
        """
        @Author  : Grace
        1：更新规划师微信号
        """
        '''随机选择一个规划师微信号信息'''
        planner1 =random.choice(self.planner.api_get_ghs_wechat_list().get('data'))
        old_wechat_id=planner1['wechatList'][0]['id']
        old_wechat_nick=planner1['wechatList'][0]['wechatNick']
        old_wechat=planner1['wechatList'][0]['wechat']
        print('*****更新规划师',planner1['email'],'的微信号和微信昵称',old_wechat_id,self.wechat_msg)
        self.planner.api_update_ghs_wechat_account(
            ghs_wechat_infos(email_address=planner1['email'],wechat_nick=self.wechat_msg,wechat=self.wechat_msg,wechat_account_id=old_wechat_id))
        row_list = self.planner.api_get_ghs_wechat_list().get('data')
        for data in row_list:
            if data['email'] == planner1['email']:
                print("邮箱信息：", data['email'], planner1['email'])
                wechat_list = data['wechatList']
                self.wechat_id_list = []
                self.wechatNick_list = []
                for wechat in wechat_list:
                    print('for循环中wechat取值',wechat['wechat'],wechat['wechatNick'])
                    self.wechat_id_list.append(wechat['wechat'])
                    self.wechatNick_list.append(wechat['wechatNick'])
                print('规划师的wechat_id_list',self.wechat_id_list)
                print('规划师的wechatNick_list',self.wechatNick_list)
                pytest_check.is_in(self.wechat_msg, self.wechat_id_list)
                pytest_check.is_in(self.wechat_msg,self.wechatNick_list)
                print('恢复规划师的账号微信信息',old_wechat_id,old_wechat,old_wechat_nick)
                self.planner.api_update_ghs_wechat_account(
                    ghs_wechat_infos(email_address=planner1['email'], wechat_nick=old_wechat_nick,
                                     wechat=old_wechat, wechat_account_id=old_wechat_id))
                break
            else:
                # print('规划师邮箱不一致',data['email'], planner1['email'])
                pass

    @pytest.mark.skip
    def test_migrate_ghs_wechat_account(self):
        """
        @Author  : Grace
        1：微信号迁移
        """
        wechat_list = self.planner.api_get_ghs_wechat_list().get('data')
        planner1 = random.choice(wechat_list)
        planner2 = random.choice(wechat_list)
        #email_list = self.planner.api_get_ghs_user_list(subject_type='all').get('data').get('emailList')
        #planner2 = random.choice(email_list)
        old_wechat_id = planner1.get('wechatList')[0].get('id')
        old_email = planner1.get('wechatList')[0].get('emailAddress')
        #new_email = planner2.get('email')
        print(planner1.get('wechatList')[0].get('id'))
        print('*****把id', old_wechat_id, '从规划师', old_email, '迁移规划师', planner2['email'])
        #print(planner1['email'], planner2['emailAddress'], old_wechat_id)
        self.planner.api_migrate_ghs_wechat_account(
            old_email=old_email,
            new_email=planner2['email'],
            wechat_account_id=old_wechat_id)
        row_list = self.planner.api_get_ghs_wechat_list().get('data')
        for data in row_list:
            if data['email'] == planner2['email']:
                print("邮箱信息：",data['email'],planner2['email'])
                wechat_list = data['wechatList']
                self.wechat_id_list = []
                for id in wechat_list:
                    print('for循环中id取值', id['id'])
                    self.wechat_id_list.append(id['id'])
                print('迁移后规划师的微信号list:',self.wechat_id_list)
                pytest_check.is_in(old_wechat_id, self.wechat_id_list)
                print('把id',old_wechat_id,'从',planner2['email'],'迁移回到', planner1['email'])
                self.planner.api_migrate_ghs_wechat_account(old_email=old_email,
                                                            new_email=planner2['email'],
                                                            wechat_account_id=old_wechat_id)
                break
            else:
                print('规划师邮箱不一致',data['email'], planner2['emailAddress'])

        #迁移回
        # self.planner.api_migrate_ghs_wechat_account(
        #     old_email=planner2['emailAddress'],
        #     new_email=old_email,
        #     wechat_account_id=old_wechat_id)


    @classmethod
    def teardown_class(cls):
        """当前类结束后默认执行方法"""
        cls.user.logout()
        print(cls.user.cookies)