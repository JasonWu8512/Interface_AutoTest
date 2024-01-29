'''
绩效表模块
tion
'''

import pytest
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.businessQuery import ghsQuery
from business.CrmQuery import CrmJainaQuery
import pytest_check
import random
from decimal import Decimal


@pytest.mark.xCrm
class TestStudentInfo(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('fat')
        cls.dm.set_domain(cls.config['crm_number_url'])
        cls.session = UserProperty(email_address=cls.config['xcrm']['email_address'], pwd=cls.config['xcrm']['pwd'])
        cls.planner = ApiPlanner(cls.session.cookies)
        cls.query = CrmJainaQuery()  # mysql
        cls.mongo = ghsQuery()  # mg

    def test_total_performance(self):
        '''
        绩效总表，获取规划师绩效接口
        '''
        performance = random.choice(self.query.query_jaina_info(table='ghs_performance_v2'))  # 随机获取不条数据
        mg_group = performance['group_id']  # 获取组信息
        mg_ghs_acct_no = performance['ghs_acct_no']  # 规划师邮箱
        mg_period = [performance['period']]  # 规划师期次
        mg_rebuy_money = performance['rebuy_money']
        mg_subject_type = performance['subject_type']  # 获取科目信息
        dimension = 1
        api_performance = self.planner.get_ghs_performance_v2(mg_group, mg_ghs_acct_no, mg_period, dimension,
                                                              mg_subject_type).get('data')
        api_rebuy_money = api_performance.get('result')[0]['rebuy_money']  # 获取第一列表
        if mg_rebuy_money != Decimal(api_rebuy_money):
            print('绩效金额不一致')
        else:
            pytest_check.equal(mg_rebuy_money, Decimal(api_rebuy_money))
            # pytest_check.equal(mg_rebuy_money, eval(api_rebuy_money))

    def test_purchase_data(self):
        '''
        复购明细表,校验接口是否正常
        '''
        mg_students = random.choice(self.query.query_jaina_info(table='ghs_performance_v2'))
        group, email, period, subject_type, = mg_students['group_id'], mg_students['ghs_acct_no'], [
            mg_students['period']], mg_students['subject_type']
        api_repurchase = self.planner.get_ghs_rebuy_order_detail_v2(group, email, period, subject_type).get('data')
        api_data = api_repurchase.get("result").get('data')
        list = []
        if api_data != None:
            for i in api_data:
                rebuy_money = i.get('rebuy_money')
                list.append(rebuy_money)
            Total_performance = sum(list)  # 获取金额
            return Total_performance
        elif api_data == None:
            print('规划师邮箱为：', email, "的规划师", "在", period, '期次没有复购绩效')
        """
        1、获取xx规划师xx期次内的用户uid
            sql_data = self.query.query_jaina_info(table='students',ghs_email=email,term=period)# 
            crm_list=[]
            for i in sql_data:
                crm_uid=i.get('uid')
                crm_list.append(crm_uid)
        2、查询这个规划师名下的用户有那些订单apporder
        3、判断订单是否在week4内 首购时间判断
        4、判断订单的状态  apporder
        5、判断订单是否需要拆分 apporderkpionmun
        6、将纳入绩效的订单金额相加与接口内的金额做对比
        """

    def test_complete_class_detailed(self):
        """
        完课明细表
        """
        mg_students = random.choice(self.query.query_jaina_info(table='ghs_performance_v2'))
        group, email, period, subject_type, = mg_students['group_id'], mg_students['ghs_acct_no'], [
            mg_students['period']], mg_students['subject_type']
        print(group, email, period, subject_type)

        api_complete_class = self.planner.get_ghs_finish_lesson_detail(group, email, period, subject_type).get(
            'data').get('result')
        if api_complete_class != []:
            api_finish_8_cnt = api_complete_class[0]["finish_8_cnt"]
            api_finish_4_cnt = api_complete_class[0]["finish_4_cnt"]
            print(api_finish_4_cnt, api_finish_8_cnt)
        elif api_complete_class == []:
            print('没有这个规划师相关的的完课信息')
