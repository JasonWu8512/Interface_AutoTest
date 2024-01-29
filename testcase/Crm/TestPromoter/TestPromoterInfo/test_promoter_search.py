# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/23
@Author  : Grace
@File    : test_promoter_search.py

case：
查询推广人
修改tag
获取备注，更新备注
更新推广人的组长和期次
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
class TestPromoterSearch(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        print(cls.config)
        cls.user = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.promoter = ApiPromoter(cls.user.cookies)
        cls.query_zarya = CrmZaryaQuery()
        '''数据库随机获取一个推广人'''
        cls.promoter_data = random.choice(cls.query_zarya.query_zarya_info(table='promoterdetail', time_removed=0))
        print(cls.promoter_data)
        '''xshare库获取推广人标签'''



    @pytest.mark.reg
    def test_get_promoter_info(self,search_promoter_infos):
        """
        @Author  : Grace
        1：根据推广人id查询推广人信息
        """
        api_data = self.promoter.api_promoter_search(search_promoter_infos(promoter_info=self.promoter_data['promoter_id'])).get('data')
        print(api_data)
        pytest_check.equal(api_data['list'][0]['promoter_id'], self.promoter_data['promoter_id'])
        pytest_check.equal(api_data['list'][0]['promoter_guaid'], self.promoter_data['promoter_guaid'])
        pytest_check.equal(api_data['list'][0]['promoter_mobile'], self.promoter_data['promoter_mobile'])

    @pytest.mark.reg
    def test_update_promoter_tags(self, search_promoter_infos):
        """
        @Author  : Grace
        1：修改标签
        """
        #随机获取一个推广人
        promoter_data = random.choice(self.promoter.api_promoter_search(search_promoter_infos()).get("data").get("list"))
        print("随机获取的推广人信息:", promoter_data)
        # 随机选择一个标签
        new_tag = random.choice(self.promoter.api_promoter_all_tags().get("data").get("tags"))
        print("随机获取的标签：", new_tag)
        new_tags_list=[]
        new_tags_list.append(new_tag)
        #删除推广人目前的标签,再新增一个标签
        self.promoter.api_promoter_tag_update(promoter_id=promoter_data["promoter_id"], tags=[])
        self.promoter.api_promoter_tag_update(
            promoter_id=promoter_data["promoter_id"], tags=[new_tag]
        )
        time.sleep(200)
        search_resp = self.promoter.api_promoter_search(search_promoter_infos(promoter_info=promoter_data['promoter_id'])).get("data")
        print("修改标签后的推广人信息:",search_resp)
        pytest_check.equal(search_resp['list'][0]['promoter_tags'],new_tags_list)

    @pytest.mark.reg
    def test_update_promoter_remark(self, search_promoter_infos):
        """
            @Author  : Grace
            1：获取备注，更新备注
        """
        #随机获取一个推广人的标签
        promoter_data = random.choice(self.promoter.api_promoter_search(search_promoter_infos()).get("data").get("list"))
        print("随机获取的推广人和备注为:", promoter_data["promoter_id"], promoter_data["remark"])
        #修改推广人的标签
        new_remark = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        print("随机生成的备注:", new_remark)
        self.promoter.api_update_promoter_remark(promoter_data['promoter_id'],new_remark)
        #搜索该标签，搜索结果是刚刚随机挑选的推广人
        search_resp = self.promoter.api_promoter_search(search_promoter_infos(remark=new_remark)).get("data").get('list')
        print("根据新备注搜索到的推广人信息:", search_resp)
        pytest_check.equal(search_resp[0]['promoter_id'], promoter_data['promoter_id'])
        #恢复数据，备注改为老备注
        self.promoter.api_update_promoter_remark(promoter_data['promoter_id'], promoter_data["remark"])

    @pytest.mark.reg
    @pytest.mark.parametrize('leader_id,group_type,new_leader_id,sn_key',
                             [(23,0,45,'newbie_period'),
                              (47,1,25,'partner_period'),
                              (59,2,57,'newbie_outside_period'),
                              (58,3,60,'partner_outside_period')])
    def test_update_promoter_sn(self, search_promoter_infos,leader_id,group_type,new_leader_id,sn_key):
        """
            @Author  : Grace
            1：更新推广人的组长和期次
        """
        #搜索某个营期的组长数据，随机获取一个推广人
        promoter_data = random.choice(
            self.promoter.api_promoter_search(search_promoter_infos(leader_id=leader_id,group_type=group_type)).get("data").get("list"))
        print("随机获取的推广人信息为:", promoter_data)
        #选择一个新组长，获取该组长的期次，随机选择一个期次
        group_data = random.choice(self.promoter.api_get_group_by_leader_id(new_leader_id).get('data'))
        print('新的组长和期次为:',group_data)
        #更新推广人的组长和期次为新组长，新期次
        self.promoter.api_update_promoter_sn(promoter_data['promoter_id'],group_type,new_leader_id,group_data['sn'])
        #搜索该推广人，检查组长和期次已更新（由于历史实现原因，更新后es内没有刷新，所以通过更改备注来刷新下es再查询，做最后更新的校验）
        # 修改推广人的标签
        new_remark = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        print("随机生成的备注:", new_remark)
        self.promoter.api_update_promoter_remark(promoter_data['promoter_id'], new_remark)
        self.promoter.api_update_promoter_remark(promoter_data['promoter_id'], promoter_data['remark'])
        resp_data = self.promoter.api_promoter_search(search_promoter_infos(promoter_info=promoter_data['promoter_id'])).get('data').get('list')
        print('修改组长和期次后的推广人信息',resp_data)
        pytest_check.equal(resp_data[0][sn_key], group_data['sn'])
        #数据恢复
        self.promoter.api_update_promoter_sn(promoter_data['promoter_id'], group_type, leader_id,
                                             promoter_data[sn_key])



    @classmethod
    def teardown_class(cls):
        """当前类结束后默认执行方法"""
        cls.user.logout()
        print(cls.user.cookies)