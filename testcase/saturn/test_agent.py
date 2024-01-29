# coding=utf-8
# @Time    : 2021/1/27 4:24 下午
# @Author  : jerry
# @File    : test_agent.py

import pytest

from business.saturn.ApiCustomerLesson import ApiCustomerLesson
from business.mysqlQuery import SaturnQuery
from config.env.domains import Domains
from business.saturn.ApiChannel import ApiChannel
from business.saturn.ApiTrialClass import ApiTrialClass


@pytest.mark.saturn
class TestAgent:

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.channel = ApiChannel()
        cls.SaturnQuery= SaturnQuery()

    @classmethod
    def teardown_class(cls):
        """删除开课记录"""
        cls.SaturnQuery.delete_data("delete from saturn_class_open_record where uid='a3704e99e1fa43e4a092e18dd1050c64'")


    def get_token(self, user_name, user_pwd):
        login_res = self.channel.api_admin_login(username=user_name, password=user_pwd)
        return login_res['data']['token']


    @pytest.mark.parametrize("user_name, user_pwd", [("manager", "123")])
    def test_channel_login(self, user_name, user_pwd):
        """代理商正常登陆"""
        token = self.get_token(user_name, user_pwd)
        channel = ApiChannel(token)
        login_res = channel.api_admin_login(username=user_name, password=user_pwd)
        assert login_res['data']['menuList'] == ['employee_management', 'fan_list', 'achievement', 'open_trial_class', 'open_system_class', 'trial_class_spu']

    @pytest.mark.parametrize("user_name, user_pwd", [("staff", "123")])
    def test_employee_login(self, user_name, user_pwd):
        """员工正常登陆"""
        token = self.get_token(user_name, user_pwd)
        channel = ApiChannel(token)
        login_res = channel.api_admin_login(username=user_name, password=user_pwd)
        assert login_res['data']['menuList'] == ['employee_management', 'fan_list']

    @pytest.mark.parametrize("page_no, page_size, user_name, user_pwd" ,[(1,20, "manager", "123")])
    def test_employee_list_agent(self,page_no,page_size, user_name, user_pwd):
        """代理商查看员工列表"""
        token = self.get_token(user_name, user_pwd)
        channel = ApiChannel(token)
        employee_list = channel.api_employee_list(page_no=page_no,page_size=page_size)
        db_result = self.SaturnQuery.query_tables("select * from saturn_user_accounts where leader_uuid='b825b69e07fd415aab54981b8645f01b'")
        db_result2 = self.SaturnQuery.query_tables(
            "select * from saturn_user_accounts where leader_uuid='b825b69e07fd415aab54981b8645f01b' order by id desc limit 1")
        assert employee_list['data']['total'] == len(db_result)
        assert employee_list['data']['list'][0]['name'] == db_result2[0]['account_name']
        assert employee_list['data']['list'][0]['id'] == db_result2[0]['uuid']

    @pytest.mark.parametrize("page_no, page_size, user_name, user_pwd", [(1, 20, "staff", "123")])
    def test_employee_list_employee(self,page_no,page_size, user_name, user_pwd):
        """员工查看员工列表"""
        token = self.get_token(user_name, user_pwd)
        channel = ApiChannel(token)
        employee_list = channel.api_employee_list(page_no=page_no,page_size=page_size)
        db_result = self.SaturnQuery.query_tables(
            "select * from saturn_user_accounts where leader_uuid='b825b69e07fd415aab54981b8645f01b' and uuid='91c2c94f9ad846f3b5c2976734478acb'")
        assert employee_list['data']['total'] == len(db_result)
        assert employee_list['data']['list'][0]['name'] == db_result[0]['account_name']
        assert employee_list['data']['list'][0]['id'] == db_result[0]['uuid']

    @pytest.mark.parametrize("page_no, page_size, user_name, user_pwd", [(1, 20, "manager", "123")])
    def test_employee_fans_init(self, page_no, page_size, user_name, user_pwd):
        """线索管理-初始化状态"""
        token = self.get_token(user_name, user_pwd)
        channel = ApiChannel(token)
        employee_fans = channel.api_employee_fans(page_no=page_no,page_size=page_size)
        db_result1 = self.SaturnQuery.query_tables(
            "select * from saturn_user_account_fans where account_uuid in('91c2c94f9ad846f3b5c2976734478acb','91c2c94f9ad846f3b5c2976734478acc') and fan_status='active'")
        db_result2 = self.SaturnQuery.query_tables(
            "select * from saturn_user_account_fan_orders where fan_id in (select id from saturn_user_account_fans where account_uuid in('91c2c94f9ad846f3b5c2976734478acb','91c2c94f9ad846f3b5c2976734478acc') and fan_status='active') order by create_time desc limit 1;")
        assert employee_fans['data']['total'] == len(db_result1)
        print(employee_fans['data']['list'][0]['orderList'][0]['productName'])
        assert employee_fans['data']['list'][0]['orderList'][0]['productName'] == db_result2[0]['ttl']

    @pytest.mark.parametrize("page_no, page_size, account_id, mobile, user_name, user_pwd", [(1, 20,"91c2c94f9ad846f3b5c2976734478acc","19700000111", "manager", "123")])
    def test_employee_fans_query(self, page_no, page_size, account_id, mobile, user_name, user_pwd):
        """绩效管理-组合查询"""
        token = self.get_token(user_name, user_pwd)
        channel = ApiChannel(token)
        employee_fans = channel.api_employee_fans(page_no=page_no, page_size=page_size,account_id=account_id,mobile=mobile)
        db_result1 = self.SaturnQuery.query_tables(
            "select * from saturn_user_account_fan_orders where uid='a3704e99e1fa43e4a092e18dd1050c64';")
        db_result2 = self.SaturnQuery.query_tables(
            "select * from saturn_user_account_fan_orders where uid='a3704e99e1fa43e4a092e18dd1050c64' order by id desc limit 1")
        assert employee_fans['data']['total'] == len(db_result1)
        assert employee_fans['data']['list'][0]['orderList'][0]['productName'] == db_result2[0]['ttl']

    @pytest.mark.parametrize("user_name,user_pwd",[("manager", "123")])
    def test_trial_inventory_info(self,user_name,user_pwd):
        """9.9课程解锁-页面库存展示"""
        token = self.get_token(user_name, user_pwd)
        trial = ApiTrialClass(token)
        trial_inventory_info = trial.api_trial_inventory_info()
        db_result1 = self.SaturnQuery.query_tables("select sum(remaining_quantity) from saturn_inventory_trial_class "
                                                   "where account_uuid='b825b69e07fd415aab54981b8645f01b' and valid_end>=now()")
        db_result2 = self.SaturnQuery.query_tables("select remaining_quantity from saturn_inventory_trial_class where account_uuid='b825b69e07fd415aab54981b8645f01b' order by valid_end limit 1")
        db_result3 = self.SaturnQuery.query_tables(
            "select valid_end from saturn_inventory_trial_class where account_uuid='b825b69e07fd415aab54981b8645f01b' order by valid_end limit 1")
        assert trial_inventory_info['data']['total'] == db_result1[0]['sum(remaining_quantity)']
        stock = db_result2[0]['remaining_quantity']
        msg = trial_inventory_info['data']['msg']
        assert str(stock) in msg
        date1 = "".join(filter(str.isdigit, msg.split("，")[1]))
        date2 = db_result3[0]['valid_end'].strftime("%Y%m%d")
        assert date2 == date1


    @pytest.mark.parametrize("user_name,user_pwd,mobile", [("manager", "123","19700000111")])
    def test_trial_open(self, user_name, user_pwd,mobile):
        """给粉丝开课"""
        token = self.get_token(user_name, user_pwd)
        trial = ApiTrialClass(token)
        stock_before = self.SaturnQuery.query_tables("select remaining_quantity from saturn_inventory_trial_class where account_uuid='b825b69e07fd415aab54981b8645f01b' order by valid_end limit 1")
        trial_open = trial.api_trial_open(mobile)
        stock_after = self.SaturnQuery.query_tables(
            "select remaining_quantity from saturn_inventory_trial_class where account_uuid='b825b69e07fd415aab54981b8645f01b' order by valid_end limit 1")
        assert trial_open['msg'] == 'ok'
        assert stock_before[0]['remaining_quantity'] == stock_after[0]['remaining_quantity'] + 1

    @pytest.mark.parametrize("user_name,user_pwd,mobile", [("manager", "123","17333333333")])
    def test_trial_open_notfans(self, user_name, user_pwd,mobile):
        """非粉丝不能开9.9体验课"""
        token = self.get_token(user_name, user_pwd)
        trial = ApiTrialClass(token)
        trial_open = trial.api_trial_open(mobile)
        assert trial_open['code'] == 30001
        assert trial_open['msg'] == '开课失败，请先扫码完成绑定'

    @pytest.mark.parametrize("user_name,user_pwd,mobile,pageNo, pageSize", [("manager", "123", "19900010001",1,20)])
    def test_trial_open_list(self, user_name, user_pwd, mobile,pageNo, pageSize):
        """已开课粉丝查询"""
        token = self.get_token(user_name, user_pwd)
        trial = ApiTrialClass(token)
        trial_open_list = trial.api_trial_open_list(mobile,pageNo, pageSize)
        print(trial_open_list)
        db_result1 = self.SaturnQuery.query_tables("select count(*) from saturn_class_open_record where uid='0604478d469c444496758b95a7476db8'")
        db_result2 = self.SaturnQuery.query_tables(
            "select mobile from saturn_class_open_record where account_uuid='b825b69e07fd415aab54981b8645f01b' limit 1")
        assert trial_open_list['data']['total'] == db_result1[0]['count(*)']
        assert trial_open_list['data']['list'][0]['mobile'] == db_result2[0]['mobile']

    @pytest.mark.parametrize("user_name,user_pwd,uid,bid", [("manager", "123", "fc713e10b6f94818b7869b61c04592b9", "c06f42d200f144d8a395f2b39a765e82")])
    def test_get_course_baby_list(self,user_name,user_pwd,uid,bid):
        """baby信息和学习信息"""
        token = self.get_token(user_name, user_pwd)
        customer = ApiCustomerLesson(token)
        course_info = customer.api_course_list(uid)
        baby_info = customer.api_baby_list(uid)
        learning_record = customer.api_baby_learning_record(uid,bid)
        assert course_info['data'][0]['ttl'] == '呱呱英语体系课'
        assert baby_info['data'][0]['bid'] == bid
        assert learning_record['msg'] == 'ok'

    # 非P0 case暂时注释掉
    # @pytest.mark.parametrize("user_name, user_pwd", [("qjdstaff", "")])
    # def test_login_fail1(self, user_name, user_pwd):
    #     """用户名/密码不存在，登陆失败"""
    #     channel = ApiChannel()
    #     login_res = channel.api_admin_login(username=user_name, password=user_pwd)
    #     assert login_res['code'] == 10002
    #     assert login_res['msg'] == "用户名密码不可为空"
    #
    # @pytest.mark.parametrize("user_name, user_pwd", [("qjdstaff", "1234567")])
    # def test_login_fail2(self, user_name, user_pwd):
    #     """用户名/密码错误，登陆失败"""
    #     channel = ApiChannel()
    #     login_res = channel.api_admin_login(username=user_name, password=user_pwd)
    #     assert login_res['code'] == 10001
    #     assert login_res['msg'] == "登陆失败"
