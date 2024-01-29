# -*- coding: utf-8 -*-
"""
@Time    : 2021/8/03
@Author  : Grace
@File    : test_promoter_leaders.py

case：
编辑组长信息
加入分配序列

"""

import pytest
from config.env.domains import Domains, ROOT_PATH
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiPromoter.ApiPromoter import ApiPromoter
import pytest_check
from business.CrmQuery import CrmZaryaQuery
from testcase.Crm.TestPromoter import conftest
import random
import datetime
import time
import string

@pytest.mark.xCrm
class TestPromoterLeaders(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        print(cls.config)
        cls.user = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.promoter = ApiPromoter(cls.user.cookies)
        cls.query_zarya = CrmZaryaQuery()

        '''数据库随机获取一个推广人
        cls.promoter_data = random.choice(cls.query_zarya.query_zarya_info(table='promoterdetail', time_removed=0))
        print(cls.promoter_data)'''




    @pytest.mark.reg
    def test_update_promoter_leaders(self,promoter_leader_search_infos):
        """
        @Author  : Grace
        1：编辑更新推广人组长信息
        """
        #随机找到一个推广人组长
        promoter_leaders = random.choice(self.promoter.api_promoter_leader_all().get('data'))
        print('随机挑选的推广人组长信息:',promoter_leaders)
        #修改推广人组长的数据
        new_wechat_account = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        new_wechat_type = random.choice(['personal','business'])
        new_work_time_type =random.choice(['parttime','fulltime'])
        print('新的推广人组长信息',new_wechat_account,new_wechat_type,new_work_time_type)
        self.promoter.api_promoter_leader_edit(promoter_leaders['id'],new_wechat_type,new_work_time_type
                                               ,promoter_leaders['wechat_qrcode_image_url'],new_wechat_account)
        #查找修改后的数据和预期一致
        search_data = self.promoter.api_promoter_leader_search(promoter_leader_search_infos(email=promoter_leaders['email'])).get('data').get('list')
        pytest_check.equal(search_data[0]['wechat_type'],new_wechat_type)
        pytest_check.equal(search_data[0]['work_time_type'], new_work_time_type)
        pytest_check.equal(search_data[0]['wechat_account'], new_wechat_account)
        #恢复数据
        self.promoter.api_promoter_leader_edit(promoter_leaders['id'], promoter_leaders['wechat_type'],
                                               promoter_leaders['work_time_type']
                                               , promoter_leaders['wechat_qrcode_image_url'],
                                               promoter_leaders['wechat_account'])

    @classmethod
    def teardown_class(cls):
        """当前类结束后默认执行方法"""
        cls.user.logout()
        print(cls.user.cookies)
