# -*- coding: utf-8 -*-
# @Time    : 2021/3/11 10:22 上午
# @Author  : jerry_wan
# @Software: PyCharm

from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from business.Trade.eshopAdmin.ApiCommodity import ApiCommodity
from business.Trade.eshopAdmin.ApiCommodityStorage import ApiCommodityStorage
from utils.enums.businessEnums import EshopCommodityStorageTypeEnum, EshopCommodityStorageStateEnum
from utils.format.format import get_all_page
from business.mysqlQuery import EshopQuery
import pytest
import shortuuid


@pytest.mark.Trade
@pytest.mark.EshopAdmin
@pytest.mark.TradeCommodity
class TestCommodityAdmin:
    """后台商品管理相关用例"""
    sxu_id = None

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        a_token = ApiAdminAuth().api_login(username=cls.config['eshop']['admin']['user'],
                                           password=cls.config['eshop']['admin']['pwd']).get('data').get('token')
        cls.eshop_admin_commodity = ApiCommodity(token=a_token)
        cls.eshop_admin_commodityStorage = ApiCommodityStorage(token=a_token)
        cls.eshop_query = EshopQuery()

    def teardown(self):
        if self.sxu_id:
            self.eshop_query.delete_sxu_record(sxu_id=self.sxu_id)
        self.sxu_id = None

    @pytest.fixture(scope='class')
    def get_one_commodity(self):
        """前置操作获取商品，可以不用写在setup"""
        res = self.eshop_admin_commodity.api_get_sxu_list(priceBy=0)
        sku_cash = self.eshop_admin_commodity.api_get_sxu_detail(res['data']['content'][0]['id'])['data']
        res = self.eshop_admin_commodity.api_get_sxu_list(priceBy=1)
        sku_points = self.eshop_admin_commodity.api_get_sxu_detail(res['data']['content'][0]['id'])['data']
        del sku_cash['propertyList']
        del sku_points['propertyList']
        res = self.eshop_admin_commodity.api_get_sxu_list(sxuType=2, priceBy=0)
        sgu_cash = self.eshop_admin_commodity.api_get_sxu_detail(res['data']['content'][0]['id'])['data']
        res = self.eshop_admin_commodity.api_get_sxu_list(sxuType=2, priceBy=1)
        sgu_points = self.eshop_admin_commodity.api_get_sxu_detail(res['data']['content'][0]['id'])['data']
        res = self.eshop_admin_commodity.api_get_spu_list(priceBy=0)
        spu_cash = self.eshop_admin_commodity.api_get_spu_detail(res['data']['content'][0]['id'])['data']
        res = self.eshop_admin_commodity.api_get_spu_list(priceBy=1)
        spu_points = self.eshop_admin_commodity.api_get_spu_detail(res['data']['content'][0]['id'])['data']
        commodity = [[sku_cash, sku_points], [sgu_cash, sgu_points], [spu_cash, spu_points]]
        return commodity

    @pytest.mark.parametrize("sxu_type", [1, 2])
    @pytest.mark.parametrize("price_by", [0, 1])
    def test_create_commodity_sxu(self, get_one_commodity, sxu_type, price_by):
        """
        新增SXU商品
        :param get_one_commodity:
        :param sxu_type: 类型，SKU 1 SGU 2
        :param price_by: SXU类型，现金0 积分1
        :return:
        """
        sxu_payload = {}
        if sxu_type == 1:
            sxu_payload.update(get_one_commodity[0][price_by])
        if sxu_type == 2:
            sxu_payload.update(get_one_commodity[1][price_by])
        # 获取的前置商品payload，更新商品编码和业务编码（有唯一性校验）
        sxu_payload.update({'commodityNo': shortuuid.uuid(), 'bizNo': shortuuid.uuid()})
        del sxu_payload['id']
        # 新建一个sxu商品
        create_res = self.eshop_admin_commodity.api_create_edit_sxu(sxu_payload)
        self.sxu_id = create_res['data']['id']
        assert create_res['code'] == 0
        assert create_res['data']['commodityNo'] == sxu_payload['commodityNo']
        assert create_res['data']['priceBy'] == sxu_payload['priceBy']

    @pytest.mark.parametrize("sxu_type", [1, 2])
    @pytest.mark.parametrize("price_by", [0, 1])
    def test_edit_commodity_sxu(self, get_one_commodity, sxu_type, price_by):
        """
        测试编辑SXU商品
        :param get_one_commodity:
        :param sxu_type: 类型，SKU 1 SGU 2
        :param price_by: SXU类型，现金0 积分1
        :return:
        """
        sxu_payload = {}
        if sxu_type == 1:
            sxu_payload.update(get_one_commodity[0][price_by])
        if sxu_type == 2:
            sxu_payload.update(get_one_commodity[1][price_by])
        # 编辑sxu的内容
        sxu_payload.update({'state': 2, 'title': 'sxu编辑自动化测试'})
        res = self.eshop_admin_commodity.api_create_edit_sxu(sxuBody=sxu_payload)
        commodity_detail = self.eshop_admin_commodity.api_get_sxu_detail(sxu_payload['id'])['data']
        # 还原商品设置
        self.eshop_admin_commodity.api_create_edit_sxu(sxuBody=get_one_commodity[price_by])
        assert res['code'] == 0
        assert commodity_detail['state'] == sxu_payload['state']
        assert commodity_detail['title'] == sxu_payload['title']

    @pytest.mark.parametrize("sxu_type", [1, 2])
    @pytest.mark.parametrize("price_by", [0, 1])
    def test_partial_edit_sxu_title(self, get_one_commodity, sxu_type, price_by):
        """
        快速修改SXU名称
        :param get_one_commodity:
        :param sxu_type: 类型，SKU 1 SGU 2
        :param price_by: SXU类型，现金0 积分1
        :return:
        """
        sxu_payload = {}
        if sxu_type == 1:
            sxu_payload.update(get_one_commodity[0][price_by])
        if sxu_type == 2:
            sxu_payload.update(get_one_commodity[1][price_by])
        # 列表快速编辑sxu名称
        res = self.eshop_admin_commodity.api_partial_edit_sxu_title(sxuId=sxu_payload['id'], title='快速编辑sxu名称自动化测试')
        commodity_detail = self.eshop_admin_commodity.api_get_sxu_detail(sxu_payload['id'])
        #  还原商品名称
        self.eshop_admin_commodity.api_partial_edit_sxu_title(sxuId=sxu_payload['id'], title=sxu_payload['title'])
        assert res['code'] == 0
        assert commodity_detail['data']['title'] == '快速编辑sxu名称自动化测试'

    @pytest.mark.parametrize("sxu_type", [1, 2])
    @pytest.mark.parametrize("state", [0, 1, 2, 3])
    def test_commodity_sku_list(self, sxu_type, state):
        """
        测试商品管理列表，根据不同状态查询（SXU）
        :param sxu_type: 类型，SKU 1 SGU 2
        :param state: sxu状态
        :return:
        """
        commodities = self.eshop_admin_commodity.api_get_sxu_list(sxuType=sxu_type, state=state)
        # 根据不同状态进行查询
        state_set = set([commodity['state'] for commodity in commodities['data']['content']])
        assert state_set == {state}

    @pytest.mark.parametrize("sxu_type", [1, 2])
    def test_commodity_sku_list_pagination(self, sxu_type):
        """
        测试sxu列表分页
        :param sxu_type: 类型，SKU 1 SGU 2
        :return:
        """
        # 获取sku列表所有数据，按照1页100条分页
        all_data, res_obj = get_all_page(self.eshop_admin_commodity, "api_get_sxu_list", page_size=100, sxuType=sxu_type)
        ids = set([commodity_sku['id'] for commodity_sku in all_data])
        assert len(ids) == res_obj['totalElements']

    @pytest.mark.parametrize("state", [0, 1, 2, 3])
    def test_commodity_spu_list(self, state):
        """
        测试商品管理列表，根据不同状态查询（SPU）
        :param state: spu状态
        :return:
        """
        commodities = self.eshop_admin_commodity.api_get_spu_list(state=state)
        # 根据不同状态进行查询
        state_set = set([commodity['state'] for commodity in commodities['data']['content']])
        assert state_set == {state}

    def test_commodity_spu_list_pagination(self):
        """
        测试spu列表分页
        :param self:
        :return:
        """
        # 获取状态为已启用的、spu列表所有数据，并按照1页100条分页
        all_data, res_obj = get_all_page(self.eshop_admin_commodity, "api_get_spu_list", page_size=100)
        ids = set([commodity_spu['id'] for commodity_spu in all_data])
        assert len(ids) == res_obj['totalElements']

    @pytest.mark.parametrize("price_by", [0, 1])
    def test_create_commodity_spu(self, get_one_commodity, price_by):
        """
        新增SPU商品
        :param get_one_commodity:
        :param price_by: SXU类型，现金0 积分1
        :return:
        """
        spu_payload = {}
        spu_payload.update(get_one_commodity[2][price_by])
        # 修改商品编码
        spu_payload.update({'commodityNo': shortuuid.uuid()})
        del spu_payload['id']
        # 新建一个spu商品
        create_res = self.eshop_admin_commodity.api_create_edit_spu(spu_payload)
        self.sxu_id = create_res['data']['id']
        assert create_res['code'] == 0
        assert create_res['data']['commodityNo'] == spu_payload['commodityNo']
        assert create_res['data']['priceBy'] == spu_payload['priceBy']

    @pytest.mark.parametrize("price_by", [0, 1])
    def test_edit_commodity_spu(self, get_one_commodity, price_by):
        """
        测试编辑SPU商品
        :param get_one_commodity:
        :param price_by: SXU类型，现金0 积分1
        :return:
        """
        spu_payload = {}
        spu_payload.update(get_one_commodity[2][price_by])
        # 编辑spu的内容
        spu_payload.update({'state': 2, 'title': 'spu编辑自动化测试'})
        res = self.eshop_admin_commodity.api_create_edit_spu(spuBody=spu_payload)
        commodity_detail = self.eshop_admin_commodity.api_get_spu_detail(spu_payload['id'])['data']
        # 还原商品设置
        self.eshop_admin_commodity.api_create_edit_spu(spuBody=get_one_commodity[price_by])
        assert res['code'] == 0
        assert commodity_detail['state'] == spu_payload['state']
        assert commodity_detail['title'] == spu_payload['title']

    @pytest.mark.parametrize("price_by", [0, 1])
    def test_partial_edit_sxu_title(self, get_one_commodity, price_by):
        """
        快速修改SPU名称
        :param get_one_commodity:
        :param price_by: SXU类型，现金0 积分1
        :return:
        """
        spu_payload = {}
        spu_payload.update(get_one_commodity[2][price_by])
        # 列表快速编辑spu名称
        res = self.eshop_admin_commodity.api_partial_edit_sxu_title(sxuId=spu_payload['id'], title='快速编辑spu名称自动化测试')
        commodity_detail = self.eshop_admin_commodity.api_get_sxu_detail(spu_payload['id'])
        #  还原商品名称
        self.eshop_admin_commodity.api_partial_edit_sxu_title(sxuId=spu_payload['id'], title=spu_payload['title'])
        assert res['code'] == 0
        assert commodity_detail['data']['title'] == '快速编辑spu名称自动化测试'

    def test_import_spu(self):
        """
        测试spu导出与列表数据一致
        :param self:
        :return:
        """
        data_csv = self.eshop_admin_commodity.api_import_spu(state=3)
        spu_list = self.eshop_admin_commodity.api_get_spu_list(pageNo=1, pageSize=100, state=3, priceBy=None)['data']['content']
        # 将导出的数据和spu列表的数据总数做对比,后面+1是因为换行分割csv文件导致
        assert len(data_csv['text'].split('\n')) == len(spu_list) + 1

    @pytest.mark.parametrize("sxu_type", ['', 1, 2])
    @pytest.mark.parametrize("state", ['', 0, 1, 2, 3])
    def test_one_commodity_storage(self, sxu_type, state):
        """
        获取商品库存列表，不同查询条件不同结果
        :param sxu_type: 类型，SKU 1 SGU 2
        :param state: SXU状态
        """
        # 根据条件查询库存商品列表
        res = self.eshop_admin_commodityStorage.api_get_commoditys_storage(type=sxu_type, state=state)
        # res中包含的type值
        type_set = set([storage['type'] for storage in res['data']['content']])
        # res中包含的state值
        state_set = set([storage['state'] for storage in res['data']['content']])
        if sxu_type != '':
            assert type_set in [{EshopCommodityStorageTypeEnum.get_chinese(sxu_type)}, set()]
        else:
            assert type_set.issubset({1, 2})
        if state != '':
            assert state_set in [{EshopCommodityStorageStateEnum.get_chinese(state)}, set()]
        else:
            assert state_set.issubset({0, 1, 2, 3})

    @pytest.mark.parametrize("sxu_type", [1, 2])
    @pytest.mark.parametrize("price_by", [0, 1])
    @pytest.mark.parametrize("key, value", [('stockNum', 7777), ('reserveLock', 77), ('soldNum', 777)])
    def test_edit_commodity_storage(self, get_one_commodity, sxu_type, price_by, key, value):
        """
        修改单个商品实际库存、保留库存、销量
        :param get_one_commodity:
        :param price_by: SXU类型，现金0 积分1
        :param sxu_type: 类型，SKU 1 SGU 2
        """
        # 获取商品的sxu_id和commodity_no
        sxu_id = get_one_commodity[0][price_by]['id']
        commodity_no = get_one_commodity[0][price_by]['commodityNo']
        if sxu_type == 2:
            sxu_id = get_one_commodity[1][price_by]['id']
            commodity_no = get_one_commodity[1][price_by]['commodityNo']
        # 根据商品的sxuId修改商品实际库存、保留库存、销量
        res = self.eshop_admin_commodityStorage.api_edit_commodity_storage(commodityId=sxu_id,
                                                                           key=key, value=value)
        # 断言调用单个商品库存修改接口是否成功
        assert res['code'] == 0
        # 根据商品commodityId查询出该商品的实际库存、保留库存、销量
        res = self.eshop_admin_commodityStorage.api_get_commoditys_storage(keyword=commodity_no)
        # res是根据关键字查询出来的，可能返回多个商品，下面只取上面修改过的商品
        comm_detail = {}
        for comm in res['data']['content']:
            if comm['commodityNo'] == commodity_no:
                comm_detail = comm
        # 断言商品库存是否修改成功
        assert comm_detail[key] == value

    @pytest.mark.parametrize("value", [100])
    def test_edit_commoditys_storage(self, value):
        """
        增加多个商品库存
        """
        # 获取商品库存列表
        storage_list = self.eshop_admin_commodityStorage.api_get_commoditys_storage(type=1)
        # 将库存列表每个商品的sxuId取出组成一个列表
        sxuId = list([storage['id'] for storage in storage_list['data']['content']])
        # 将库存列表每个商品的commodityNo取出组成一个列表
        commodityNo = list([storage['commodityNo'] for storage in storage_list['data']['content']])
        # 将库存列表每个商品未修改前的库存取出+100，组成一个列表作为预期结果
        storage = list([int(storage['stockNum']) + 100 for storage in storage_list['data']['content']])
        # 批量增加商品库存
        res = self.eshop_admin_commodityStorage.api_edit_commoditys_storage(ids=sxuId, value=value)
        # 调用获取商品列表接口，通过commodityNo精确查询出每个商品修改后的库存，并将库存组成一个列表作为实际结果
        commodity_detail = list([self.eshop_admin_commodity.api_get_sxu_list(commodityNo=storage) for storage in
                                 commodityNo])
        edit_storage = list([storage['data']['content'][0]['stockNum'] for storage in commodity_detail])
        # 断言调用批量增加商品库存接口是否成功
        assert res['code'] == 0
        # 断言修改后库存是否等于原库存+100
        assert storage == edit_storage








