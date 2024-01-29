'''
学员查询模块
'''
import pytest

from business.Crm.ApiShare.ApiShare import ApiShare
from config.env.domains import Domains
from business.Crm.ApiAccount.userProperty import UserProperty
from business.Crm.ApiPlanner.ApiPlanner import ApiPlanner
from business.businessQuery import ghsQuery, ggrCustomerRightQuery
from business.CrmQuery import CrmJainaQuery, CrmAllianceQuery
import pytest_check
import random


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
        cls.Alliance = CrmAllianceQuery()
        cls.mongo = ghsQuery()  # mg
        cls.mongo_ggr = ggrCustomerRightQuery()  # mg
        cls.ApiShare = ApiShare(cls.session.cookies)

    def test_materia_data(self):
        """
        @ting
        获取用户拥有的魔石
        1、随机获取一个规划师学员手机号（接口api_get_students()/mysql）
        2、通过接口获取学员的魔石/钻石
        3、校验学员查询接口和数据库的准确性
        """
        students = self.query.query_jaina_info(table='students')[0]
        gua_id = students['gua_id']
        magika_total, magika_overage = students['magika_total'], students.get('magika_overage')
        data = self.planner.get_point_detail(gua_id).get('data')
        magike = data.get('magika_info')
        pytest_check.equal(magike.get('total_magika'), magika_total)

    def test_student_basic_data(self):
        """
        @ting
        根据呱号获取学员基础信息-mongo_users手机号，UID,注册途径
        个人信息的注册时间:暂不写、呱豆余额暂不写-->暂不支持转化
        """
        mg_gusher = self.mongo.query_table_info('users')[0]
        mobile, uid, typ = mg_gusher['mobile'], mg_gusher['_id'], mg_gusher['typ']
        api_user = self.planner.get_basic_detail(mobile).get('data')
        api_gua = api_user.get('basic_info').get('user')
        pytest_check.equal(api_gua.get('mobile'), mobile)
        pytest_check.equal(api_gua.get('typ'), typ)

    def test_first_purchase(self):
        """
        用户首购购买信息
        """
        mg_user = self.mongo.query_table_info('ghs_user')[0]
        grid = mg_user['ghs']
        uid = mg_user['_id']
        api_itemId = self.planner.get_ghs_detail(uid).get('data')
        api_ghs = api_itemId.get('ghs_info').get('ghs').get('ghs_id')
        api_ghs = str(api_ghs)
        pytest_check.equal(api_ghs, grid)

    def test_quack_reading_vip(self):
        """
        @ting,P1
        学员查询、验证用户是否拥有呱呱阅读vip终身卡
        uid：用户的uid
        """
        uid = random.choice(self.query.query_jaina_info(table='students')).get('user_id')
        api_ggr_vip_time = self.planner.get_basic_detail(uid).get('data').get('basic_info').get('user').get(
            'ggr_vip_time')
        mg_vip_rand = self.mongo_ggr.query_table_info('vip_record', uid='uid')
        mg = mg_vip_rand.count()
        li = []
        if mg > 0:
            for di in mg_vip_rand:
                for i, o in di.items():
                    if i == 'duration':
                        li.append(o)
            if 36500 in li:
                if api_ggr_vip_time != "还不是vip":
                    print(uid, '有终身卡')
        if mg == 0:
            if api_ggr_vip_time == "还不是vip":
                print(uid, '没有终身卡')
        if api_ggr_vip_time == "还不是vip" and 36500 in li:
            print(uid, '数据库信息与接口信息不一致，数据库返回拥有终身卡接口返回无终身卡')
        if api_ggr_vip_time != "还不是vip":
            if mg > 0:
                print(uid, '此用户有呱呱记录，但不是终身卡,时间截止', api_ggr_vip_time)

    def test_lan_evaluation(self):
        """
        @ting、P1
        用户是否拥有蓝思测评记录
        数据库：   ggr_customer_rights下的lexile_test_record表，uts：蓝思测评使用时间
        """
        uid = random.choice(self.query.query_jaina_info(table='students')).get('user_id')
        api_ggr_vip_time = self.planner.get_basic_detail(uid).get('data').get('basic_info').get('user').get(
            'lexile_status')
        mg_len_status = self.mongo_ggr.query_table_info('lexile_test_record', uid='uid')
        mg = mg_len_status.count()
        if mg == 0:
            if api_ggr_vip_time == '/':
                print(uid, '此用户没有蓝思测评')
            elif api_ggr_vip_time != '/':
                print(uid, '数据库有信息，接口无返回')
        if mg != 0:
            if api_ggr_vip_time != '/':
                print(uid, '此用户有蓝思测评')
            elif api_ggr_vip_time == '/':
                print(uid, '数据库无信息，接口有返回')

    def test_follow_up_information(self):
        """
        @ting、P1验证学员查询跟进信息模块
        self：登陆人的uuid
        comment_content：要备注的信息
        优化：将数据库时间进行转换与当前时间做对比
        """
        land_uuid = '2fd82252a49f4a75acddeae0571f025a'
        students_uid = random.choice(self.query.query_jaina_info(table='students')).get('user_id')
        random_string = random.choice("秦时明月汉时关万里长征人未还但使龙城飞将在不教胡马度阴山")
        self.ApiShare.api_create_student_comment(land_uuid, students_uid, random_string)
        mg_len_status = self.Alliance.query_alliance_info(table='comments', user_id=students_uid)
        ls = []
        for li in mg_len_status:
            for i, o in li.items():
                if i == 'comment_content':
                    ls.append(o)
        if random_string in ls:
            print(students_uid, '本次添加的备注信息为', random_string)

    def test_diamonds_number(self):
        """
        @ting 、p1
        验证用户钻石的使用情况
        JLGL下point_user,available_point:可用钻石
        """
        api_minds = self.planner.get_point_detail('2b1642ce933d4b039a0ab30c170cd69f').get('data').get('point_info')
        api_Diamonds_balance = api_minds.get('available_point')
        mongo = self.mongo.query_table_info('point_user', _id='2b1642ce933d4b039a0ab30c170cd69f')
        mongo_minds = mongo.count()
        li = []
        if mongo_minds > 0:
            for i in mongo:
                for it, io in i.items():
                    if it == 'point':
                        li.append(io)
        if api_Diamonds_balance in li:
            print('钻石余额为', api_Diamonds_balance)
