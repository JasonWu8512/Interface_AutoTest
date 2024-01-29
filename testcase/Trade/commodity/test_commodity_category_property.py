# @Time : 2021/7/30
# @Author : kira
# @File : ApiCommodityCategory.py
# @Software: PyCharm

import time

import pytest
from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth
from business.Trade.eshopAdmin.ApiCommodityCategory import ApiCommodityCategory
from business.Trade.eshopAdmin.ApiCommodityPropertys import ApiCommodityPropertys
from business.mysqlQuery import EshopQuery
from config.env.domains import Domains


@pytest.mark.Trade
@pytest.mark.EshopAdmin
@pytest.mark.TradeCommodity
class TestCommodityCategoryProperty:
    """
    后台新商品管理-商品类目管理/商品属性管理相关测试
    """

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_commodityCategory = ApiCommodityCategory(token=a_token)
        cls.eshop_admin_commodityProperty = ApiCommodityPropertys(token=a_token)
        cls.eshop_query = EshopQuery()

    @pytest.fixture(scope='class')
    def get_category_init_value(self):
        """初始化类目接口参数"""
        parent_code = self.eshop_admin_commodityCategory.api_get_category_list()['data']['categories'][0][
            'categoryNo']  # 获取父类目编码
        category_initialization = {
            'categoryNo': 'test_category_1.0',  # 新建类目编码
            'title': '测试_类目_T1.0',  # 新建类目名称
            'edit_title': '测试_类目_T1.1',  # 修改/子类目名称
            'edit_code': 'test_category_1.1',  # 修改/子类目编码
            'parent_code': parent_code
        }
        return category_initialization

    def test_get_category_list(self):
        """
        查看类目列表
        """
        res = self.eshop_admin_commodityCategory.api_get_category_list()
        assert res['code'] == 0

    @pytest.mark.parametrize("state", [1, 2])
    def test_create_edit_category(self, state, get_category_init_value):
        """
        1、新增子类目
        2、编辑类目：名称、启用状态
        3、类目名称输入框校验：输入符合条件的数据，校验通过
        4、类目编码输入框校验：输入符合条件的数据，校验通过
        5、类目名称输入框校验：输入重复的类目名称，校验不通过
        6、类目编码输入框校验：输入重复的类目编码，校验不通过
        7、编辑默认类目，校验不通过
        8、类目名称输入框校验：输入为空/空串/不符合条件，校验不通过
        9、类目编码输入框校验：输入为空/空串/不符合条件，校验不通过
        """
        # 初始化新建类目接口参数
        edit_state = 2 if state == 1 else 1  # 修改类目状态
        # 新建一个二级类目
        res_1 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title=get_category_init_value['title'],
                                                                            categoryNo=get_category_init_value['categoryNo'], state=state,
                                                                            create='true')
        # 新建一个类目名称重复的子类目
        res_3 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title=get_category_init_value['title'],
                                                                            categoryNo='test_category_1.2',
                                                                            state=state, create='true')
        # 新建一个类目编码重复的子类目
        res_4 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title='测试_类目_T1.0', categoryNo=get_category_init_value['categoryNo'],
                                                                            state=state, create='true')
        # 编辑默认类目
        res_5 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo='courses',
                                                                            title='测试_类目_T1.3',
                                                                            categoryNo='trial_courses', state=state,
                                                                            create='false')
        # 查询数据库落库情况
        query_1 = self.eshop_query.query_commodity_category_category_no(get_category_init_value['categoryNo'])
        # 新建一个类目名称为空的子类目
        res_6 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title='', categoryNo=get_category_init_value['categoryNo'],
                                                                            state=state, create='true')
        # 新建一个类目编码为空的子类目
        res_7 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title='测试_类目_T1.3', categoryNo='',
                                                                            state=state, create='true')
        # 类目名称不符合条件
        res_8 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title='&*', categoryNo=get_category_init_value['categoryNo'],
                                                                            state=state, create='true')
        # 类目编码不符合条件
        res_9 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title='测试_类目_T1.3', categoryNo='&*%',
                                                                            state=state, create='true')
        # 编辑刚新建的类目
        res_2 = self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'],
                                                                            title=get_category_init_value['edit_title'], categoryNo=get_category_init_value['categoryNo'],
                                                                            state=edit_state, create='false')
        time.sleep(1)
        # 查询数据库落库情况
        query_2 = self.eshop_query.query_commodity_category_category_no(get_category_init_value['categoryNo'],)
        # 删除新增加的类目
        self.eshop_query.delete_commodity_category_category_no(get_category_init_value['categoryNo'],)
        # 新建编辑（1-4）
        assert res_1['code'] == 0
        assert res_2['code'] == 0
        assert query_1[0]['title'] == get_category_init_value['title']
        assert query_1[0]['state'] == state
        assert query_2[0]['title'] == get_category_init_value['edit_title']
        assert query_2[0]['state'] == edit_state
        # 重复性校验（5-6）
        assert res_3['code'] == 37005
        assert res_4['code'] == 37005
        # 编辑默认类目（7）
        assert res_5['code'] == 37002
        # 字符校验
        assert res_6['code'] == 10400
        assert res_7['code'] == 10400
        assert res_8['code'] == 10400
        assert res_9['code'] == 10400

    def test_disable_enable_parent_category(self, get_category_init_value):
        """
        1、禁用父类目，子类目状态也会变成禁用
        2、启用父类目，子类目状态也会变成启用
        """
        # 手动新建一个二级类目
        self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'], title=get_category_init_value['title'],
                                                                    categoryNo=get_category_init_value['categoryNo'], state=1,
                                                                    create='true')
        # 手动新建一个三级类目
        self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['categoryNo'],
                                                                    title=get_category_init_value['edit_title'],
                                                                    categoryNo=get_category_init_value['edit_code'], state=1,
                                                                    create='true')
        # 禁用父类目
        self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'], title=get_category_init_value['title'],
                                                                    categoryNo=get_category_init_value['categoryNo'], state=2,
                                                                    create='false')
        # 查询子类目状态
        query_1 = self.eshop_query.query_commodity_category_category_no(get_category_init_value['edit_code'])
        # 启用父类目
        self.eshop_admin_commodityCategory.api_create_edit_category(parentCategoryNo=get_category_init_value['parent_code'], title=get_category_init_value['title'],
                                                                    categoryNo=get_category_init_value['categoryNo'], state=1,
                                                                    create='false')
        # 查询子类目状态
        query_2 = self.eshop_query.query_commodity_category_category_no(get_category_init_value['edit_code'])
        # 删除新增加的类目
        self.eshop_query.delete_commodity_category_category_no(get_category_init_value['categoryNo'])
        self.eshop_query.delete_commodity_category_category_no(get_category_init_value['edit_code'])
        assert query_1[0]['state'] == 2
        assert query_2[0]['state'] == 1

    def test_get_property_list(self):
        """
        查看属性列表
        """
        res = self.eshop_admin_commodityProperty.api_get_property_list()
        assert res['code'] == 0
        assert res['data']['properties'][0]['code'] == 'subject'
        assert res['data']['properties'][1]['code'] == 'level'

    @pytest.mark.parametrize("propertyKeyCode", ['subject', 'level'])
    @pytest.mark.parametrize("state", [1, 2])
    def test_create_edit_property(self, propertyKeyCode, state):
        """
        1、新增属性值
        2、编辑属性值:启用状态
        3、属性名称输入框校验：科目下输入级别中的属性名称，校验通过
        4、属性编码输入框校验：科目下输入级别中的属性编码，校验通过
        5、属性名称输入框校验：科目输入重复的属性名称，校验不通过
        6、属性编码输入框校验：科目输入重复的属性编码，校验不通过
        """
        # 获取已经存在的属性值
        key = 0 if propertyKeyCode == 'subject' else 1
        key_1 = 1 if key == 0 else 0
        property_list = self.eshop_admin_commodityProperty.api_get_property_list()['data']['properties'][key]['values']
        property_list_1 = self.eshop_admin_commodityProperty.api_get_property_list()['data']['properties'][key_1][
            'values']
        # 初始化新增编辑属性值参数
        code = property_list_1[0]['code']
        title = property_list_1[0]['title']
        edit_state = 2 if state == 1 else 1
        # 添加元素keycode
        for i in range(len(property_list)):
            property_list[i].update({'keyCode': propertyKeyCode})
        batch_1 = {'propertyKeyCode': propertyKeyCode, 'code': code, 'title': title, 'state': state,
                   'keyCode': propertyKeyCode}
        property_list.append(batch_1)
        # 新增属性值
        res_1 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 查询数据库落库
        query_1 = self.eshop_query.query_commodity_property_code(code)
        # 编辑属性值
        property_list[-1]['state'] = edit_state
        res_2 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 查询数据库落库
        query_2 = self.eshop_query.query_commodity_property_code(code)
        # 同一属性输入重复的属性名
        batch_2 = {'propertyKeyCode': propertyKeyCode, 'code': 'test_property_1.0', 'title': title, 'state': state,
                   'keyCode': propertyKeyCode}
        property_list.append(batch_2)
        res_5 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 同一属性输入重复的属性code
        batch_3 = {'propertyKeyCode': propertyKeyCode, 'code': code, 'title': '测试_属性_1.0', 'state': state,
                   'keyCode': propertyKeyCode}
        property_list.append(batch_3)
        res_6 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 属性名称输入为空
        property_list.append(
            {'propertyKeyCode': propertyKeyCode, 'code': code, 'title': '', 'state': state, 'keyCode': propertyKeyCode})
        res_7 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 属性编码输入为空
        property_list.append({'propertyKeyCode': propertyKeyCode, 'code': '', 'title': '测试_属性_1.0', 'state': state,
                              'keyCode': propertyKeyCode})
        res_8 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 属性名称输入为特殊字符
        property_list.append({'propertyKeyCode': propertyKeyCode, 'code': code, 'title': '&*', 'state': state,
                              'keyCode': propertyKeyCode})
        res_9 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 属性编码输入为特殊字符
        property_list.append({'propertyKeyCode': propertyKeyCode, 'code': '&*', 'title': '测试_属性_1.0', 'state': state,
                              'keyCode': propertyKeyCode})
        res_10 = self.eshop_admin_commodityProperty.api_create_edit_property(property_list)
        # 删除新增加的属性
        self.eshop_query.delete_commodity_property_code(code)
        # 正向验证（1-4）
        assert res_1['code'] == 0
        assert res_2['code'] == 0
        assert query_1[-1]['title'] == title
        assert query_2[-1]['state'] == edit_state
        # 重复性验证（5-6）
        assert res_5['code'] == 12101
        assert res_6['code'] == 12101
        # 字符校验
        assert res_7['code'] == 999994
        assert res_8['code'] == 999994
        assert res_9['code'] == 999994
        assert res_10['code'] == 999994
